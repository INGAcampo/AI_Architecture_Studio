param([switch]$RunTests)
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$argsList = @("$PSScriptRoot\generate_handoff.py", "--root", $root, "--output", "AIAS_HANDOFF_CURRENT", "--zip")
if ($RunTests) { $argsList += "--run-tests" }
python @argsList
