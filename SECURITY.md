# Security Policy

## Overview

Arculus Recovery is an offline BIP39/BIP32 recovery and key-derivation tool. It is designed to run locally from either:

- `Arculus_Recovery.html`, opened directly in a browser
- `Arculus_Recovery.py`, run as a Python desktop GUI or CLI

The core security expectation is simple: seed phrases, passphrases, private keys, exported files, and derived addresses should stay on a trusted machine that you control. The application does not require a server, account, cloud service, telemetry endpoint, or network API.

## Supported Versions

| Version | Supported |
| --- | --- |
| Latest | Active |
| Older copies | Not supported |

Use the latest checked-in `Arculus_Recovery.html`, `index.html`, and `Arculus_Recovery.py` files together. The README includes SHA256 hashes so users can verify the exact files they are running.

## Threat Model

The project is built for users who need to inspect or recover wallet data without sending secrets to a website or remote service.

### In Scope

- Local mnemonic parsing and BIP39 checksum validation
- BIP39 seed generation from mnemonic plus optional passphrase
- BIP32 private key derivation
- Address and extended key formatting
- Encrypted `.arc` seed export/import
- JSON, CSV, and TXT derived-output exports
- Browser and Python GUI handling of hidden imported seeds

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
- No network request is needed for validation, derivation, import, or export.
- Browser storage is used only for the dark-mode preference.
- Generated downloads are created locally with `Blob` object URLs.
- The hidden imported-seed workflow keeps an imported mnemonic out of the visible text box until the user holds `Show Seed`.

Recommended browser posture:

- Disconnect from the internet before opening the file.
- Use a clean browser profile if possible.
- Disable extensions that could read page content.
- Avoid copying seed phrases to the clipboard unless absolutely necessary.

### Python Version

The Python version uses only the Python standard library. The GUI is implemented with Tkinter, and CLI mode can derive output without opening the desktop interface.

Security properties:

- No external Python packages are required.
- No network APIs are used.
- File import/export happens through local filesystem dialogs or CLI output.
- GUI dark mode and settings are local UI state only.

Recommended Python posture:

- Run from a trusted Python installation.
- Prefer an offline or air-gapped environment.
- Verify file hashes before running if the files were transferred between machines.

## Mnemonic and Key Derivation Details

The tool validates 12-word and 24-word BIP39 English mnemonics.

Validation checks include:

- Word count
- Wordlist membership
- Entropy bit length
- Checksum bit length
- Checksum match
- BIP39 compliance result
- Keystore or seed format detection
- Root fingerprint

Derivation flow:

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

## Clipboard and Display Risks

Clipboard use is convenient but risky. Other applications, browser extensions, clipboard managers, remote desktop tools, and malware may be able to read clipboard contents.

The app warns before copying a seed phrase. Even with that warning, the safest practice is to avoid copying:

- Seed phrases
- BIP39 passphrases
- Private keys
- WIF keys
- Extended private keys
- Encrypted seed backup passwords

The hidden imported-seed workflow reduces accidental display, but it does not protect against software that can inspect process memory or capture the screen.

## Recommended Offline Workflow

1. Download or transfer the latest project files.
2. Verify SHA256 hashes from the README.
3. Move the files to a trusted offline machine.
4. Disconnect networking before opening the app.
5. Run validation or derivation.
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
