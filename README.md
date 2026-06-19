# Arculus Recovery

Arculus Recovery is an offline seed recovery, deterministic key derivation, and encrypted seed-backup tool. The v1.6.4 release candidate is [Arculus_Beta.html](/T:/Arculus_Recovery/Arculus_Beta.html): a standalone file that validates or generates BIP39 mnemonics, derives wallet addresses and private keys, imports or exports `.arc` seed backups, exports derived material, and generates address QR codes without contacting a server. It is the source being prepared for production promotion.

Use this tool only on a trusted offline machine. It handles seed phrases, BIP39 passphrases, private keys, extended private keys, WIF keys, Stellar secret seeds, Cardano private keys, and plaintext export files.

## Current Build

| Surface | Current role |
| --- | --- |
| `Arculus_Beta.html` | v1.6.4 release candidate and current browser source of truth |
| `Arculus_Recovery.html` | Previously promoted v1.6.2 production HTML; replace from the verified beta during release promotion |
| `lts/Arculus_Recovery_v1.6.0_LTS.html` | Archived v1.6.0 long-term-support browser build |
| `lts/Arculus Recovery_v1.5.0_LTS.html` | Archived v1.5.0 long-term-support browser build |
| `src/arculus_recovery/assets/Arculus_Recovery.html` | Previously packaged v1.6.2 HTML asset; synchronize during v1.6.4 promotion |
| `Arculus_Recovery.py` | Compatibility launcher for Python GUI and CLI |
| Python CLI | Scripted derivation/export compatibility surface; coin coverage may differ from the browser GUI |
| PySide6 GUI | Desktop wrapper around the packaged HTML asset |
| Tauri wrapper | Existing v1.6.2 desktop wrapper sources; rebuild after v1.6.4 asset/version synchronization |

Do not mix files from different releases. The root HTML, packaged assets, Python package, Tauri wrapper, documentation, and release artifacts should be treated as one build set.

## Safety Rules

1. Verify hashes before entering real seed material.
2. Disconnect Wi-Fi, Ethernet, Bluetooth, sync tools, and remote access.
3. Use a clean browser profile or live operating system when practical.
4. Do not paste seed phrases or private keys into online pages, chat systems, or hosted tools.
5. Export only what you need, store exports on encrypted media, then click **Clear All** and close the app.

No local recovery tool can protect secrets from malware, keyloggers, browser extensions, screen capture, clipboard monitors, firmware compromise, or an already-compromised operating system.

## Current HTML Features

- 12-word and 24-word BIP39 English mnemonic validation
- CSPRNG-based 12-word and 24-word mnemonic generation
- Numbered word grid and normalized textarea input
- Hidden-seed workflow for generated, imported, and successfully derived manually entered seeds
- Press-and-hold seed reveal
- BIP39 passphrase support with root fingerprint display
- Bitcoin, Bitcoin Cash, Litecoin, Dogecoin, Ethereum / ERC-20, BNB Chain, Avalanche C-Chain, Polygon, Cosmos / ATOM, Tron / TRC-20, Solana, Stellar, Cardano, and XRP derivation
- P2PKH, P2WPKH-P2SH, P2WPKH, and P2TR address output where supported
- Bitcoin Cash CashAddr output with legacy Base58 toggle
- Ethereum EIP-55 checksummed addresses
- Ethereum-compatible EIP-55 addresses for BNB Chain, Avalanche C-Chain, and Polygon
- Polygon PoS mainnet and Polygon Amoy testnet profiles
- XRP classic addresses, with QR destination-tag prompt
- SLIP-0010 Ed25519 derivation for Solana and Stellar
- Cardano Icarus/CIP-1852 Shelley base address derivation
- Encrypted and unprotected `.arc` seed import/export
- Password, keyfile, and keyfile + password `.arc` protection modes
- JSON, CSV, TXT, and PDF derived-output export
- Self-contained QR encoder and PNG export
- Light, Dark, Dark+, and Terminal themes
- Configurable 2/5/15-minute or Off session timeout (five-minute default),
  visible one-minute warning, and optional 15-second tab-switch grace period

## Quick Start

### Browser

Open the canonical file directly:

```text
Arculus_Beta.html
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

The Python CLI is a separate compatibility surface and may not match the active browser build. Run `python Arculus_Recovery.py --help` for its current choices.

## Default HTML Paths

The v1.6.4 `Arculus_Beta.html` browser app uses the defaults below.

| Coin | Internal ID | Default path | Notes |
| --- | --- | --- | --- |
| Bitcoin | `bitcoin` | `m/0'` | Arculus-native default; UI initially selects P2WPKH |
| Bitcoin Cash | `bitcoincash` | `m/0'` | Default CashAddr, optional legacy Base58 |
| Litecoin | `litecoin` | `m/84'/2'/0'` | Native SegWit default |
| Dogecoin | `dogecoin` | `m/44'/3'/0'` | P2PKH default |
| Ethereum / ERC-20 | `ethereum` | `m/44'/60'/0'` | ERC-20 tokens use same account address |
| BNB Chain | `bnbchain` | `m/44'/60'/0'` | Ethereum-compatible secp256k1 account |
| Avalanche C-Chain | `avalanche` | `m/44'/60'/0'` | Ethereum-compatible C-Chain account |
| Polygon | `polygon` | `m/44'/60'/0'` | Polygon PoS mainnet; Amoy testnet available |
| Cosmos / ATOM | `cosmos` | `m/44'/118'/0'` | Cosmos Bech32 account address |
| Tron / TRC-20 | `tron` | `m/44'/195'/0'` | TRC-20 tokens use the same account address |
| Solana | `solana` | `m/44'/501'/0'` | SLIP-0010 Ed25519 |
| Stellar | `stellar` | `m/44'/148'/0'` | StrKey public and secret seed output |
| Cardano | `cardano` | `m/1852'/1815'/0'/0/0` | Shelley base address output |
| XRP | `xrp` | `m/44'/144'/0'` | Destination tags are not derived |

