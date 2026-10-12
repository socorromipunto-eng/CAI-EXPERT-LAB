# CAI-Engine — Governance demo
# Runs the full lifecycle, a human-gated eviction, chain verification and report.
# Run from inside C:\cai-engine with:
#   powershell -ExecutionPolicy Bypass -File .\demo_governance.ps1

$ErrorActionPreference = "Stop"
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"

Write-Host "==================== 1) INIT ====================" -ForegroundColor Cyan
& $py -m cai_engine init | Out-Null
& $py -m cai_engine status

Write-Host "`n============ 2) WALK LIFECYCLE MODEL -> EVICT ============" -ForegroundColor Cyan
& $py -m cai_engine set assets_discovered true            | Out-Null
& $py -m cai_engine set telemetry_validated true          | Out-Null
& $py -m cai_engine transition HARDEN
& $py -m cai_engine set baseline_hardened true            | Out-Null
& $py -m cai_engine set telemetry_active true             | Out-Null
& $py -m cai_engine transition DETECT
& $py -m cai_engine set detection_confirmed true          | Out-Null
& $py -m cai_engine transition ISOLATE
& $py -m cai_engine set malicious_presence_confirmed true | Out-Null
& $py -m cai_engine set safety_approved true              | Out-Null
& $py -m cai_engine transition EVICT

Write-Host "`n======= 3) PROPOSE ERADICATION (expect PENDING_APPROVAL) =======" -ForegroundColor Cyan
$out = & $py -m cai_engine propose examples/action_evict.json | ConvertFrom-Json
$out | ConvertTo-Json -Depth 6
$aid = $out.action_id
Write-Host "Pending action_id = $aid" -ForegroundColor Yellow

Write-Host "`n============ 4) HUMAN APPROVES (authority is final) ============" -ForegroundColor Cyan
& $py -m cai_engine approve $aid --by "Antonio Socorro"

Write-Host "`n============ 5) VERIFY HASH-CHAINED EVIDENCE LOG ============" -ForegroundColor Cyan
& $py -m cai_engine verify

Write-Host "`n==================== 6) WRITE REPORT ====================" -ForegroundColor Cyan
& $py -m cai_engine report --out report.md
Write-Host "Done. Open report.md to read the full evidence log." -ForegroundColor Green
