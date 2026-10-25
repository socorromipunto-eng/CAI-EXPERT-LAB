#requires -Version 5.1
# Isolated reference-implementation demonstration, not operational authorization.
[CmdletBinding()]
param([string]$PythonExecutable, [string[]]$PythonPrefix = @())
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not $PythonExecutable) {
    foreach ($name in @('py.exe','python3','python')) {
        $cmd = Get-Command -Name $name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($cmd) {
            $PythonExecutable=$cmd.Source
            if ($name -eq 'py.exe') { $PythonPrefix=@('-3') }
            break
        }
    }
}
if (-not $PythonExecutable) { throw 'Python 3.11+ is required. Nothing is installed automatically.' }
function Write-CAIMessage([string]$Message,[ValidateSet('Read','Notice','Error')][string]$Level='Read') {
    if ($Level -eq 'Error') { Write-Host $Message -ForegroundColor Red; return }
    if ($Level -eq 'Notice') {
        $vt=$Host.UI.PSObject.Properties['SupportsVirtualTerminal']
        if ($null -ne $vt -and [bool]$vt.Value) {
            $esc=[char]27
            Write-Host ($esc+'[38;2;255;165;0m'+$Message+$esc+'[0m')
        } else { Write-Host $Message -ForegroundColor DarkYellow }
        return
    }
    Write-Host $Message -ForegroundColor Green
}
function Invoke-CAIDemoNative([string[]]$Arguments) {
    $savedPreference=$ErrorActionPreference
    $savedEncoding=[Console]::OutputEncoding
    try {
        [Console]::OutputEncoding=New-Object Text.UTF8Encoding($false)
        $ErrorActionPreference='Continue'
        $out=@(& $PythonExecutable @PythonPrefix @Arguments 2>&1)
        $rc=$LASTEXITCODE
    } finally { $ErrorActionPreference=$savedPreference; [Console]::OutputEncoding=$savedEncoding }
    if ($rc -ne 0) { throw ('Demo stopped: native exit='+$rc+'; '+($out -join "`n")) }
    return ($out -join "`n")
}
$null=Invoke-CAIDemoNative -Arguments @('-X','utf8','-I','-B','-c','import sys; sys.exit(0 if sys.version_info >= (3,11) else 10)')
$demoRoot=Join-Path ([IO.Path]::GetTempPath()) ('CAI-DEMO-'+[Guid]::NewGuid().ToString('N'))
$null=[IO.Directory]::CreateDirectory($demoRoot)
$runtime=Join-Path $demoRoot 'runtime'
$report=Join-Path $demoRoot 'report.md'
$pending=$null
Push-Location $PSScriptRoot
try {
    # DEMO_SCENARIO_BEGIN: the same cases are exercised by the Python smoke test.
    $scenario=ConvertFrom-Json -InputObject @'
[
  {
    "args": [
      "init"
    ],
    "expect": "INIT"
  },
  {
    "args": [
      "govern",
      "examples/ai_minimal.json"
    ],
    "expect": "EXECUTED"
  },
  {
    "args": [
      "govern",
      "examples/ai_highrisk_energy.json"
    ],
    "expect": "PENDING_APPROVAL"
  },
  {
    "args": [
      "govern",
      "examples/ai_highrisk_lowconf.json"
    ],
    "expect": "BLOCKED"
  },
  {
    "args": [
      "govern",
      "examples/ai_prohibited.json"
    ],
    "expect": "BLOCKED"
  },
  {
    "args": [
      "approve",
      "$pending",
      "--by",
      "fixture-operator"
    ],
    "expect": "EXECUTED"
  },
  {
    "args": [
      "verify"
    ],
    "expect": "VERIFY"
  },
  {
    "args": [
      "report",
      "--out",
      "$report"
    ],
    "expect": "REPORT"
  }
]
'@
    # DEMO_SCENARIO_END
    foreach ($step in $scenario) {
        $arguments=@('-X','utf8','-B','-s','-E','-m','cai_engine','--home',$runtime)
        foreach ($arg in $step.args) {
            if ($arg -eq '$pending') {
                if (-not $pending) { throw 'Demo stopped: no pending fixture proposal.' }
                $arguments+=$pending
            } elseif ($arg -eq '$report') { $arguments+=$report }
            else { $arguments+=[string]$arg }
        }
        $text=Invoke-CAIDemoNative -Arguments $arguments
        if ($step.expect -eq 'REPORT') {
            if (-not (Test-Path -LiteralPath $report -PathType Leaf)) { throw 'Demo report missing.' }
        } else {
            $result=ConvertFrom-Json -InputObject $text -ErrorAction Stop
            if ($step.expect -eq 'INIT') {
                if ($result.current_state -cne 'MODEL') { throw 'Demo initialization did not enter MODEL.' }
            } elseif ($step.expect -eq 'FACT') {
                if ($result.fact -cne $step.args[1] -or $result.value -ne $true) { throw 'Demo fact was not recorded.' }
            } elseif ($step.expect -eq 'VERIFY') {
                if ($result.integrity_ok -ne $true) { throw 'Demo evidence verification failed.' }
            } elseif ($result.status -cne $step.expect) { throw ('Unexpected demo status: '+$text) }
            if ($step.expect -eq 'PENDING_APPROVAL') { $pending=$result.action_id }
        }
        Write-CAIMessage $text 'Read'
    }
    Write-CAIMessage ('DEMO_PASS. Isolated fixture/report: '+$demoRoot) 'Read'
    Write-CAIMessage 'NOTICE: Fixture approval labels do not authenticate a human or authorize external effects.' 'Notice'
} finally { Pop-Location }