Auto script selection uses the first purpose component: `49'` -> P2WPKH-P2SH, `84'` -> P2WPKH, `86'` -> P2TR, otherwise P2PKH. Ethereum, BNB Chain, Avalanche C-Chain, Polygon, Tron, Cosmos, and XRP ignore UTXO script type and use account-address logic. Solana, Stellar, and Cardano use their coin-specific Ed25519-family derivation flows.

## `.arc` Seed Backups

Current v1.6.4 exports retain the historical ARC V2 outer armor text marker:

```text
ARCULUS-ARC-V2
<base64 compact JSON bundle>
```

Protected internal ARC V3 properties:

- 32-byte random salt
- 12-byte random nonce
- AES-256-GCM with a 128-bit authentication tag
- fixed 512-byte zero-padded plaintext and 528-byte ciphertext/tag output
- authenticated JSON metadata, including `credential_mode`, as GCM AAD
- SHA-512 password pre-hash followed by PBKDF2-HMAC-SHA512 with 1,000,000 iterations in Password mode
- HKDF-SHA512 in Keyfile and Keyfile + Password modes

Protection modes:

- Password: password string after Unicode NFKD normalization
- Keyfile: 64 random keyfile bytes encoded into an `arc-keyfile-v1:` secret
- Keyfile + Password: keyfile bytes and NFKD password mixed by HKDF-SHA512 into an `arc-combined-v1:` secret
- Unprotected: plaintext mnemonic JSON inside `.arc` armor, for controlled test/offline handling only

The `.arc` file stores the mnemonic only. It does not store the BIP39 passphrase.

### v1.6.4 Encryption Format

`Arculus_Beta.html` writes protected bundles with internal format
`arculus-encrypted-seed-v3` while retaining the existing `ARCULUS-ARC-V2`
outer armor for parser compatibility. The decoded JSON `format` and `version`,
not the armor line, identify the cryptographic format.

ARC V3 changes include:

- AES-256-GCM with a 32-byte random salt, 12-byte random nonce, and 128-bit tag
- a 512-byte zero-padded plaintext payload so ciphertext size does not reveal
  whether the mnemonic contains 12 or 24 words
- authenticated bundle metadata, including `credential_mode`, supplied as
  AES-GCM additional authenticated data rather than a separate MAC field
- SHA-512 password pre-hashing followed by PBKDF2-HMAC-SHA512 at 1,000,000
  iterations for Password mode
- HKDF-SHA512 for high-entropy Keyfile mode and for the Keyfile + Password
  combined-secret path
- best-effort clearing of temporary password, keyfile, salt, and plaintext byte
  arrays after cryptographic use

New password-protected keyfiles use version 2 of
`arculus-recovery-keyfile-enc-v1`: AES-256-GCM, a 12-byte nonce, SHA-512
password pre-hashing, and PBKDF2-HMAC-SHA512 at 1,000,000 iterations. Keyfile
magic and format values are authenticated as GCM additional data.

Version 1.6.4 retains all legacy ARC V1/V2 and encrypted-keyfile v1 import paths.
Old files are decrypted with their original KDF, cipher, MAC, and combined-mode
secret construction; newly exported v1.6.4 files use the upgraded formats.

## Derived Exports

| Format | Filename | Contents |
| --- | --- | --- |
| JSON | `Arculus_Derived_Keys_Addresses.json` | Full structured object and nested key/address material |
| CSV | `Arculus_Derived_Keys_Addresses.csv` | Flattened address rows |
| TXT | `Arculus_Derived_Keys_Addresses.txt` | Human-readable deterministic text report |
| PDF | `Arculus_Key_Export_<Coin>.pdf` | jsPDF A4 landscape export with extended keys and address table |
| QR PNG | `qr_<sanitized_address>.png` | Address URI QR image only |

JSON, CSV, TXT, and PDF exports can contain private keys. Treat them as critical secrets.

## HTML Test Harness

The Playwright harness serves `Arculus_Beta.html` from a loopback-only HTTP
server and runs with one worker for deterministic cryptographic and UI tests.

```bash
npm install
npx playwright install chromium
npm run test:html
```

Available commands:

