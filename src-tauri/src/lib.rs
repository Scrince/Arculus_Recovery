use std::path::PathBuf;
use tauri::webview::{DownloadEvent, WebviewWindowBuilder};
use tauri::WebviewUrl;

const EXPORT_BRIDGE_SCRIPT: &str = r#"
(() => {
  const invoke = (command, args) => {
    if (window.__TAURI__?.core?.invoke) {
      return window.__TAURI__.core.invoke(command, args);
    }
    if (window.__TAURI__?.invoke) {
      return window.__TAURI__.invoke(command, args);
    }
    if (window.__TAURI_INTERNALS__?.invoke) {
      return window.__TAURI_INTERNALS__.invoke(command, args);
    }
    throw new Error("Tauri invoke bridge is not available.");
  };

  Object.defineProperty(window, "arculusTauriSaveExport", {
    configurable: true,
    value: (filename, contentBase64) => invoke("save_export", { filename, contentBase64 })
  });

  Object.defineProperty(window, "arculusTauriExportBridgeReady", {
    configurable: true,
    value: true
  });
})();
"#;

fn safe_filename(filename: &str) -> String {
    let cleaned: String = filename
        .chars()
        .map(|ch| match ch {
            '<' | '>' | ':' | '"' | '/' | '\\' | '|' | '?' | '*' | '\0' => '_',
            ch if ch.is_control() => '_',
            ch => ch,
        })
        .collect();
    let trimmed = cleaned.trim().trim_matches('.').to_string();
    if trimmed.is_empty() {
        "Arculus_Recovery_export".to_string()
    } else {
        trimmed
    }
}

fn downloads_dir() -> PathBuf {
    if cfg!(target_os = "windows") {
        if let Ok(profile) = std::env::var("USERPROFILE") {
            let path = PathBuf::from(profile).join("Downloads");
            if path.exists() {
                return path;
            }
        }
    }

    if let Ok(home) = std::env::var("HOME") {
        let path = PathBuf::from(home).join("Downloads");
        if path.exists() {
            return path;
        }
    }

    std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."))
}

fn export_filter(filename: &str) -> (&'static str, &'static [&'static str]) {
    match filename
        .rsplit_once('.')
        .map(|(_, ext)| ext.to_ascii_lowercase())
        .as_deref()
    {
        Some("pdf") => ("PDF", &["pdf"]),
        Some("json") => ("JSON", &["json"]),
        Some("csv") => ("CSV", &["csv"]),
        Some("txt") => ("Text", &["txt"]),
        Some("arc") => ("Arculus Encrypted Seed", &["arc"]),
        Some("png") => ("PNG Image", &["png"]),
        _ => ("Export File", &["*"]),
    }
}

fn write_export_file(path: PathBuf, bytes: &[u8]) -> Result<String, String> {
    std::fs::write(&path, bytes)
        .map_err(|err| format!("Could not write export to {}: {err}", path.display()))?;
    Ok(path.display().to_string())
}

#[tauri::command(rename_all = "camelCase")]
fn save_export(filename: String, content_base64: String) -> Result<String, String> {
    use base64::Engine as _;

    let bytes = base64::engine::general_purpose::STANDARD
        .decode(content_base64)
        .map_err(|err| format!("Export data was not valid base64: {err}"))?;
    let filename = safe_filename(&filename);
    let (filter_name, extensions) = export_filter(&filename);
    let path = rfd::FileDialog::new()
        .set_directory(downloads_dir())
        .set_file_name(&filename)
        .add_filter(filter_name, extensions)
        .save_file()
        .ok_or_else(|| "Export cancelled.".to_string())?;

    write_export_file(path, &bytes)
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_export])
        .setup(|app| {
            WebviewWindowBuilder::new(app, "main", WebviewUrl::App("index.html".into()))
                .initialization_script(EXPORT_BRIDGE_SCRIPT)
                .title("Arculus Recovery")
                .inner_size(1180.0, 860.0)
                .min_inner_size(900.0, 700.0)
                .resizable(true)
                .on_download(|_webview, event| {
                    if let DownloadEvent::Requested { destination, .. } = event {
                        let filename = destination
                            .file_name()
                            .map(|name| name.to_owned())
                            .unwrap_or_else(|| "Arculus_Recovery_export".into());
                        *destination = downloads_dir().join(filename);
                    }
                    true
                })
                .build()?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running Arculus Recovery");
}

#[cfg(test)]
mod tests {
    use super::*;
    use base64::Engine as _;

    #[test]
    fn save_export_decodes_base64_and_writes_file() {
        let filename = format!(
            "Arculus_Recovery_export_test_{}.txt",
            std::process::id()
        );
        let path = downloads_dir().join(&filename);
        if path.exists() {
            std::fs::remove_file(&path).expect("remove stale export test file");
        }

        let bytes = base64::engine::general_purpose::STANDARD
            .decode("QXJjdWx1cyBleHBvcnQgdGVzdA==")
            .expect("decode fixture");
        let saved_path =
            write_export_file(path.clone(), &bytes).expect("save export should write content");
        let bytes = std::fs::read(&saved_path).expect("read saved export test file");

        assert_eq!(bytes, b"Arculus export test");
        std::fs::remove_file(path).expect("remove export test file");
    }

    #[test]
    fn safe_filename_removes_windows_reserved_characters() {
        assert_eq!(
            safe_filename("Arculus:Recovery/export?.txt"),
            "Arculus_Recovery_export_.txt"
        );
    }
}
