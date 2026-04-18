<#
create_and_push_main_up.ps1

Create a snapshot branch `main-up` that excludes large files (by pattern), push it to origin.

By default this script will create and push `main-up` but will NOT replace remote `main` unless `-ForceReplaceMain` is passed.

Usage:
  # Create and push main-up only
  .\create_and_push_main_up.ps1

  # Create, push and replace remote main (dangerous, will force update)
  .\create_and_push_main_up.ps1 -ForceReplaceMain
#>

param(
    [switch]$ForceReplaceMain,
    [string[]]$ExcludePatterns = @('*.tflite'),
    [string]$TempRoot = $env:TEMP,
    [switch]$DryRun
)

function ExitErr($msg, $code=1) { Write-Host $msg -ForegroundColor Red; exit $code }

# ensure in a git repo
$repoRoot = (& git rev-parse --show-toplevel) 2>$null
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { ExitErr "Not inside a git repository." }

$originUrl = (& git remote get-url origin) 2>$null
if ($LASTEXITCODE -ne 0 -or -not $originUrl) { ExitErr "Cannot determine origin URL. Ensure 'origin' remote exists." }

$timestamp = Get-Date -Format yyyyMMddHHmmss
$tmp = Join-Path $TempRoot ("main-up-snapshot-$timestamp")
Write-Host "Creating temporary snapshot at: $tmp"
New-Item -ItemType Directory -Path $tmp -Force | Out-Null

# Build robocopy args
$xf = $ExcludePatterns
$robocopyArgs = @($repoRoot, $tmp, "*.*", "/E", "/XD", ".git")
if ($xf.Count -gt 0) {
    $robocopyArgs += "/XF"
    $robocopyArgs += $xf
}

Write-Host "Copying files (excluding patterns: $($ExcludePatterns -join ', '))"
if ($DryRun) { Write-Host "Dry run: would run robocopy $($robocopyArgs -join ' ')" } else {
    robocopy @robocopyArgs | Out-Null
}

# Init git in temp dir and commit
Push-Location $tmp
if ($DryRun) { Write-Host "Dry run: git init && git checkout -b main-up && git add -A && git commit ..." } else {
    git init | Out-Null
    git checkout -b main-up | Out-Null
    git add -A | Out-Null
    $commitMsg = "Snapshot for main-up (exclude: $($ExcludePatterns -join ', '))"
    git commit -m $commitMsg 2>$null
}

# Add remote and push
if ($DryRun) { Write-Host "Dry run: git remote add origin $originUrl && git push -u origin main-up" } else {
    git remote add origin $originUrl 2>$null
    Write-Host "Pushing branch 'main-up' to origin..."
    git push -u origin main-up
    if ($LASTEXITCODE -ne 0) { Write-Host "Push returned exit code $LASTEXITCODE" -ForegroundColor Yellow }
}

if ($ForceReplaceMain) {
    if ($DryRun) { Write-Host "Dry run: git push origin main-up:main --force-with-lease" } else {
        Write-Host "Replacing remote 'main' with 'main-up' (force-with-lease)"
        git push origin main-up:main --force-with-lease
        if ($LASTEXITCODE -ne 0) { Write-Host "Force push returned exit code $LASTEXITCODE" -ForegroundColor Red }
    }
} else {
    Write-Host "Remote 'main' left unchanged. To replace remote main, re-run with -ForceReplaceMain (destructive)."
}

Pop-Location

Write-Host "Cleaning up temporary snapshot: $tmp"
if (-not $DryRun) { Remove-Item -Recurse -Force $tmp }

Write-Host "Done. 'main-up' pushed to origin (if push succeeded)."
