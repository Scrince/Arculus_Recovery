[CmdletBinding()]
param(
  [switch]$BuildInstallers,
  [switch]$ValidateArtifacts,
  [switch]$SkipRustTests,
  [switch]$RequireSignature
)

$ErrorActionPreference = "Stop"
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$tauriDir = Join-Path $root "src-tauri"
$configPath = Join-Path $tauriDir "tauri.conf.json"
$cargoPath = Join-Path $tauriDir "Cargo.toml"
$dist = Join-Path $root "tauri-dist"

function Assert-True([bool]$Condition, [string]$Message) {
  if (-not $Condition) { throw $Message }
}

function Assert-File([string]$Path, [long]$MinimumBytes = 1) {
  Assert-True (Test-Path -LiteralPath $Path -PathType Leaf) "Missing required file: $Path"
  $item = Get-Item -LiteralPath $Path
  Assert-True ($item.Length -ge $MinimumBytes) "File is unexpectedly small: $Path ($($item.Length) bytes)"
}

function Invoke-Checked([string]$Executable, [string[]]$Arguments, [string]$Label) {
  Write-Host "[RUN] $Label"
  & $Executable @Arguments
  if ($LASTEXITCODE -ne 0) { throw "$Label failed with exit code $LASTEXITCODE" }
}

function Test-ReleaseArtifacts([string]$Version, [string]$ArtifactRoot, [bool]$BundledLayout) {
  if ($BundledLayout) {
    $msi = @(Get-ChildItem -LiteralPath (Join-Path $ArtifactRoot "msi") -Filter "*$Version*.msi" -File -ErrorAction SilentlyContinue)
    $nsis = @(Get-ChildItem -LiteralPath (Join-Path $ArtifactRoot "nsis") -Filter "*$Version*.exe" -File -ErrorAction SilentlyContinue)
  } else {
    $msi = @(Get-ChildItem -LiteralPath $ArtifactRoot -Filter "*$Version*.msi" -File -ErrorAction SilentlyContinue)
    $nsis = @(Get-ChildItem -LiteralPath $ArtifactRoot -Filter "*$Version*-setup.exe" -File -ErrorAction SilentlyContinue)
  }
  Assert-True ($msi.Count -gt 0) "No MSI installer found under $ArtifactRoot"
  Assert-True ($nsis.Count -gt 0) "No NSIS installer found under $ArtifactRoot"

  foreach ($artifact in @($msi + $nsis)) {
    Assert-True ($artifact.Length -gt 100KB) "Installer is unexpectedly small: $($artifact.FullName)"
    Assert-True ($artifact.Name -like "*$Version*") "Installer filename does not contain version ${Version}: $($artifact.Name)"
    $hash = (Get-FileHash -LiteralPath $artifact.FullName -Algorithm SHA256).Hash
    Write-Host "[PASS] $($artifact.Name) $($artifact.Length) bytes SHA256=$hash"
    $signature = Get-AuthenticodeSignature -LiteralPath $artifact.FullName
    if ($RequireSignature) {
      Assert-True ($signature.Status -eq "Valid") "Installer signature is not valid: $($artifact.Name) ($($signature.Status))"
    } else {
      Write-Host "[INFO] Authenticode status for $($artifact.Name): $($signature.Status)"
    }
  }
}

Assert-True ($IsWindows -or $env:OS -eq "Windows_NT") "The Tauri Windows release harness must run on Windows."
Assert-File $configPath
Assert-File $cargoPath
Assert-File (Join-Path $root "YellowSphere.html") 500000

$package = Get-Content -Raw -LiteralPath (Join-Path $root "package.json") | ConvertFrom-Json
$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json
$cargoText = Get-Content -Raw -LiteralPath $cargoPath
$cargoVersionMatch = [regex]::Match($cargoText, '(?ms)^\[package\].*?^version\s*=\s*"([^"]+)"')
Assert-True $cargoVersionMatch.Success "Could not read the package version from src-tauri/Cargo.toml"
$version = [string]$config.version
Assert-True ($package.version -eq $version) "package.json version $($package.version) does not match Tauri version $version"
Assert-True ($cargoVersionMatch.Groups[1].Value -eq $version) "Cargo version $($cargoVersionMatch.Groups[1].Value) does not match Tauri version $version"
Assert-True ($config.identifier -eq "com.yellowsphere.recovery") "Unexpected Tauri identifier: $($config.identifier)"
Assert-True ($config.build.frontendDist -eq "../tauri-dist") "Unexpected frontendDist: $($config.build.frontendDist)"
Write-Host "[PASS] Tauri identity/version configuration"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
Assert-True ($null -ne $python) "Python is required to prepare and validate Tauri assets."
Invoke-Checked $python.Source @((Join-Path $root "scripts\prepare_tauri_assets.py")) "Prepare Tauri frontend assets"

$index = Join-Path $dist "index.html"
Assert-File $index 500000
Assert-File (Join-Path $dist "favicon.png") 1000
Assert-File (Join-Path $dist "settings-icon.png") 1000
$indexText = [IO.File]::ReadAllText($index, [Text.Encoding]::UTF8)
Assert-True (-not $indexText.Contains("src/yellowsphere/assets/")) "Prepared index still contains packaged-asset paths."
Assert-True ($indexText.Contains("Tauri native export failed; trying WebView download fallback.")) "Prepared index is missing the Tauri export fallback."
$scriptMatches = [regex]::Matches($indexText, '<script(?:\s[^>]*)?>(.*?)</script>', [Text.RegularExpressions.RegexOptions]::Singleline)
Assert-True ($scriptMatches.Count -gt 0) "Prepared index contains no inline scripts."
foreach ($match in $scriptMatches) {
  $bytes = [Text.Encoding]::UTF8.GetBytes($match.Groups[1].Value)
  $digest = [Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
  $hash = "sha256-$([Convert]::ToBase64String($digest))"
  Assert-True ($indexText.Contains("'$hash'")) "Prepared index CSP does not allow inline script hash $hash."
}
Assert-True ((Get-FileHash -LiteralPath (Join-Path $dist "favicon.png")).Hash -eq (Get-FileHash -LiteralPath (Join-Path $root "src\yellowsphere\assets\favicon.png")).Hash) "Prepared favicon differs from source."
Assert-True ((Get-FileHash -LiteralPath (Join-Path $dist "settings-icon.png")).Hash -eq (Get-FileHash -LiteralPath (Join-Path $root "src\yellowsphere\assets\settings-icon.png")).Hash) "Prepared settings icon differs from source."
Write-Host "[PASS] Prepared frontend assets"

foreach ($icon in @("icon.ico", "icon.png", "icon.icns")) {
  Assert-File (Join-Path $tauriDir "icons\$icon") 1000
}
Write-Host "[PASS] Tauri bundle icons"

if (-not $SkipRustTests) {
  $cargo = Get-Command cargo -ErrorAction SilentlyContinue
  Assert-True ($null -ne $cargo) "Cargo is required for Rust/Tauri tests."
  Invoke-Checked $cargo.Source @("test", "--manifest-path", $cargoPath) "Rust unit tests"
}

if ($BuildInstallers) {
  $tauri = Join-Path $root "node_modules\.bin\tauri.cmd"
  Assert-File $tauri
  Invoke-Checked $tauri @("build", "--bundles", "msi,nsis") "Build Tauri MSI and NSIS installers"
  Test-ReleaseArtifacts $version (Join-Path $tauriDir "target\release\bundle") $true
}

if ($ValidateArtifacts) { Test-ReleaseArtifacts $version (Join-Path $root "releases\tauri\windows") $false }

Write-Host "[PASS] Tauri Windows release harness completed."
