# G10 — Security / adversarial review

**Assessment:** local static and executable self-check, NOT independent IV&V. Test cases in `verification/G10-TEST-TRACEABILITY.csv` are executed in an offline test harness with generated test keys.

| Risk | Test / treatment | Residual state |
| --- | --- | --- |
| Bit-flipped signature | Test 026/052 real signature verification | LAB-PASS / production HOLD |
| Substituted key or algorithm | Test 011/012/024/028/044/045 | LAB-PASS / trust lifecycle HOLD |
| Replay, parallel duplicate consumption | Test 005/046/047/048 | LAB-PASS / restart+distributed HOLD |
| Revoked key | Test 013/057 | LAB-PASS / persistent revocation HOLD |
| Tampered request/policy/context | Tests 006/007/008/017/018/019/020/051 | LAB-PASS / external drift HOLD |
| Expired/future timestamp | Tests 014/015/016/031/032 | LAB-PASS / trusted clock HOLD |
| Approval purpose / signer separation | Tests 009/010/037-042/053-056 | LAB-PASS / independent issuer HOLD |
| Unicode, duplicates, NaN, float | Tests 029/030/033/034/035/036 | LAB-PASS / interop HOLD |
| Unknown effect/type / unsafe default | Restricted to EFFECTFUL / policy quorum; no real gateway | HOLD |
| Cross-tenant or delegated identity | Signed fields checked against trusted binding; identity source fixture | HOLD |
| Untrusted OpenSSL provider / supply chain | OpenSSL 3.5+ presence and algorithm, no provider attestation | HOLD |
| Key material in temporary filesystem | Test-only ephemeral PEM generated and deleted after tests | HOLD (lab-only) |

**Critical note:** None of the G05 historical findings are claimed CLOSED VERIFIED because the canonical engine, independent approvals and real external system are not available as tested evidence. Any implied 'ready for production' interpretation is explicitly invalid.
