param([string]$AIASRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $AIASRoot).Path
$out = Join-Path $root "AIAS_L2_VERTICAL_SLICE_DISCOVERY_CURRENT"
$contract = Join-Path $out "VERTICAL_SLICE_CONTRACT.json"
if (-not (Test-Path $contract)) { throw "Missing contract: $contract" }
$data = Get-Content $contract -Raw | ConvertFrom-Json
if ($data.schema -ne "aias.l2.vertical-slice.discovery.v1") { throw "Unexpected contract schema" }
Get-Content (Join-Path $out "checksums.sha256") | ForEach-Object {
  if ($_ -match '^([a-fA-F0-9]{64})\s+\*(.+)$') {
    $expected=$matches[1]; $file=Join-Path $out $matches[2]
    if (-not (Test-Path $file)) { throw "Missing file: $file" }
    $actual=(Get-FileHash $file -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Checksum mismatch: $file" }
  }
}
Write-Host "AIAS L2 vertical-slice discovery verified successfully."
