param([switch]$Once)
$ErrorActionPreference='Stop'
$repo='C:\AIAS\AI_Architecture_Studio'
$runtime=Join-Path $repo '.aias_automation'
New-Item -ItemType Directory -Force -Path $runtime | Out-Null
$statePath=Join-Path $runtime 'AUTOMATION_STATE.json'
$watchdogPath=Join-Path $runtime 'AUTOMATION_WATCHDOG.json'
$restarts=0
do {
  $state=if(Test-Path $statePath){ Get-Content $statePath -Raw | ConvertFrom-Json }else{$null}
  $gate=if($state){$state.gate_current}else{'NOT_STARTED'}
  $record=@{pid=$PID;started_at=(Get-Date).ToString('o');last_check=(Get-Date).ToString('o');state=$gate;restart_count=$restarts}
  $record|ConvertTo-Json|Set-Content -LiteralPath $watchdogPath -Encoding utf8
  if($gate -in @('TARGET_REACHED','HUMAN_INPUT_REQUIRED','REPRODUCIBLE_TECHNICAL_IMPOSSIBILITY')){break}
  & (Join-Path $repo 'tools\automation\Start-AIASAutonomousProduction.ps1')
  $restarts++
  if($Once -or $restarts -ge 3){break}
  Start-Sleep -Seconds 30
} while($true)
