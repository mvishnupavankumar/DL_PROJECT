param([switch]$RunTrials,[switch]$AnalyzeOnly)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
$Py=Join-Path $Root '.venv\Scripts\python.exe'
if (!(Test-Path $Py)) {$Py=(Get-Command python -ErrorAction Stop).Source}
if ($AnalyzeOnly) { & $Py (Join-Path $Root 'research_automation.py') analyze; if ($LASTEXITCODE -ne 0) {throw 'Analysis failed'}; exit $LASTEXITCODE }
& $Py (Join-Path $Root 'research_pipeline.py') --python $Py
$rc=$LASTEXITCODE
if ($rc -ne 0) { Write-Host 'Readiness blocked. No fault injection occurred. Read research\controlled_experiment\research_readiness.md.' -ForegroundColor Yellow; if ($RunTrials) {throw 'Trials refused because readiness is blocked.'}; exit $rc }
if ($RunTrials) { & $Py (Join-Path $Root 'research_automation.py') run; if ($LASTEXITCODE -ne 0) {throw 'Trial run stopped; inspect saved trial row and service state.'}; & $Py (Join-Path $Root 'research_automation.py') analyze; if ($LASTEXITCODE -ne 0) {throw 'Analysis failed'} }
