# Arculus Recovery

Arculus Recovery is an offline BIP39/BIP32 recovery and key-derivation tool for Arculus-compatible recovery work and general HD wallet inspection. It can validate or generate BIP39 mnemonics, derive addresses and private keys, import or export encrypted `.arc` seed backups, and export derived results without contacting any server.

The canonical app is the standalone `Arculus_Recovery.html` file. The PySide6 and Tauri desktop apps package that same HTML interface. The Python CLI uses the Python derivation engine for scripted recovery sessions.

## Release Channels

- `Arculus_Recovery.html` is the current promoted v1.6.0 HTML release.
- `Arculus_Recovery_LTS.html` keeps the previous long-term-support HTML build.
- `Arculus_Recovery.py` is the compatibility launcher for the PySide6 GUI and CLI.
- `releases/tauri/` contains locally built desktop artifacts when present.

Use the current project files as a set. Do not mix a new HTML file with an older `src/`, packaged asset, or desktop wrapper.

## Safety First

Use this tool offline on a trusted machine.

1. Verify file hashes before using real seed material.
2. Disconnect Ethernet, Wi-Fi, Bluetooth, and any other network interfaces.
3. Use a clean browser profile or a live operating system where practical.
4. Never share a seed phrase, BIP39 passphrase, `.arc` password, private key, WIF key, or derived export.
5. Click **Clear All** and close the app when finished.

No recovery tool can protect secrets from malware, keyloggers, screen capture, clipboard monitors, or an already-compromised operating system.

## Main Features

- BIP39 validation for 12-word and 24-word English mnemonics
- Cryptographically random 12-word or 24-word mnemonic generation
- Numbered word grid with inline word-list feedback
- Hidden-seed workflow for generated, imported, and manually entered seeds
- Press-and-hold seed reveal
- Root fingerprint display for verification
- Address derivation for Bitcoin, Litecoin, Dogecoin, Ethereum / ERC-20, and XRP
- Bitcoin, Litecoin, and Dogecoin support for P2PKH, P2WPKH-P2SH, and P2WPKH
- Taproot / BIP86 support where enabled by the selected coin
- Ethereum EIP-55 account addresses
- XRP classic `r...` addresses
- Encrypted `.arc` seed export/import
- Derived-output export as JSON, CSV, TXT, or PDF
- Self-contained QR export with XRP destination-tag handling
- Light, Dark, Dark+, and Terminal themes
- Tauri desktop save bridge for native file export in packaged builds

## Quick Start

### Browser

Open `Arculus_Recovery.html` directly in a browser:

```text
Arculus_Recovery.html
```

The file is self-contained. Runtime use does not require npm, Python, Tauri, `vendor/`, a CDN, or network access.

### Python GUI

Install the GUI dependency, then launch the desktop wrapper:

```bash
python -m pip install -r requirements.txt
python Arculus_Recovery.py --gui
```

The GUI renders the canonical HTML app in PySide6 WebEngine.

### Python CLI

CLI mode does not require the GUI extra when installed as a package:

```bash
python -m pip install .
```

Example:

```bash
python Arculus_Recovery.py \
  --mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about" \
  --derivation "m/84'/0'/0'" \
  --script-type p2wpkh \
  --coin bitcoin \
  --count 5 \
  --output-format json
```

Important CLI flags:

| Flag | Description |
| --- | --- |
| `--gui` | Launch the PySide6 desktop GUI |
| `--mnemonic` | BIP39 mnemonic, quoted as one string |
| `--passphrase` | Optional BIP39 passphrase |
| `--derivation` | Account-level BIP32 path |
| `--all-common` | Derive common purpose paths for the selected coin |
| `--script-type` | `auto`, `p2pkh`, `p2wpkh-p2sh`, `p2wpkh`, or `p2tr` |
| `--count` | Address count per branch |
| `--coin` | `bitcoin`, `litecoin`, `dogecoin`, `ethereum`, or `xrp` |
| `--testnet` | Enable supported testnet parameters |
| `--output-format` | `json`, `csv`, or `txt` |
| `--version` | Print the Python core version |

## Recovery Workflow

1. Start the app on an offline machine.
2. Enter a 12-word or 24-word mnemonic, generate one, or import an encrypted `.arc` file.
3. Validate the mnemonic and resolve any word-list or checksum errors.
4. Enter the BIP39 passphrase only if the wallet used one.
5. Choose the coin, path, script type, count, and range.
6. Derive keys and addresses.
7. Verify the root fingerprint or at least one known address before exporting.
8. Export only the material you need.
9. Store exports on encrypted media and clear the session.

The `.arc` decryption password and the BIP39 passphrase are separate secrets. Decrypting a `.arc` file restores the mnemonic only; any BIP39 passphrase must still be entered for derivation.

## Default Paths

| Coin | Default path | Notes |
| --- | --- | --- |
| Bitcoin | `m/0'` | Arculus-native default |
| Litecoin | `m/84'/2'/0'` | Native SegWit default |
| Dogecoin | `m/44'/3'/0'` | Legacy BIP44 default |
| Ethereum / ERC-20 | `m/44'/60'/0'` | ERC-20 tokens use the same account address |
| XRP | `m/44'/144'/0'` | Destination tags are not derived |

