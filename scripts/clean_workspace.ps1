# AIAS Sprint S0 - Safe workspace cleanup
# Removes generated caches only. It does NOT delete project backups or source files.

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "AIAS: limpiando caches generados..." -ForegroundColor Cyan

$cacheDirectories = Get-ChildItem -Path $ProjectRoot -Directory -Recurse -Force |
    Where-Object { $_.Name -in @("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache") }

foreach ($directory in $cacheDirectories) {
    Remove-Item -LiteralPath $directory.FullName -Recurse -Force
    Write-Host "Eliminado: $($directory.FullName)"
}

Get-ChildItem -Path $ProjectRoot -File -Recurse -Force -Include "*.pyc", "*.pyo" |
    Remove-Item -Force

Write-Host "Limpieza terminada. Los backups no fueron modificados." -ForegroundColor Green
