param([string]$RepositoryPath = 'C:\CAI-EXPERT-LAB')
$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\', '/')
$repo = [System.IO.Path]::GetFullPath($RepositoryPath).TrimEnd('\', '/')
$repoPrefix = $repo + [System.IO.Path]::DirectorySeparatorChar
if ($root.Equals($repo, [System.StringComparison]::OrdinalIgnoreCase) -or
    $root.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'HOLD: Run only outside repository.'
}
Write-Host 'CAI GATE11 v1.0.0 | OFFLINE MCP TOOLS/CALL LAB | NO REPOSITORY MUTATION' -ForegroundColor Cyan
Write-Host 'No downloads, installs, external MCP servers, production connections or effectful tools.'

$manifest = Join-Path $root 'SHA256SUMS.txt'
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) { throw 'FAIL: MISSING MANIFEST' }
$seen = @{}
$lines = @(Get-Content -LiteralPath $manifest -Encoding UTF8 | Where-Object { $_ -ne '' })
foreach ($line in $lines) {
    $parts = $line -split '\|', 2
    if ($parts.Count -ne 2 -or $parts[0] -cnotmatch '^[0-9a-f]{64}$') {
        throw 'FAIL: MALFORMED SHA256 RECORD'
    }
    $name = $parts[1]
    if ($name -notmatch '^[A-Za-z0-9_./-]+$' -or $name.Contains('..') -or
        $name.StartsWith('/') -or $name.Contains('//') -or $seen.ContainsKey($name)) {
        throw 'FAIL: UNSAFE MANIFEST ENTRY'
    }
    $seen[$name] = $true
    $path = [System.IO.Path]::GetFullPath((Join-Path $root ($name -replace '/', '\')))
    if (-not $path.StartsWith(($root + [System.IO.Path]::DirectorySeparatorChar),
          [System.StringComparison]::OrdinalIgnoreCase)) { throw 'FAIL: PATH ESCAPES BUNDLE' }
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('FAIL: MISSING ' + $name) }
    $got = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($got -cne $parts[0]) { throw ('FAIL: SHA256 MISMATCH ' + $name) }
}
$all = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force | ForEach-Object {
    $_.FullName.Substring($root.Length + 1).Replace('\', '/')
} | Where-Object { $_ -ne 'SHA256SUMS.txt' })
if ($all.Count -ne $seen.Count) { throw 'FAIL: UNEXPECTED PACKAGE FILE COUNT' }
foreach ($item in $all) {
    if (-not $seen.ContainsKey($item)) { throw ('FAIL: UNMANIFESTED ' + $item) }
}
Write-Host ('[PASS] PACKAGE MANIFEST - ' + $seen.Count + '/' + $seen.Count + ' SHA256') -ForegroundColor Green

$lineage = @(Get-Content -LiteralPath (Join-Path $root 'verification\G10-SOURCE-LINEAGE-SHA256.txt') -Encoding UTF8 |
    Where-Object { $_ -ne '' })
foreach ($line in $lineage) {
    $parts = $line -split '\|', 2
    if ($parts.Count -ne 2 -or $parts[0] -cnotmatch '^[0-9a-f]{64}$') { throw 'FAIL: LINEAGE RECORD INVALID' }
    $p = Join-Path $root ($parts[1] -replace '/', '\')
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw 'FAIL: INHERITED FILE MISSING' }
    if ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -cne $parts[0]) {
        throw ('FAIL: G10 INHERITED FILE CHANGED ' + $parts[1])
    }
}
Write-Host ('[PASS] G10 SOURCE/TEST LINEAGE - ' + $lineage.Count + '/' + $lineage.Count) -ForegroundColor Green

$python = $null
$pyCmd = Get-Command 'py.exe' -ErrorAction SilentlyContinue
if ($null -ne $pyCmd) {
    & $pyCmd.Source -3 -c 'import sys;sys.exit(0 if sys.version_info >= (3,10) else 4)' 2>$null
    if ($LASTEXITCODE -eq 0) { $python = @($pyCmd.Source, '-3') }
}
if ($null -eq $python) {
    $pythonCmd = Get-Command 'python.exe' -ErrorAction SilentlyContinue
    if ($null -ne $pythonCmd) {
        & $pythonCmd.Source -c 'import sys;sys.exit(0 if sys.version_info >= (3,10) else 4)' 2>$null
        if ($LASTEXITCODE -eq 0) { $python = @($pythonCmd.Source) }
    }
}
if ($null -eq $python) { Write-Host '[HOLD] Python 3.10+ missing' -ForegroundColor Yellow; exit 3 }
Write-Host '[PASS] PYTHON - 3.10+' -ForegroundColor Green

$opensslPath = $null
$gitCandidates = @(
    'C:\Program Files\Git\usr\bin\openssl.exe',
    'C:\Program Files\Git\mingw64\bin\openssl.exe'
)
foreach ($candidate in $gitCandidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        $opensslPath = $candidate
        break
    }
}
if ($null -eq $opensslPath) {
    $opensslCmd = Get-Command 'openssl.exe' -ErrorAction SilentlyContinue
    if ($null -ne $opensslCmd) { $opensslPath = $opensslCmd.Source }
}
if ($null -eq $opensslPath) {
    Write-Host '[HOLD] OpenSSL 3.5+ ML-DSA-87 unavailable, no install attempted' -ForegroundColor Yellow
    exit 3
}
Write-Host ('[INFO] OPENSSL PATH - ' + $opensslPath)

$oldPath = $env:PATH
$oldPythonPath = $env:PYTHONPATH
$oldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldUserSite = $env:PYTHONNOUSERSITE
Push-Location -LiteralPath $root
try {
    $opensslDir = Split-Path -Parent $opensslPath
    $env:PATH = $opensslDir + [System.IO.Path]::PathSeparator + $oldPath
    $env:PYTHONPATH = Join-Path $root 'src'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONNOUSERSITE = '1'
    $exe = $python[0]
    $prefix = @()
    if ($python.Count -gt 1) { $prefix += $python[1] }
    & $exe @prefix -B -m cai_g11.run_gate11
    $status = $LASTEXITCODE
}
finally {
    Pop-Location
    $env:PATH = $oldPath
    $env:PYTHONPATH = $oldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $oldNoBytecode
    $env:PYTHONNOUSERSITE = $oldUserSite
}
if ($status -eq 3) { Write-Host '[HOLD] PQC provider unavailable' -ForegroundColor Yellow; exit 3 }
if ($status -ne 0) { throw 'FAIL: GATE11 TEST RUNNER' }
Write-Host '[PASS] GATE11 - OFFLINE MCP SIGNED FIXTURE GATEWAY LAB' -ForegroundColor Green
Write-Host '[HOLD] Real MCP transport/OS isolation, real IdP/KMS, canonical CORE and independent IV&V' -ForegroundColor Yellow
