param([switch]$RunRelatedTests,[string]$AIASRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $AIASRoot).Path
$args = @((Join-Path $PSScriptRoot "discover_vertical_slice.py"), "--root", $root)
if ($RunRelatedTests) { $args += "--run-related-tests" }
& python @args
exit $LASTEXITCODE
