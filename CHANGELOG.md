# Changelog — Arculus Recovery

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

Changes on `main` not yet tagged in a formal release.

### Added

- Ethereum / ERC-20 address derivation in the HTML tool, Python GUI, and Python CLI.
- Offline Keccak-256 and EIP-55 checksum address support for Ethereum addresses.
- ERC-20 export fields clarifying that Ethereum token balances use the same derived account address.
- XRP classic address derivation in the HTML tool, Python GUI, and Python CLI.

### Changed

- Updated README, security guidance, contribution checklist, and threat model for Ethereum / ERC-20 and XRP support.

---

## [Arculus_Recovery] — 2026-04-24

Tagged release commit `e7cc84e`. This is the first formal GitHub release and represents a significant feature expansion over the initial commits.

### Added

**Validation output (HTML & Python)**
- Word count display
- Wordlist validity check
- Entropy bits
- Checksum bits
- Checksum match result
- BIP-39 compliance indicator
- Root fingerprint
- Keystore type detection
- Seed format detection
- Passphrase warning

**Deep validation output (HTML & Python)**
- BIP-39 seed (512-bit)
- Master private key
- Master chain code

**Taproot (P2TR) support (HTML & Python)**
- P2TR address derivation
- Bech32m address encoding
- BIP86 purpose detection (`m/86'/coin'/0'`)
- Taproot internal public and private key fields
- Taproot tweak field
- Taproot output public and private key fields
- Taproot output key parity field

**Encrypted seed workflow (HTML)**
- `Encrypt/Export Seed` action to save the active mnemonic as a `.arc` file
- `Import Seed` action to load a `.arc` file back into the app
- `Show Seed` press-and-hold button to temporarily reveal a hidden imported seed
- Inline root fingerprint display beside the `Show Seed` button

**Encrypted seed workflow (Python GUI)**
- Matching `Encrypt/Export Seed` and `Import Seed` actions
- `Show Seed` press-and-hold button
- Inline root fingerprint display

### Changed

- Standardized encrypted seed export/import to the shared `.arc` file format, enabling cross-compatibility between the HTML and Python versions.
- Updated imported-seed behavior so that encrypted seeds remain hidden on screen while still being usable for validation and key derivation.
- Extended common derivation handling to include `m/86'/coin'/0'` (Taproot/BIP86).

### Compatibility

- Added support for reading older encrypted seed formats to preserve backward compatibility while writing the new shared `.arc` format for all current exports.

---

## Pre-Release History (Commits to `main` before 2026-04-24)

The following summarizes the development history reconstructed from the repository. Exact commit dates are not shown.

### Earlier work included:

- Initial BIP39 mnemonic validation for 12-word and 24-word seeds (HTML and Python)
- BIP32 key derivation pipeline
- Address derivation for P2PKH, P2WPKH-P2SH, and P2WPKH
- Multi-coin support: Bitcoin, Litecoin, Dogecoin
- Derivation path table covering BIP44 (`m/44'`), BIP49 (`m/49'`), and BIP84 (`m/84'`) purposes
- Export of derived keys and addresses in JSON, CSV, and TXT formats (HTML and Python)
- Python CLI mode (`--mnemonic`, `--derivation`, `--script-type`, `--count`, `--output-format` flags)
- Python desktop GUI launch via `--gui` flag
- Dark mode toggle in both the HTML settings dialog and the Python settings popup
- SHA256 hash verification instructions in the README
- `SECURITY.md` covering the local execution model, recommended offline workflow, cryptographic design, and clipboard/display risks
- `CONTRIBUTING.md` with contribution guidelines
- MIT `LICENSE.md`
- Documentation screenshots for light mode and dark mode

---

## Notes on Versioning

This project currently uses a single rolling release tag (`Arculus_Recovery`) rather than semantic version numbers. The README includes SHA256 hashes for `Arculus_Recovery.html`, `index.html`, and `Arculus_Recovery.py` so users can verify the exact file state they are running, independent of the tag name.

If semantic versioning is adopted in the future, the recommended starting point would be `v1.0.0` for the current tagged release.
