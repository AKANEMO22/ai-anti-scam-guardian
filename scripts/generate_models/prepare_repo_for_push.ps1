param(
    [string]$OutputPath = "lane-end-user/core/ml/src/main/assets/scam_detector_en.tflite",
    [int]$SizeMB = 5,
    [switch]$Random,
    [switch]$Force,
    [switch]$AutoPush
)

function ExitWithError($msg, $code=1) {
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit $code
}

# Find git repo root
$repoRoot = (& git rev-parse --show-toplevel) 2>$null
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    ExitWithError "Not inside a git repository. Run this script from a repo work tree."
}

Set-Location $repoRoot

# 1) Generate model placeholder (if python available)
$pythonCmd = "python"
if (-not (Get-Command $pythonCmd -ErrorAction SilentlyContinue)) { $pythonCmd = "python3" }
if (Get-Command $pythonCmd -ErrorAction SilentlyContinue) {
    $args = @("scripts/generate_models/generate_tflite.py", "--output", $OutputPath, "--size-mb", $SizeMB)
    if ($Random) { $args += "--random" }
    if ($Force) { $args += "--force" }
    Write-Host "Running: $pythonCmd $($args -join ' ')"
    & $pythonCmd @args
    if ($LASTEXITCODE -ne 0) { ExitWithError "Model generation script failed." }
} else {
    Write-Host "Python not found in PATH — skipping generation step. You can run generate_tflite.py manually." -ForegroundColor Yellow
}

# 2) Ensure .gitignore contains patterns for .tflite
$gitignorePath = Join-Path $repoRoot ".gitignore"
if (-not (Test-Path $gitignorePath)) { New-Item -Path $gitignorePath -ItemType File -Force | Out-Null }
$existing = Get-Content -Raw -ErrorAction SilentlyContinue $gitignorePath
$patterns = @("lane-end-user/core/ml/src/main/assets/*.tflite","*.tflite")
foreach ($p in $patterns) {
    if ($existing -notmatch [regex]::Escape($p)) {
        Add-Content -Path $gitignorePath -Value ("`n# Ignore generated large tflite models`n$p`n")
        Write-Host "Added '$p' to .gitignore"
    }
}

# 3) Remove any currently tracked .tflite files in the asset folder from the index
$trackedFiles = & git ls-files -- 'lane-end-user/core/ml/src/main/assets/*.tflite' 2>$null | Where-Object { $_ -ne '' }
if ($trackedFiles.Count -gt 0) {
    Write-Host "Found tracked tflite files; removing from index (they will remain in working tree)."
    foreach ($f in $trackedFiles) {
        Write-Host "git rm --cached --ignore-unmatch -- $f"
        git rm --cached --ignore-unmatch -- $f
    }
    # commit removal if there are staged changes
    $status = & git status --porcelain
    if ($status) {
        git commit -m "Remove oversized model files from index before push" || Write-Host "No commit created"
    }
} else {
    Write-Host "No tracked .tflite files found in index."
}

# 4) Check git history for any .tflite objects (this indicates the object exists in history and may cause push rejection)
$historyHas = & git rev-list --objects --all | Select-String '\.tflite$'
if ($historyHas) {
    Write-Host "WARNING: .tflite files show up in git history. A normal push may still be rejected by remote hosts due to file size limits." -ForegroundColor Yellow
    Write-Host "Suggested actions:" -ForegroundColor Yellow
    Write-Host " - Use 'git lfs migrate import --include=""*.tflite""' to move large files into Git LFS (rewrites history; coordinate with team)."
    Write-Host " - Or remove history entries using BFG or git-filter-repo, then push force (destructive)."
    Write-Host "This script will stop to avoid accidental push. If you understand the implications and still want to push, re-run with -AutoPush." -ForegroundColor Yellow
    if (-not $AutoPush) { exit 2 }
}

# 5) Push if requested (or advise manual push)
if ($AutoPush) {
    $branch = (& git rev-parse --abbrev-ref HEAD).Trim()
    Write-Host "Pushing branch $branch to origin..."
    git push origin $branch
    exit $LASTEXITCODE
} else {
    Write-Host "Preparation done. To push now, run: git push origin <branch> or re-run this script with -AutoPush to push automatically."
}
