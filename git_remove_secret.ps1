<#
  Usage (recommended):
   1. Install git-filter-repo: https://github.com/newren/git-filter-repo
      (On Windows you can download and put git-filter-repo in PATH.)
   2. Run this script from the repository root in PowerShell:
        .\git_remove_secret.ps1
   3. When prompted, paste the exact secret string reported by GitHub (example: the Twilio SID shown in the push error).
   4. After it finishes, force-push rewritten history:
        git push origin --force --all
        git push origin --force --tags

  BFG fallback (if you cannot install git-filter-repo):
   - Download BFG repo-cleaner: https://rtyley.github.io/bfg-repo-cleaner/
   - Example (replace SECRET-FILE with a file containing the secret to remove):
        java -jar bfg.jar --replace-text SECRET-FILE
        git reflog expire --expire=now --all && git gc --prune=now --aggressive
        git push origin --force --all

  WARNING: Rewriting history requires all collaborators to re-clone or reset their clones.
#>

param()
Write-Host "This script will remove an exact secret string from all commits using git-filter-repo."
$secret = Read-Host -Prompt "Paste the secret/token (exact string) to remove from history (or leave blank to cancel)"
if (-not $secret) {
    Write-Host "No secret provided. Exiting."
    exit 1
}

# Create replace-file used by git-filter-repo (exact match)
$replaceFile = "$env:TEMP\git_replace.txt"
# git-filter-repo replace-text expects lines of the form:
#    <old>==><new>
# We will replace the exact secret with [REDACTED]
Set-Content -Path $replaceFile -Value "$secret==>[REDACTED]"

Write-Host "Running git-filter-repo --replace-text on the repository..."
git rev-parse --show-toplevel > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Not a git repository root. Run this in the repository root."
    exit 1
}

git filter-repo --replace-text $replaceFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Secret replacement complete."
    Write-Host "Now run the following to push the cleaned history (this rewrites remote history):"
    Write-Host "  git push origin --force --all"
    Write-Host "  git push origin --force --tags"
    Write-Host ""
    Write-Host "If you prefer BFG, see the header comments for the fallback steps."
    Write-Host "Remember: collaborators must re-clone or reset their local repos."
} else {
    Write-Error "git-filter-repo failed. Consider installing it or use BFG repo-cleaner as fallback."
}
