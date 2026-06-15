# Arculus Recovery

Arculus Recovery is an offline seed recovery, deterministic key derivation, and encrypted seed-backup tool. The canonical v1.6.0 application is [Arculus_Recovery.html](/T:/Arculus_Recovery/Arculus_Recovery.html): a standalone browser file that validates or generates BIP39 mnemonics, derives wallet addresses and private keys, imports or exports `.arc` seed backups, exports derived material, and generates address QR codes without contacting a server.

Use this tool only on a trusted offline machine. It handles seed phrases, BIP39 passphrases, private keys, extended private keys, WIF keys, Monero spend/view keys, Stellar secret seeds, Cardano private keys, and plaintext export files.

## Current Build

| Surface | Current role |
| --- | --- |
| `Arculus_Recovery.html` | Canonical v1.6.0 standalone HTML app and source of truth |
| `Arculus_Recovery_LTS.html` | Previous long-term-support HTML copy |
| `src/arculus_recovery/assets/Arculus_Recovery.html` | Packaged HTML asset used by Python/Tauri preparation flows |
| `Arculus_Recovery.py` | Compatibility launcher for Python GUI and CLI |
| Python CLI | Scripted derivation/export compatibility surface for the v1.6.0 coin set |
| PySide6 GUI | Desktop wrapper around the packaged HTML asset |
| Tauri wrapper | Desktop WebView wrapper with native save bridge |

Do not mix files from different releases. The root HTML, packaged assets, Python package, Tauri wrapper, documentation, and release artifacts should be treated as one build set.

## Safety Rules

1. Verify hashes before entering real seed material.
2. Disconnect Wi-Fi, Ethernet, Bluetooth, sync tools, and remote access.
3. Use a clean browser profile or live operating system when practical.
4. Do not paste seed phrases or private keys into online pages, chat systems, or hosted tools.
5. Export only what you need, store exports on encrypted media, then click **Clear All** and close the app.

No local recovery tool can protect secrets from malware, keyloggers, browser extensions, screen capture, clipboard monitors, firmware compromise, or an already-compromised operating system.

## v1.6.0 HTML Features

- 12-word and 24-word BIP39 English mnemonic validation
- CSPRNG-based 12-word and 24-word mnemonic generation
- Numbered word grid and normalized textarea input
- Hidden-seed workflow for generated, imported, and successfully derived manually entered seeds
- Press-and-hold seed reveal
- BIP39 passphrase support with root fingerprint display
- Bitcoin, Bitcoin Cash, Litecoin, Dogecoin, Ethereum / ERC-20, Solana, Stellar, Monero, Cardano, and XRP derivation
- P2PKH, P2WPKH-P2SH, P2WPKH, and P2TR address output where supported
- Bitcoin Cash CashAddr output with legacy Base58 toggle
- Ethereum EIP-55 checksummed addresses
- XRP classic addresses, with QR destination-tag prompt
- SLIP-0010 Ed25519 derivation for Solana, Stellar, and Monero
- Cardano Icarus/CIP-1852 Shelley base address derivation
- Encrypted and unprotected `.arc` seed import/export
- Password, keyfile, and keyfile + password `.arc` protection modes
- JSON, CSV, TXT, and PDF derived-output export
- Self-contained QR encoder and PNG export
- Light, Dark, Dark+, and Terminal themes
- Five-minute idle timeout with visible one-minute warning

## Quick Start

### Browser

Open the canonical file directly:

```text
Arculus_Recovery.html
```

The browser app is local-file capable. Runtime recovery use does not require npm, Python, Tauri, a CDN, or internet access.

### Python GUI

```bash
python -m pip install -r requirements.txt
python Arculus_Recovery.py --gui
```

The GUI uses PySide6 WebEngine to render the packaged HTML asset.

### Python CLI

```bash
python -m pip install .
python Arculus_Recovery.py --help
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

CLI coin support is currently `bitcoin`, `bitcoincash`, `litecoin`, `dogecoin`, `ethereum`, `solana`, `stellar`, `monero`, `cardano`, and `xrp`.

## Default HTML v1.6.0 Paths

The canonical HTML app and upgraded Python CLI support the full v1.6.0 coin set
below.

| Coin | Internal ID | Default path | Notes |
| --- | --- | --- | --- |
| Bitcoin | `bitcoin` | `m/0'` | Arculus-native default; UI initially selects P2WPKH |
| Bitcoin Cash | `bitcoincash` | `m/0'` | Default CashAddr, optional legacy Base58 |
| Litecoin | `litecoin` | `m/84'/2'/0'` | Native SegWit default |
| Dogecoin | `dogecoin` | `m/44'/3'/0'` | P2PKH default |
| Ethereum / ERC-20 | `ethereum` | `m/44'/60'/0'` | ERC-20 tokens use same account address |
| Solana | `solana` | `m/44'/501'/0'` | SLIP-0010 Ed25519 |
| Stellar | `stellar` | `m/44'/148'/0'` | StrKey public and secret seed output |
| Monero | `monero` | `m/44'/128'/0'` | Mainnet standard address output |
| Cardano | `cardano` | `m/1852'/1815'/0'/0/0` | Shelley base address output |
| XRP | `xrp` | `m/44'/144'/0'` | Destination tags are not derived |

