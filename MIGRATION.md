# Migration Guide

This guide covers upgrading Arculus Recovery and migrating encrypted `.arc` seed backups.

## Upgrade Checklist

1. Download or transfer the full new project folder.
2. Verify hashes before opening the app with real seed material.
3. Replace the HTML file, Python package, packaged assets, documentation, and desktop wrapper together.
4. Test with a known mnemonic before operational use.
5. Re-export older `.arc` files with the current release when practical.

Do not mix files from different releases. The root HTML app, `src/arculus_recovery/assets/`, Python code, and Tauri package should represent the same release state.

## Hash Verification

macOS or Linux:

```bash
find Arculus_Recovery.html Arculus_Recovery_LTS.html Arculus_Recovery.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File Arculus_Recovery.html,Arculus_Recovery_LTS.html,Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

Compare the output with hashes published for the exact release you are using.

## `.arc` Format History

| Format | Status | Notes |
| --- | --- | --- |
| `ARCULUS-ARC-V2` armored text | Current export format | PBKDF2-HMAC-SHA512, 1,000,000 iterations for new exports |
| Raw JSON `arculus-encrypted-seed-v2` | Import supported | Earlier V2 storage without armor |
| Browser `arculus-encrypted-seed-v1` | Browser import supported | Legacy AES-GCM browser format |
| `arculus-encrypted-seed-python-v1` | Import supported | Legacy Python format |
| Headerless PBKDF2-SHA256/XOR-HMAC | Import supported | Oldest compatibility path |

All new exports should use `ARCULUS-ARC-V2`.

## Migrating an Old `.arc` File

1. Start the current app on a trusted offline machine.
2. Click **Import Seed** and select the old `.arc` file.
3. Enter the old `.arc` password.
4. Verify the root fingerprint after import.
5. Click **Encrypt/Export Seed** and save a new `.arc` file.
6. Re-import the new file to confirm it decrypts.
7. Store the new file on encrypted removable media.

The new export uses a fresh random salt and nonce. You may choose a new password during export.

## Derived Export Migration

JSON, CSV, TXT, and PDF derived-output exports are snapshots. They are not migrated in place. Re-derive and re-export when:

- You need a larger address range.
- You need Taproot output added by a newer release.
- You suspect the old export used the wrong path or passphrase.
- You want the newest schema and PDF layout.

Derived exports are plaintext when private key fields are present. Handle old and new exports as sensitive key material.

## Python Environment Migration

CLI use:

```bash
python -m pip install .
```

GUI use:

```bash
python -m pip install -r requirements.txt
python Arculus_Recovery.py --gui
```

The CLI and GUI should be run from the same verified project folder unless installed from a trusted package.

## Desktop Package Migration

When moving to Tauri desktop packages:

- Verify the installer, executable, or DMG hash before opening.
- Choose the macOS artifact for the correct architecture, or use the universal DMG.
- Confirm PDF, JSON, CSV, TXT, `.arc`, and QR PNG exports prompt for a save location.
- Keep the standalone HTML file available as a fallback recovery surface.

## Post-Upgrade Validation

Before relying on the upgraded tool:

- Validate the standard `abandon ... about` mnemonic.
- Derive one known Bitcoin path and compare the expected address.
- Import and export a test `.arc` file.
- Confirm the network indicator shows offline status when disconnected.
- Confirm **Clear All** wipes visible input and output.
