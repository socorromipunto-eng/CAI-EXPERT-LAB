# CAI-Engine — USA per-sector AI governance demo (NIST AI RMF / AI 600-1 / NSM-22)
# Run from inside C:\cai-engine with:
#   powershell -ExecutionPolicy Bypass -File .\demo_usa_sectors.ps1

$ErrorActionPreference = "Stop"
$py = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"

Write-Host "==================== INIT ====================" -ForegroundColor Cyan
& $py -m cai_engine init | Out-Null

Write-Host "`n--- Energy (CATASTROPHIC, SRMA: DOE) confidence 0.96 -> PENDING ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/usa_energy.json

Write-Host "`n--- Energy confidence 0.92 < 0.95 floor -> BLOCKED ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/usa_energy_lowconf.json

Write-Host "`n--- Healthcare + Generative AI (SRMA: HHS, NIST AI 600-1) -> PENDING ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/usa_healthcare_genai.json

Write-Host "`n--- Non-critical corporate IT -> EXECUTED ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/usa_corporate.json

Write-Host "`n--- Same engine, EU jurisdiction on one call (override) ---" -ForegroundColor Cyan
& $py -m cai_engine govern examples/ai_highrisk_energy.json --jurisdiction EU

Write-Host "`n--- VERIFY evidence chain ---" -ForegroundColor Cyan
& $py -m cai_engine verify

Write-Host "`n--- WRITE report ---" -ForegroundColor Cyan
& $py -m cai_engine report --out report_usa_sectors.md
Write-Host "Done. Open report_usa_sectors.md to read the per-sector governed log." -ForegroundColor Green
