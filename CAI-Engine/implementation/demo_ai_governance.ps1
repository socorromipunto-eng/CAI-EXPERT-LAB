# CAI-Engine — AI governance demo (EU AI Act + CAI layers)
# Shows an AI whose recommendations are governed before they can act.
# Run from inside C:\cai-engine with:
#   powershell -ExecutionPolicy Bypass -File .\demo_ai_governance.ps1

$ErrorActionPreference = "Stop"
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"

Write-Host "==================== INIT ====================" -ForegroundColor Cyan
& $py -m cai_engine init | Out-Null

Write-Host "`n--- A) MINIMAL risk AI recommendation (expect EXECUTED) ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/ai_minimal.json

Write-Host "`n--- B) HIGH-risk AI on critical infrastructure (expect PENDING, Art. 14) ---" -ForegroundColor Cyan
$out = & $py -m cai_engine govern examples/ai_highrisk_energy.json | ConvertFrom-Json
$out | ConvertTo-Json -Depth 8
$gid = $out.action_id
Write-Host "Governed decision pending human oversight: $gid" -ForegroundColor Yellow

Write-Host "`n--- C) HIGH-risk AI, LOW confidence (expect BLOCKED, Art. 15) ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/ai_highrisk_lowconf.json

Write-Host "`n--- D) PROHIBITED practice (expect BLOCKED, Art. 5) ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/ai_prohibited.json

Write-Host "`n--- E) HUMAN approves the high-risk decision (authority is final) ---" -ForegroundColor Cyan
& $py -m cai_engine approve $gid --by "Antonio Socorro"

Write-Host "`n--- F) VERIFY hash-chained evidence log ---" -ForegroundColor Cyan
& $py -m cai_engine verify

Write-Host "`n--- G) WRITE report ---" -ForegroundColor Cyan
& $py -m cai_engine report --out report_ai_governance.md
Write-Host "Done. Open report_ai_governance.md to read the full governed-decision log." -ForegroundColor Green