- `npm test` runs every Playwright test.
- `npm run test:html` runs the beta UI smoke and encryption suites.
- `npm run test:smoke` runs generation, derivation, settings, QR, and PDF flows.
- `npm run test:crypto` runs ARC V3, encrypted-keyfile v2, tamper rejection,
  independent Web Crypto conformance, and legacy compatibility tests.

When a managed Playwright browser is unavailable, set
`PLAYWRIGHT_EXECUTABLE_PATH` to an installed Chromium-family executable. The
harness fails on browser console errors and uncaught page errors.

### Python Harness

The Python harness uses the standard library only and supports the project
minimum of Python 3.10:

```bash
npm run test:python
# or: python tests/python/run_tests.py
```

It covers known BIP39 and Bitcoin BIP84 vectors, mnemonic generation, ARC V2
round trips and tamper rejection, JSON/CSV/TXT formatting, CLI execution,
version synchronization, and packaged offline GUI assets.

### Tauri Windows Release Harness

Run Windows release preflight checks and Rust unit tests without building a new
installer:

```powershell
npm run test:tauri
```

Build and validate fresh MSI and NSIS installers:

```powershell
npm run test:tauri:windows
```

The PowerShell harness validates synchronized package/Cargo/Tauri versions,
application identity, prepared frontend assets, icons, Rust tests, installer
sizes, versioned filenames, SHA-256 hashes, and Authenticode status. Use
`-ValidateArtifacts` to inspect existing current-version bundles without a new
build, or `-RequireSignature` when signed installers are mandatory.

`npm run test:release` runs Python, HTML, and Tauri preflight suites. Installer
building remains opt-in because it requires the Windows Tauri toolchain and can
take substantially longer.

## Documentation

The text files in `docs/` specify the v1.6.4 release-candidate behavior and preserve
explicitly labeled v1.6.0 LTS compatibility material where required:

Until promotion, `Arculus_Beta.html` is the normative v1.6.4 browser source.
Historical release notes and hashes continue to identify their archived builds.

- `docs/UserGuide.txt`
- `docs/FileFormat.txt`
- `docs/Encryption.txt`
- `docs/Derivation.txt`
- `docs/QR.txt`
- `docs/Passphrase.txt`
- `docs/Recovery.txt`
- `docs/OpSec.txt`
- `docs/TestVectors.txt`
- `docs/Release_v1.6.1.txt`
- `docs/Release_v1.6.2.txt`
- `docs/Release_v1.6.4.txt`

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

The equivalent direct Windows release command is:

```powershell
cargo tauri build --bundles msi,nsis --ci
```

The published Windows artifacts currently remain v1.6.2. Version 1.6.4 native
artifacts must be rebuilt after source promotion; see `docs/Release_v1.6.4.txt`
for the checklist and `docs/SHA256SUMS` only for already measured artifacts.

macOS release builds can also be produced per architecture:

```bash
cargo tauri build --target x86_64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target aarch64-apple-darwin --bundles app,dmg --ci
cargo tauri build --target universal-apple-darwin --bundles app,dmg --ci
```

The current macOS release set publishes v1.6.2 x64, Apple Silicon, and universal
DMGs under `releases/tauri/macos/`. The `.app` bundles are ad-hoc
signed for local distribution; the DMGs are not Apple-notarized.

Linux amd64 release packages can be produced on a Linux build host, or from a
Linux amd64 Docker builder, with:

```bash
cargo tauri build --bundles deb,rpm --ci
```

The current Linux release set publishes a v1.6.2 amd64 raw ELF, Debian package,
and RPM package under `releases/tauri/linux/`. No Linux AppImage or Linux
arm64/aarch64 package is published for v1.6.2. Version 1.6.4 packages are not
release artifacts until rebuilt and measured.

The Tauri wrapper uses the Rust `save_export` command and the `window.arculusTauriSaveExport` bridge for PDF, JSON, CSV, TXT, `.arc`, keyfile, and QR PNG saves.

## Hash Verification

Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File 'Arculus_Beta.html','Arculus_Recovery.html','lts/Arculus_Recovery_v1.6.0_LTS.html','lts/Arculus Recovery_v1.5.0_LTS.html',Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

macOS/Linux:

```bash
find Arculus_Beta.html Arculus_Recovery.html lts/Arculus_Recovery_v1.6.0_LTS.html 'lts/Arculus Recovery_v1.5.0_LTS.html' Arculus_Recovery.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

Publish hashes for release artifacts with the exact build they came from. This
repository currently contains v1.6.4 Windows x64 executable, MSI, and NSIS
artifacts; v1.6.4 macOS Intel, Apple Silicon, and universal `.app`/DMG
artifacts; and v1.6.4 Linux amd64 binary, `.deb`, and `.rpm` artifacts.
Archived v1.6.1/v1.6.0 Windows installers and v1.6.0 macOS/Linux packages are
kept under `releases/tauri/` for reference.

## Repository Map

See [RepoTree.txt](/T:/Arculus_Recovery/RepoTree.txt) for the current root tree.

## License

Project-specific source and documentation are MIT licensed. Vendored third-party components retain their own upstream notices and license terms. See [LICENSE.md](/T:/Arculus_Recovery/LICENSE.md).
