$ErrorActionPreference='Stop'
$repo='C:\AIAS\AI_Architecture_Studio'
Set-Location -LiteralPath $repo
$env:PYTHONPATH='src'
$runtime=Join-Path $repo '.aias_automation'
New-Item -ItemType Directory -Force -Path $runtime | Out-Null
@{ pid=$PID; started_at=(Get-Date).ToString('o'); launcher='Start-AIASAutonomousProduction.ps1' } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runtime 'AUTOMATION_LAST_START.json') -Encoding utf8
try {
  & .\.venv\Scripts\python.exe -m aias_autonomous_supervisor.supervisor resume --root $repo
  if ($LASTEXITCODE -ne 0) { throw "Supervisor exit code: $LASTEXITCODE" }
} catch {
  @{ pid=$PID; failed_at=(Get-Date).ToString('o'); error=$_.Exception.Message } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runtime 'AUTOMATION_LAST_ERROR.json') -Encoding utf8
  throw
}
