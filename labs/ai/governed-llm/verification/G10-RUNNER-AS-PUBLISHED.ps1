param(
    [string]$RepositoryPath = 'C:\CAI-EXPERT-LAB'
)
$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\', '/')
$repo = [System.IO.Path]::GetFullPath($RepositoryPath).TrimEnd('\', '/')
$repoPrefix = $repo + [System.IO.Path]::DirectorySeparatorChar
if ($root.Equals($repo, [System.StringComparison]::OrdinalIgnoreCase) -or
    $root.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'HOLD: Gate10 must be run outside repository.'
}
Write-Host 'CAI GATE10 v1.0.0 | REAL ML-DSA-87 | OFFLINE LAB | NO REPO MUTATION' -ForegroundColor Cyan
Write-Host 'No downloads, dependency installs, external tools, identity federation or deployment.'

$manifest = Join-Path $root 'SHA256SUMS.txt'
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) { throw 'FAIL: Missing manifest' }
$entries = @(Get-Content -LiteralPath $manifest -Encoding UTF8 | Where-Object { $_ -ne '' })
$seen = @{}
foreach ($line in $entries) {
    $fields = $line -split '\|', 2
    if ($fields.Count -ne 2 -or $fields[0] -cnotmatch '^[0-9a-f]{64}$') { throw 'FAIL: Invalid manifest line' }
    $name = $fields[1]
    if ($name -notmatch '^[A-Za-z0-9_./-]+$' -or $name.StartsWith('/') -or
        $name.Contains('..') -or $name.Contains('//') -or $seen.ContainsKey($name)) {
        throw 'FAIL: Unsafe or repeated manifest path'
    }
    $seen[$name] = $true
    $path = [System.IO.Path]::GetFullPath((Join-Path $root ($name -replace '/', '\')))
    if (-not $path.StartsWith(($root + [System.IO.Path]::DirectorySeparatorChar),
        [System.StringComparison]::OrdinalIgnoreCase)) { throw 'FAIL: Path escapes bundle' }
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('FAIL: Missing ' + $name) }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -cne $fields[0]) { throw ('FAIL: HASH MISMATCH ' + $name) }
}
$all = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force | ForEach-Object {
    $_.FullName.Substring($root.Length + 1).Replace('\', '/')
} | Where-Object { $_ -ne 'SHA256SUMS.txt' })
if ($all.Count -ne $seen.Count) { throw 'FAIL: Manifest count or unexpected files' }
foreach ($file in $all) {
    if (-not $seen.ContainsKey($file)) { throw ('FAIL: Unmanifested file ' + $file) }
}
Write-Host ('[PASS] PACKAGE MANIFEST - ' + $seen.Count + '/' + $seen.Count) -ForegroundColor Green

$expectedLineage = Join-Path $root 'verification\G09-SOURCE-LINEAGE-SHA256.txt'
$lineage = @(Get-Content -LiteralPath $expectedLineage | Where-Object { $_ -ne '' })
foreach ($line in $lineage) {
    $fields = $line -split '\|', 2
    if ($fields.Count -ne 2) { throw 'FAIL: invalid lineage' }
    $p = Join-Path $root ($fields[1] -replace '/', '\')
    if ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -cne $fields[0]) {
        throw ('FAIL: inherited G09 file changed ' + $fields[1])
    }
}
Write-Host ('[PASS] G09 SOURCE/TEST LINEAGE - ' + $lineage.Count + '/' + $lineage.Count + ' unchanged') -ForegroundColor Green

$python = $null
$cmd = Get-Command 'py.exe' -ErrorAction SilentlyContinue
if ($null -ne $cmd) {
    & $cmd.Source -3 -c 'import sys;sys.exit(0 if sys.version_info >= (3,10) else 4)' 2>$null
    if ($LASTEXITCODE -eq 0) { $python = @($cmd.Source, '-3') }
}
if ($null -eq $python) {
    $cmd = Get-Command 'python.exe' -ErrorAction SilentlyContinue
    if ($null -ne $cmd) {
        & $cmd.Source -c 'import sys;sys.exit(0 if sys.version_info >= (3,10) else 4)' 2>$null
        if ($LASTEXITCODE -eq 0) { $python = @($cmd.Source) }
    }
}
if ($null -eq $python) { Write-Host '[HOLD] Python 3.10+ missing; no install attempted' -ForegroundColor Yellow; exit 3 }
Write-Host '[PASS] PYTHON - 3.10+' -ForegroundColor Green

$openssl = Get-Command 'openssl.exe' -ErrorAction SilentlyContinue
if ($null -eq $openssl) {
    Write-Host '[HOLD] OpenSSL 3.5+ with ML-DSA-87 missing from PATH; no install attempted' -ForegroundColor Yellow
    exit 3
}
$oldPythonPath = $env:PYTHONPATH
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldUserSite = $env:PYTHONNOUSERSITE
Push-Location -LiteralPath $root
try {
    $env:PYTHONPATH = Join-Path $root 'src'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONNOUSERSITE = '1'
    $exe = $python[0]
    $prefix = @()
    if ($python.Count -gt 1) { $prefix += $python[1] }
    & $exe @prefix -B -m cai_g10.run_gate10
    $status = $LASTEXITCODE
}
finally {
    Pop-Location
    $env:PYTHONPATH = $oldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTHONNOUSERSITE = $oldUserSite
}
if ($status -eq 3) { Write-Host '[HOLD] Gate10 real crypto provider unavailable' -ForegroundColor Yellow; exit 3 }
if ($status -ne 0) { throw 'FAIL: GATE10 LAB' }
Write-Host '[PASS] GATE10 - OFFLINE REAL ML-DSA-87 TESTS' -ForegroundColor Green
Write-Host '[HOLD] Not HSM/KMS, federation, actual CAI CORE, external execution, or independent release.' -ForegroundColor Yellow
