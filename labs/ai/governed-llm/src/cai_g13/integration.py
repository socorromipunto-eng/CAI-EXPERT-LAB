"""GATE13 lab-only adversarial integration and post-execution evidence review.

This is NOT an actual remote MCP/LLM connector, OS sandbox, independently
trusted auditor, or a canonical CAI policy implementation. Every effect is a
G12 PUT_ONCE temporary-file fixture; all identities/keys are test fixtures.
"""
from __future__ import annotations

import hashlib
import hmac
import sqlite3
from dataclasses import dataclass
from typing import Any

from cai_g10.pqc import Denied, Hold, canonical, digest
from cai_g11.gateway import Gateway, Session, MCP_TOOL
from cai_g12.execution import ControlledBroker, LabJournal, LabEvidenceSigner, EvidenceObserver, validate_request

MAX_READ_BYTES = 4096
LAB_CONTEXT = "CAI-G13-SIGNED-DUAL-GATE-LAB/V1"


@dataclass(frozen=True)
class LabPlan:
    """In-process *trusted fixture configuration*, not a signed enterprise plan.

    Its integrity is provided only by the trusted test harness/process; it must
    never be populated from an untrusted MCP document or LLM message.
    """
    tenant_id: str
    requester_id: str
    resource_id: str
    read_text_digest: str
    effect_request_digest: str
    context: str = LAB_CONTEXT

    def __post_init__(self):
        if self.context != LAB_CONTEXT:
            raise Denied('BAD_PLAN_CONTEXT')
        for field in ('read_text_digest', 'effect_request_digest'):
            val = getattr(self, field)
            if type(val) is not str or not val.startswith('sha256:') or len(val) != 71:
                raise Denied('BAD_PLAN_DIGEST')
            if any(x not in '0123456789abcdef' for x in val[7:]):
                raise Denied('BAD_PLAN_DIGEST')


class ReceiptInspector:
    """Second verifier path: cryptographic signature + SQLite state + re-read.

    The journal, observer, signer and Python process are NOT independently
    controlled. Detects simple tampering, not privileged chain recomputation.
    """
    def __init__(self, journal: LabJournal, signer: LabEvidenceSigner,
                 observer: EvidenceObserver):
        if type(journal) is not LabJournal or type(signer) is not LabEvidenceSigner or type(observer) is not EvidenceObserver:
            raise TypeError('LAB_COMPONENTS_REQUIRED')
        self.journal, self.signer, self.observer = journal, signer, observer

    def inspect(self, request: Any, receipt: Any) -> str:
        """MATCH / HOLD / DENIED. HOLD means current effect not established."""
        try:
            req = validate_request(request)
            if not self.signer.verify(receipt):
                return 'DENIED'
            payload = receipt['payload']
            if (payload['tenant_id'] != req['tenant_id'] or
                payload['request_id'] != req['request_id'] or
                payload['request_digest'] != digest(req)):
                return 'DENIED'
            with self.journal.lock:
                with self.journal._db() as con:
                    self.journal._assert_chain(con)
                    op = con.execute('SELECT operation_digest,status FROM operations WHERE tenant=? AND request_id=?',
                                     (req['tenant_id'], req['request_id'])).fetchone()
                    if op != (digest(req), 'SUCCEEDED'):
                        return 'DENIED'
                    rows = con.execute('SELECT status,observed_digest FROM events WHERE tenant=? AND request_id=? AND event_hash=?',
                                       (req['tenant_id'], req['request_id'], payload['journal_head'])).fetchall()
                    if rows != [('SUCCEEDED', payload['observed_digest'])]:
                        return 'DENIED'
                    observation, obs_digest = self.observer.observe(req)
                    if observation != 'MATCH' or obs_digest != payload['observed_digest']:
                        return 'HOLD'
                    return 'MATCH'
        except (Denied, Hold, sqlite3.DatabaseError, OSError, ValueError, TypeError, KeyError):
            return 'DENIED'


