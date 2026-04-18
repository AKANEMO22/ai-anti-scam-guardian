param(
    [string]$Config = "scripts/generate_models/models_to_fetch.json",
    [switch]$SkipVerify,
    [int]$Timeout = 60
)

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $args = @("scripts/generate_models/fetch_models.py", "--config", $Config, "--timeout", $Timeout)
    if ($SkipVerify) { $args += "--skip-verify" }
    Write-Host "Running: python $($args -join ' ')"
    & python @args
    exit $LASTEXITCODE
}

Write-Host "Python not found. Falling back to PowerShell Invoke-WebRequest for each entry in $Config"
if (-not (Test-Path $Config)) { Write-Host "Config file not found: $Config" -ForegroundColor Red; exit 2 }

$json = Get-Content -Raw $Config | ConvertFrom-Json
foreach ($entry in $json) {
    $url = $entry.url
    $dest = $entry.path
    $name = if ($entry.name) { $entry.name } else { Split-Path $dest -Leaf }
    if (-not $url -or -not $dest) { Write-Host "Skipping invalid entry: $entry"; continue }
    New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
    Write-Host "Downloading $name -> $dest"
    try {
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -TimeoutSec $Timeout
    } catch {
        Write-Host "Failed: $_" -ForegroundColor Red
    }
}