Auto script selection uses the first purpose component: `49'` -> P2WPKH-P2SH, `84'` -> P2WPKH, `86'` -> P2TR, otherwise P2PKH. Ethereum and XRP ignore UTXO script type and use account-address logic. Solana, Stellar, Monero, and Cardano use their coin-specific Ed25519-family derivation flows.

## `.arc` Seed Backups

Current v1.6.0 exports are armored text files:

```text
ARCULUS-ARC-V2
<base64 compact JSON bundle>
```

Protected ARC V2 properties:

- 32-byte random salt
- 24-byte random nonce
- PBKDF2-HMAC-SHA512 with 1,000,000 iterations for new exports
- minimum accepted ARC V2 iteration count of 600,000
- HMAC-SHA512-labeled encryption and authentication key separation
- HMAC-SHA512 counter stream named `HMAC-SHA512-CTR`
- HMAC-SHA512 MAC over typed metadata, salt, nonce, and ciphertext

Protection modes:

- Password: password string after Unicode NFKD normalization
- Keyfile: 64 random keyfile bytes encoded into an `arc-keyfile-v1:` secret
- Keyfile + Password: encrypted keyfile plus `arc-combined-v1:` SHA-256 secret binding
- Unprotected: plaintext mnemonic JSON inside `.arc` armor, for controlled test/offline handling only

The `.arc` file stores the mnemonic only. It does not store the BIP39 passphrase.

## Derived Exports

| Format | Filename | Contents |
| --- | --- | --- |
| JSON | `Arculus_Derived_Keys_Addresses.json` | Full structured object and nested key/address material |
| CSV | `Arculus_Derived_Keys_Addresses.csv` | Flattened address rows |
| TXT | `Arculus_Derived_Keys_Addresses.txt` | Human-readable deterministic text report |
| PDF | `Arculus_Key_Export_<Coin>.pdf` | jsPDF A4 landscape export with extended keys and address table |
| QR PNG | `qr_<sanitized_address>.png` | Address URI QR image only |

JSON, CSV, TXT, and PDF exports can contain private keys. Treat them as critical secrets.

## Documentation

The text files in `docs/` are byte-level v1.6.0 specifications:

- `docs/UserGuide.txt`
- `docs/FileFormat.txt`
- `docs/Encryption.txt`
- `docs/Derivation.txt`
- `docs/QR.txt`
- `docs/Passphrase.txt`
- `docs/Recovery.txt`
- `docs/OpSec.txt`
- `docs/TestVectors.txt`

The generated manual is:

```text
docs/Arculus_Recovery_Manual.pdf
```

Build it with:

```bash
python scripts/build_manual_pdf.py
```

If your system Python lacks ReportLab, use the bundled Codex runtime or install the dependency in an isolated environment.

## Tauri Build

Prepare assets:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepare-tauri-assets.ps1
```

or:

```bash
python scripts/prepare_tauri_assets.py
```

Build:

```bash
npm run tauri -- build
```

macOS release builds can also be produced per architecture:

```bash
cargo tauri build --target x86_64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target aarch64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target universal-apple-darwin --bundles app,dmg --ci
```

Linux amd64 release packages can be produced on a Linux build host, or from a
Linux amd64 Docker builder, with:

```bash
cargo tauri build --bundles deb,rpm --ci
```

The Tauri wrapper uses the Rust `save_export` command and the `window.arculusTauriSaveExport` bridge for PDF, JSON, CSV, TXT, `.arc`, keyfile, and QR PNG saves.

## Hash Verification

Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File Arculus_Recovery.html,Arculus_Recovery_LTS.html,Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

macOS/Linux:

```bash
find Arculus_Recovery.html Arculus_Recovery_LTS.html Arculus_Recovery.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

Publish hashes for release artifacts with the exact build they came from. This repository currently contains v1.6.0 Windows installer artifacts, v1.6.0 macOS Intel, Apple Silicon, and universal `.app`/DMG artifacts, and v1.6.0 Linux amd64 binary, `.deb`, and `.rpm` artifacts.

## Repository Map

See [RepoTree.txt](/T:/Arculus_Recovery/RepoTree.txt) for the current root tree.

## License

Project-specific source and documentation are MIT licensed. Vendored third-party components retain their own upstream notices and license terms. See [LICENSE.md](/T:/Arculus_Recovery/LICENSE.md).
