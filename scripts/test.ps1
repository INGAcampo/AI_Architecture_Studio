param([switch]$Fast,[switch]$CollectOnly,[string]$Path = "")
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
Write-Host "AIAS - Ejecutor oficial de pruebas" -ForegroundColor Cyan
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }
$Arguments = @("-m", "pytest")
if ($CollectOnly) { $Arguments += "--collect-only"; $Arguments += "-q" }
elseif ($Fast) { $Arguments += "-q"; $Arguments += "--maxfail=1" }
else { $Arguments += "-q" }
if ($Path.Trim() -ne "") { $Arguments += $Path }
& $Python @Arguments
$ExitCode = $LASTEXITCODE
if ($ExitCode -eq 0) { Write-Host "RESULTADO: PRUEBAS CORRECTAS" -ForegroundColor Green }
else { Write-Host "RESULTADO: SE DETECTARON ERRORES" -ForegroundColor Red }
exit $ExitCode
