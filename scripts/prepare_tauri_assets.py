from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "tauri-dist"

EXPORT_FALLBACK_OLD = """        } catch (err) {
          const message = err && err.message ? err.message : String(err);
          console.error('Tauri native export failed.', err);
          uiStatus(`Tauri export failed: ${message}`, 'invalid');
          return null;
        }
"""

EXPORT_FALLBACK_NEW = """        } catch (err) {
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
"""


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir(parents=True, exist_ok=True)

    html = (ROOT / "Arculus_Recovery.html").read_text(encoding="utf-8")
    html = html.replace("src/arculus_recovery/assets/favicon.png", "favicon.png")
    html = html.replace("src/arculus_recovery/assets/settings-icon.png", "settings-icon.png")
    if EXPORT_FALLBACK_OLD not in html:
        raise RuntimeError("Could not apply Tauri export fallback patch to generated index.html")
    html = html.replace(EXPORT_FALLBACK_OLD, EXPORT_FALLBACK_NEW)
    (DIST / "index.html").write_text(html, encoding="utf-8", newline="\n")

    for asset_name in ("favicon.png", "settings-icon.png"):
        source = ROOT / "src" / "arculus_recovery" / "assets" / asset_name
        if not source.exists():
            raise FileNotFoundError(f"Could not find required Tauri asset: {source}")
        (DIST / asset_name).write_bytes(source.read_bytes())

    print(f"Prepared Tauri assets in {DIST}")


if __name__ == "__main__":
    main()
