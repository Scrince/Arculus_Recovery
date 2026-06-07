# Security Policy

## Overview

Arculus Recovery is an offline BIP39/BIP32 recovery and key-derivation tool. It is designed to run locally from either:

- `Arculus_Recovery.html`, opened directly in a browser
- `Arculus_Recovery.py`, run as a Python desktop GUI or CLI
- a Tauri desktop package that wraps the same canonical HTML application

The core security expectation is simple: seed phrases, passphrases, private keys, exported files, and derived addresses should stay on a trusted machine that you control. The application does not require a server, account, cloud service, telemetry endpoint, or network API.

The current derivation surface includes UTXO-style outputs for Bitcoin, Litecoin, and Dogecoin; Ethereum account addresses for ETH and ERC-20 tokens; and XRP Ledger classic addresses.

## Supported Versions

| Version | Supported |
| --- | --- |
| 1.5.0 | Active |
| Older copies | Not supported |

Use the latest project folder together, including `Arculus_Recovery.html`, `Arculus_Recovery.py`, `src/`, `vendor/`, and the relevant desktop package when using Tauri. The README includes SHA256 hashes so users can verify the exact files and release artifacts they are running.

## Threat Model

The project is built for users who need to inspect or recover wallet data without sending secrets to a website or remote service.

### In Scope

- Cryptographically random mnemonic generation (12 or 24 words)
- Local mnemonic parsing and BIP39 checksum validation
- BIP39 seed generation from mnemonic plus optional passphrase
- BIP32 private key derivation
- Address and extended key formatting
- UTXO script address formatting, Ethereum EIP-55 address formatting, and XRP Ledger classic-address formatting
- Encrypted `.arc` seed export/import
- JSON, CSV, and TXT derived-output exports
- Browser and Python GUI handling of hidden imported and generated seeds

### Out of Scope

- Malware already running on the user's device
- Screen recording, clipboard monitoring, keylogging, or memory scraping by other software
- Physical access to the machine
- User mistakes such as sharing exported private keys
- Browser, OS, Python, or firmware vulnerabilities outside this project
- Use of the tool while online on an untrusted or general-purpose machine

## Local Execution Model

### HTML Version

The HTML version is a single-file browser app. It embeds the BIP39 word list, cryptographic helpers, key-derivation code, UI, and export logic directly in the file. It is intended to be opened as a local file, not hosted on a public website.

Security properties:

- No backend service is required.
- No network request is needed for validation, derivation, import, export, or random mnemonic generation.
- Random mnemonic generation uses `crypto.getRandomValues`, the browser's CSPRNG, with no network involvement.
- Browser storage is used only for the dark-mode preference.
- Generated downloads are created locally with `Blob` object URLs.
- Generated and imported mnemonics are handled through the same hidden-seed workflow: the phrase is kept out of the visible word grid until the user holds `Show Seed`.

Recommended browser posture:

- Disconnect from the internet before opening the file.
- Use a clean browser profile if possible.
- Disable extensions that could read page content.
- Avoid copying seed phrases to the clipboard unless absolutely necessary.

### Python Version

The Python CLI core uses the Python standard library. The GUI is implemented with PySide6 WebEngine and renders the same local `Arculus_Recovery.html` file as the browser version. CLI mode can derive output without opening the desktop interface.

Security properties:

- PySide6 is required only for GUI mode.
- The PySide6 GUI injects a local vendored jsPDF bundle for PDF export rather than fetching the CDN copy at runtime.
- No network APIs are used.
- Random mnemonic generation uses `os.urandom`, the OS CSPRNG.
- File import/export happens through local filesystem dialogs or CLI output.
- GUI themes and settings are local HTML application state.

Recommended Python posture:

- Run from a trusted Python installation.
- Prefer an offline or air-gapped environment.
- Verify file hashes before running if the files were transferred between machines.

### Tauri Desktop Packages

The Tauri packages are native desktop wrappers around the canonical HTML application. They add a WebView shell and native file-save bridge, but the recovery workflow, derivation code, encrypted seed handling, and export serializers remain those of the packaged HTML application.

Security properties:

- The packaged app loads local bundled assets, not a hosted website.
- Browser-style exports are routed through the injected `window.arculusTauriSaveExport` bridge and Rust `save_export` command.
- The Tauri v2 capability and permission files restrict the native command surface used by the main window.
- macOS artifacts may be Apple Silicon-only, Intel-only, or universal. Verify that the downloaded DMG matches the target machine, or use the universal DMG.

Recommended Tauri posture:

- Verify the installer or DMG SHA256 hash from the README before opening it.
- Treat ad-hoc signed macOS builds as unsigned for trust purposes unless a Developer ID signature and notarization are provided.
- If Gatekeeper warns on macOS, bypass it only after verifying the hash and trusted source.
- Test PDF, JSON, CSV, TXT, encrypted seed, and QR PNG export behavior in the packaged build before relying on it during an operational recovery.

## Mnemonic and Key Derivation Details

The tool validates and generates 12-word and 24-word BIP39 English mnemonics.

**Validation** checks include:

- Word count
- Wordlist membership
- Entropy bit length
- Checksum bit length
- Checksum match
- BIP39 compliance result
- Keystore or seed format detection
- Root fingerprint

