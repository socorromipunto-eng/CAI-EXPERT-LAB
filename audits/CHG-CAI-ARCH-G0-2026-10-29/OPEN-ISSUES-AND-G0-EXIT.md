# Open issues and G0 exit criteria

## OI-01 — Original scenario evidence

The current and historical recursive trees were inspected. Neither contains the expected implementation/tests/scenarios directory. The source refers to T-01–T-10 and a baseline report; their exact original scripts and raw run receipts were not recovered in the inspected trees. The full history and external private archives were not exhaustively searched. Owner-reported or previously executed evidence must retain its provenance.

Proposed disposition: recover the originals, or adjudicate a dated replacement baseline with newly identified scripts. Keep historical b52935e and current 80cd71e results separate. No original scenario is reconstructed and falsely labelled authentic. No G0 baseline run is claimed by this dossier.

## OI-02 — Time contracts

SR-13.6, SR-14.1 and §8 use acceptance freshness, decision expiry and a signed not_after. The proposed interpretation is: reject an expired statement at acceptance, preserve accepted approval only for its exact decision digest/lifetime, and revalidate current trust and decision before dispatch. Explicitly adjudicate how a common not_after interacts with an already accepted statement. Do not impose an accidental new expiry rule from the lab or erase a signed deadline. Add a boundary test supplement before implementation if needed.

## OI-03 — Proposal wording around execution

§9 defines DISPATCHED as acknowledged dispatch, while SR-13 checks validity before signing dispatch and §11 separately handles acknowledgement/report/deadlines. Before G7, define the durable event representing send attempt and lost ACK, preserving the existing state vocabulary unless a semantic change is approved. No blind retry or assumption that missing acknowledgement proves no effect. G12/G13 uncertainty handling is input to the design, not an automatically accepted solution.

## OI-04 — Runtime capability and provider qualification

The specification requires in-process verification/signing, hybrid purposes and specific encodings/canonicalization. The lab uses subprocess OpenSSL and different envelopes. No source copy satisfies this contract. Choose an exact released package, dependency artifacts, provider/backend and vectors through a separately scoped qualification change. Latest documentation observed as a development version is not a dependency lock. Preserve the owner's working Git signing configuration.

## OI-05 — Platform and protected-profile provisioning

The contract remains neutral; Windows named pipes/effective-access checks and POSIX sockets/ACL handling are separate implementations already proposed. Hardware token, dedicated accounts, protected directories, anchor host and deployment policies have not been provisioned. Profile P cannot be approved merely by observing SID/UID or a valid fixture signature.

## OI-06 — Jurisdiction and normative source currency

Profile metadata and internal threshold proposals are preserved. This package does not refresh every legal clause, SRMA, statutory date, retention rule or post-quantum migration instrument. Before G4 adoption, verify the actor/use/asset/jurisdiction matrix and official sources; flag any change for human adjudication. Numerical engineering floors are not legislated confidence values. National security deployments remain excluded by the proposal.

## G0 exit conditions

- The owner records D01–D12 selections or specific alternatives against this exact dossier hash.
- Technical and governance reviewers record their scoped review, evidence and independence/conflicts; no fictional names or signatures.
- Original G0 baseline evidence is recovered, or the replacement criterion is explicitly adopted as a new dated change.
- Authorised baseline tests have commands, pinned environment, expected/actual results, raw receipts and hashes; known limitations are LIMIT, not target PASS.
- OI-02/03 contract ambiguities have an explicit disposition before their implementation gate. Deferring them does not authorise guessing their semantics.
- Core, profile and lab traceability remain consistent, and no gate is implicitly implemented by document approval.

All conditions are pending unless an evidence receipt explicitly closes them. The preparation is reviewable and complete within the documentary boundary. Overall G0: HOLD. Next implementation gate G1: not authorised by this package.
