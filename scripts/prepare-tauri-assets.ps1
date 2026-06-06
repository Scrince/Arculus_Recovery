$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root "tauri-dist"

if (Test-Path -LiteralPath $dist) {
  Remove-Item -LiteralPath $dist -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $dist | Out-Null

$htmlSource = Join-Path $root "Arculus_Recovery.html"
$htmlOut = Join-Path $dist "index.html"
Copy-Item -LiteralPath $htmlSource -Destination $htmlOut -Force

$html = Get-Content -LiteralPath $htmlOut -Raw -Encoding UTF8
$old = @'
        } catch (err) {
          const message = err && err.message ? err.message : String(err);
          console.error('Tauri native export failed.', err);
          uiStatus(`Tauri export failed: ${message}`, 'invalid');
          return null;
        }
'@
$new = @'
        } catch (err) {
          const message = err && err.message ? err.message : String(err);
          if (message === 'Export cancelled.') {
            uiStatus('Export cancelled.', '');
            return null;
          }
          console.error('Tauri native export failed; trying WebView download fallback.', err);
          try {
            downloadBlobInBrowser(blob, filename);
            uiStatus(`Tauri native export failed; started WebView download fallback for ${filename}.`, 'valid');
            return null;
          } catch (fallbackErr) {
            const fallbackMessage = fallbackErr && fallbackErr.message ? fallbackErr.message : String(fallbackErr);
            uiStatus(`Tauri export failed: ${message}; fallback failed: ${fallbackMessage}`, 'invalid');
            return null;
          }
        }
'@
if (-not $html.Contains($old)) {
  throw "Could not apply Tauri export fallback patch to generated index.html"
}
$html = $html.Replace($old, $new)
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($htmlOut, $html, $utf8NoBom)

Write-Host "Prepared Tauri assets in $dist"