**Generation** uses the browser's `crypto.getRandomValues` or Python's `os.urandom` to produce the required entropy bytes, computes the BIP39 checksum, maps the result to word indices, and verifies the output against the same validation pipeline before presenting the mnemonic. A generated mnemonic that fails its own validation is rejected and never surfaced to the user.

**Derivation** flow:

1. Normalize mnemonic and passphrase with Unicode NFKD where applicable.
2. Use BIP39 PBKDF2-HMAC-SHA512 to produce the 512-bit seed.
3. Use BIP32 master key derivation.
4. Derive the selected account path.
5. Derive receiving addresses at `<account path>/0/index`.
6. Derive change addresses at `<account path>/1/index`.

Supported script outputs include:

- P2PKH
- P2WPKH-P2SH
- P2WPKH
- P2TR where supported by the selected coin

Taproot support includes BIP86-style output derivation, Bech32m encoding, internal key data, tweak data, output key data, and parity metadata.

Ethereum and XRP are account-style outputs rather than UTXO script outputs. Ethereum derivation returns EIP-55 checksummed `0x...` account addresses; ERC-20 tokens on Ethereum use the same account address. XRP derivation returns XRPL classic `r...` addresses. XRP destination tags, when required by an exchange or custodian, are operational routing metadata and are not derived from the seed.

## Export Formats

Derived key/address exports can contain highly sensitive data, including private keys and extended private keys. Treat every derived export as secret material.

Supported derived-output formats:

- JSON: structured output suitable for exact inspection or tooling
- CSV: flattened row output suitable for spreadsheet review
- TXT: human-readable labeled sections for offline review

These exports are not encrypted. If you need to preserve a derived-output export, store it on encrypted removable media or inside an encrypted container.

## Encrypted Seed Files

Encrypted seed backups use the `.arc` extension. Current exports use version 2 of the Arculus encrypted seed format.

Current `.arc` files are armored UTF-8 text with an `ARCULUS-ARC-V2` header. The visible file body is base64-encoded metadata and ciphertext rather than pretty-printed JSON.

Internally, the armored body contains:

- `magic`: `ARCULUS-ARC`
- `format`: `arculus-encrypted-seed-v2`
- `version`: `2`
- KDF metadata
- Cipher metadata
- Base64 ciphertext
- Base64 MAC

High-level cryptographic design:

- Passwords are normalized with Unicode NFKD before key derivation.
- PBKDF2-HMAC-SHA512 derives a 64-byte master key from the password and a 32-byte random salt.
- New exports use 1,000,000 KDF iterations.
- Existing version 2 imports with 600,000 or more iterations remain supported.
- Separate encryption and authentication keys are derived with domain-specific HMAC-SHA512 labels.
- Encryption uses an HMAC-SHA512 counter stream with a 24-byte random nonce.
- Authentication uses HMAC-SHA512 over versioned metadata, KDF parameters, nonce, ciphertext, and related fields.
- Binary fields are base64 encoded inside the armored bundle.

Important limitations:

- `.arc` encryption protects the seed file at rest, not while it is open in the application.
- The armored envelope hides casual JSON metadata, but it is not a substitute for encryption. The password-derived keys and MAC are the security boundary.
- A weak password can still be guessed offline by an attacker who obtains the `.arc` file.
- The browser and Python app must decrypt the mnemonic into memory to validate or derive from it.
- A newly generated mnemonic also resides in memory; the same memory-exposure caveats apply.

## Clipboard and Display Risks

Clipboard use is convenient but risky. Other applications, browser extensions, clipboard managers, remote desktop tools, and malware may be able to read clipboard contents.

The app warns before copying a seed phrase. Even with that warning, the safest practice is to avoid copying:

- Seed phrases (whether typed, imported, or generated)
- BIP39 passphrases
- Private keys
- WIF keys
- Raw hex private keys for account-based coins
- Extended private keys
- Encrypted seed backup passwords

The hidden-seed workflow (covering both imported `.arc` seeds and newly generated mnemonics) reduces accidental display, but it does not protect against software that can inspect process memory or capture the screen.

## Recommended Offline Workflow

1. Download or transfer the latest project files.
2. Verify SHA256 hashes from the README, including installer or DMG hashes when using a packaged desktop build.
3. Move the files to a trusted offline machine.
4. Disconnect networking before opening the app.
5. Run validation, generation, or derivation.
6. Export only what you need.
7. Store exports on encrypted media.
8. Clear browser downloads, clipboard history, terminal history, and temporary files if applicable.
9. Power down the machine when finished.

## Reporting a Vulnerability

Please report security issues responsibly. Do not publish exploit details in a public issue before maintainers have had a chance to investigate.

Include:

- A clear description of the issue
- Affected file or workflow
- Steps to reproduce
- Expected and actual behavior
- Potential impact
- Suggested fix, if you have one

If private vulnerability reporting is available for the repository, use it. Otherwise, contact the maintainer through the project's preferred private channel.

## Disclaimer

No recovery tool can make unsafe handling of seed material safe. Arculus Recovery is provided as-is. Users are responsible for running it in a trusted environment and protecting all seed phrases, passphrases, private keys, and exported files.



