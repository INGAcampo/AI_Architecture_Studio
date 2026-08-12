param([string]$AIASRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $AIASRoot).Path
$out = Join-Path $root "AIAS_L2_TEST_RECOVERY_CURRENT"
$resultPath = Join-Path $out "RECOVERY_RESULT.json"
if (-not (Test-Path $resultPath)) { throw "Missing recovery result: $resultPath" }
$result = Get-Content $resultPath -Raw | ConvertFrom-Json
if ($result.targeted_tests.returncode -ne 0) { throw "Targeted tests failed. Review RECOVERY_RESULT.json" }
$checksums = Join-Path $out "checksums.sha256"
Get-Content $checksums | ForEach-Object {
  if ($_ -match '^([a-fA-F0-9]{64})\s+\*(.+)$') {
    $expected=$matches[1]; $file=Join-Path $out $matches[2]
    if (-not (Test-Path $file)) { throw "Missing file: $file" }
    $actual=(Get-FileHash $file -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Checksum mismatch: $file" }
  }
}
Write-Host "AIAS L2 test recovery verified successfully."