Common UTXO account paths:

| Purpose | Script type | Bitcoin | Litecoin | Dogecoin |
| --- | --- | --- | --- | --- |
| BIP44 | P2PKH | `m/44'/0'/0'` | `m/44'/2'/0'` | `m/44'/3'/0'` |
| BIP49 | P2WPKH-P2SH | `m/49'/0'/0'` | `m/49'/2'/0'` | `m/49'/3'/0'` |
| BIP84 | P2WPKH | `m/84'/0'/0'` | `m/84'/2'/0'` | `m/84'/3'/0'` |
| BIP86 | P2TR | `m/86'/0'/0'` | `m/86'/2'/0'` | Not supported |

Use `Auto` script type when deriving standard BIP44, BIP49, BIP84, or BIP86 paths. If recovering a wallet created outside Arculus, match that wallet's path and script type before relying on output.

## Encrypted `.arc` Files

Current exports use the armored `ARCULUS-ARC-V2` format:

```text
ARCULUS-ARC-V2
<base64 compact JSON bundle>
```

High-level properties:

- Passwords are Unicode NFKD-normalized before key derivation.
- PBKDF2-HMAC-SHA512 derives a 64-byte master key from a 32-byte random salt.
- New exports use 1,000,000 KDF iterations.
- Version 2 imports with at least 600,000 iterations remain supported.
- Encryption and authentication keys are separated with HMAC-SHA512 labels.
- Plaintext is encrypted with an HMAC-SHA512 counter stream and authenticated with HMAC-SHA512.
- New exports are readable by both the browser app and Python implementation.

Supported import formats include current armored V2, raw JSON V2, legacy Python V1, legacy headerless XOR-HMAC files, and browser V1 AES-GCM files in the browser implementation.

## Documentation

The PDF manual is generated from the text files in `docs/`:

- `docs/UserGuide.txt`
- `docs/Recovery.txt`
- `docs/OpSec.txt`
- `docs/Passphrase.txt`
- `docs/FileFormat.txt`
- `docs/Encryption.txt`
- `docs/Derivation.txt`
- `docs/QR.txt`
- `docs/TestVectors.txt`
- `docs/Notice.txt`

Build the manual with ReportLab:

```bash
python -m pip install reportlab
python scripts/build_manual_pdf.py
```

Generated output:

```text
docs/Arculus_Recovery_Manual.pdf
```

## Screenshots

![Main recovery workspace](docs/screenshots/arculus-main-recovery.png)

![Derived output table](docs/screenshots/arculus-derived-output.png)

![QR export modal](docs/screenshots/arculus-qr-export.png)

![Settings dialog](docs/screenshots/arculus-settings.png)

## Hash Verification

Verify source and documentation files before operational use. On macOS or Linux:

```bash
find Arculus_Recovery.html Arculus_Recovery_LTS.html Arculus_Recovery.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

On Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File Arculus_Recovery.html,Arculus_Recovery_LTS.html,Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

Expected Windows release hashes for v1.6.0:

| Artifact | SHA-256 |
| --- | --- |
| `releases/tauri/windows/arculus-recovery.exe` | `354B04845E543BE4050BCD256D4F918D1AB97995260AA0021253452D0E278878` |
| `releases/tauri/windows/Arculus Recovery_1.6.0_x64-setup.exe` | `3CFAF01E9DB8EF245852BC84BBA17ADE99117981647E0419737CC9E33C590130` |
| `releases/tauri/windows/Arculus Recovery_1.6.0_x64_en-US.msi` | `8AE9EB9873CD4805B4E641A4183AC0070E2129F8A3E4DCB039A97842A25B649E` |

## Repository Layout

| Path | Purpose |
| --- | --- |
| `Arculus_Recovery.html` | Current standalone HTML app |
| `Arculus_Recovery_LTS.html` | Previous LTS HTML copy |
| `Arculus_Recovery.py` | Python compatibility launcher |
| `src/arculus_recovery/core.py` | Python derivation, export, encryption, and QR helpers |
| `src/arculus_recovery/cli.py` | CLI argument handling |
| `src/arculus_recovery/gui.py` | PySide6 WebEngine wrapper |
| `src/arculus_recovery/assets/` | Packaged HTML and GUI assets |
| `docs/` | Manual sources, references, screenshots, and generated PDF |
| `vendor/jspdf/` | Vendored jsPDF source used for packaging support |
| `src-tauri/` | Tauri v2 desktop wrapper |
| `scripts/` | Manual and packaging build helpers |
| `releases/` | Local release artifacts when built |

## Tauri Builds

Prepare assets on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare-tauri-assets.ps1
```

Prepare assets on macOS or Linux:

```bash
python3 scripts/prepare_tauri_assets.py
```

Build from the Tauri project environment:

```bash
cargo tauri build
```

The packaged WebView uses `window.arculusTauriSaveExport` and the Rust `save_export` command for PDF, JSON, CSV, TXT, `.arc`, and QR PNG saves. Keep `src-tauri/capabilities/default.json` and `src-tauri/permissions/export.toml` in place when rebuilding desktop artifacts.

## Release Notes

Use `CHANGELOG.md` for version history and release preparation notes. For v1.6.0, upload desktop artifacts that match the final built version and refresh the release hash list before publishing.
