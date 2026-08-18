param([string]$BaselinePath = ".\AIAS_L2_CONSOLIDATION_CURRENT")
$ErrorActionPreference = "Stop"
if (-not (Test-Path $BaselinePath)) { throw "Baseline folder not found: $BaselinePath" }
$checksumFile = Join-Path $BaselinePath "checksums.sha256"
if (-not (Test-Path $checksumFile)) { throw "checksums.sha256 not found" }
Get-Content $checksumFile | ForEach-Object {
  if ($_ -match '^([a-fA-F0-9]{64})\s+\*(.+)$') {
    $expected=$matches[1]; $name=$matches[2]; $path=Join-Path $BaselinePath $name
    if (-not (Test-Path $path)) { throw "Missing baseline artifact: $name" }
    $actual=(Get-FileHash $path -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Checksum mismatch: $name" }
  }
}
Write-Host "AIAS L2 consolidation baseline verified successfully." -ForegroundColor Green
