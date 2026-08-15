$ErrorActionPreference='Stop'
$repo='C:\AIAS\AI_Architecture_Studio'
Set-Location -LiteralPath $repo
$env:PYTHONPATH='src'
& .\.venv\Scripts\python.exe -m aias_autonomous_supervisor.supervisor resume --root $repo
