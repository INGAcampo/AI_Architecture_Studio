param(
  [switch]$RunFull,
  [string]$AIASRoot = "."
)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $AIASRoot).Path
$script = Join-Path $PSScriptRoot "repair_l2_test_recovery.py"
$args = @($script, "--root", $root)
if ($RunFull) { $args += "--run-full" }
& python @args
exit $LASTEXITCODE
