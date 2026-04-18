param(
  [string]$fsckFile = 'recover_fsck_now.txt',
  [string]$outDir = 'recovered_objects_fsck2',
  [string]$outMatches = 'recover_fsck_matches2.txt'
)

if (-not (Test-Path $fsckFile)) { Write-Output "Fsck file $fsckFile not found"; exit 0 }
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
Remove-Item $outMatches -ErrorAction SilentlyContinue
$regex = 'unreachable\s+(blob|tree|commit)\s+([0-9a-f]{40})'
$terms = 'messeng|activity_main|activity_main.xml|messag|Messenger|Chat|tin nhan|nhắn|messenger_tab|MessengerFragment|R\.id\.messeng|messenger_tab'
$found = $false
Get-Content $fsckFile | ForEach-Object {
  $line = $_
  if ($line -match $regex) {
    $type=$matches[1]; $sha=$matches[2]
    Write-Output "PROCESS $type $sha"
    if ($type -eq 'blob') {
      git cat-file -p $sha 2>$null | Out-File -FilePath (Join-Path $outDir "$sha.blob.txt") -Encoding utf8
      try { $content = Get-Content -Raw (Join-Path $outDir "$sha.blob.txt") -ErrorAction SilentlyContinue } catch { $content = '' }
      if ($content -match $terms) { Add-Content $outMatches "FOUND blob ${sha}"; Add-Content $outMatches $line; $found=$true }
    } elseif ($type -eq 'tree') {
      git ls-tree -r --name-only $sha 2>$null | Out-File -FilePath (Join-Path $outDir "$sha.tree.txt") -Encoding utf8
      $names = Get-Content (Join-Path $outDir "$sha.tree.txt") -ErrorAction SilentlyContinue
      foreach ($n in $names) { if ($n -match $terms) { Add-Content $outMatches "FOUND tree ${sha}: $n"; $found=$true } }
    } elseif ($type -eq 'commit') {
      git show --name-only --pretty=format:"" $sha 2>$null | Out-File -FilePath (Join-Path $outDir "$sha.commit.files.txt") -Encoding utf8
      $names = Get-Content (Join-Path $outDir "$sha.commit.files.txt") -ErrorAction SilentlyContinue
      foreach ($n in $names) { if ($n -match $terms) { Add-Content $outMatches "FOUND commit ${sha}: $n"; $found=$true } }
    }
  }
}
if (-not $found) { Write-Output 'No matches found in unreachable objects.' } else { Write-Output "Matches saved to $outMatches" }