class SignedDualGatePipeline:
    """Two domain-separated authorizations; no tool-data-to-command promotion.

    A signed MCP read is NOT sufficient to execute any operation. A separate
    ML-DSA-87-signed G12 request and a trusted lab plan are mandatory.
    """
    def __init__(self, gateway: Gateway, broker: ControlledBroker,
                 inspector: ReceiptInspector, plan: LabPlan):
        if (type(gateway) is not Gateway or type(broker) is not ControlledBroker or
            type(inspector) is not ReceiptInspector or type(plan) is not LabPlan):
            raise TypeError('TRUSTED_LAB_OBJECTS_REQUIRED')
        self.gateway, self.broker, self.inspector, self.plan = gateway, broker, inspector, plan

    @staticmethod
    def _read_response(response: Any, requested_id: str) -> str | None:
        if type(response) is not dict or set(response) != {'jsonrpc', 'id', 'result'}:
            return None
        if response['jsonrpc'] != '2.0' or response['id'] != requested_id:
            return None
        result = response['result']
        if type(result) is not dict or set(result) != {'content', 'isError', '_meta'} or result['isError'] is not False:
            return None
        meta = result['_meta']
        if (type(meta) is not dict or
            meta.get('cai_data_trust') != 'UNTRUSTED_FIXTURE_DATA' or
            meta.get('cai_execution') != 'IN_MEMORY_FIXTURE_READ_ONLY' or
            set(meta) != {'cai_data_trust', 'cai_classification', 'cai_execution'}):
            return None
        content = result['content']
        if type(content) is not list or len(content) != 1 or type(content[0]) is not dict or set(content[0]) != {'type','text'}:
            return None
        item = content[0]
        if item['type'] != 'text' or type(item['text']) is not str or not item['text']:
            return None
        try:
            raw = item['text'].encode('utf-8', errors='strict')
            if len(raw) > MAX_READ_BYTES: return None
            canonical(item['text'])
        except (ValueError, UnicodeError, TypeError, Denied):
            return None
        return item['text']

    def run(self, wire: Any, session: Any, read_approvals: Any,
            effect_request: Any, effect_approvals: Any, *, fault_lab: str | None = None) -> dict:
        try:
            if type(session) is not Session or type(read_approvals) is not list or type(effect_approvals) is not list:
                return {'status':'DENIED','receipt':None,'source_digest':None}
            req = validate_request(effect_request)
            if (session.tenant != self.plan.tenant_id or session.principal != self.plan.requester_id or
                req['tenant_id'] != session.tenant or req['requester_id'] != session.principal or
                not hmac.compare_digest(digest(req), self.plan.effect_request_digest)):
                return {'status':'DENIED','receipt':None,'source_digest':None}
            data, reqid, resource, nonce = Gateway._parse(wire)
            if (resource != self.plan.resource_id or data['params']['name'] != MCP_TOOL or
                not reqid or not nonce):
                return {'status':'DENIED','receipt':None,'source_digest':None}
            result = self.gateway.call(wire, session, read_approvals)
            text = self._read_response(result, reqid)
            if text is None:
                return {'status':'DENIED','receipt':None,'source_digest':None}
            source_digest = digest(text)
            if not hmac.compare_digest(source_digest, self.plan.read_text_digest):
                return {'status':'DENIED','receipt':None,'source_digest':None}
            # Never parse, evaluate, execute or copy the source text into effect parameters.
            outcome = self.broker.execute(req, effect_approvals, fault_lab=fault_lab)
            if outcome['status'] != 'SUCCEEDED':
                return {'status':outcome['status'],'receipt':None,'source_digest':source_digest}
            verified = self.inspector.inspect(req, outcome['receipt'])
            if verified != 'MATCH':
                return {'status':'INDETERMINATE','receipt':None,'source_digest':source_digest}
            return {'status':'SUCCEEDED','receipt':outcome['receipt'],'source_digest':source_digest}
        except (Denied, Hold, KeyError, TypeError, ValueError, UnicodeError):
            return {'status':'DENIED','receipt':None,'source_digest':None}
