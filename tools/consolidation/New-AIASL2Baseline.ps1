param(
  [string]$AIASRoot = (Get-Location).Path,
  [switch]$RunTests,
  [string]$TestCommand = "python -m pytest -q"
)
$ErrorActionPreference = "Stop"
$tool = Join-Path $PSScriptRoot "consolidate_audit.py"
$argsList = @($tool, "--root", $AIASRoot)
if ($RunTests) { $argsList += @("--run-tests", "--test-command", $TestCommand) }
& python @argsList
if ($LASTEXITCODE -ne 0) { throw "AIAS consolidation audit failed with exit code $LASTEXITCODE" }
