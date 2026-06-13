# Changelog - Arculus Recovery

All notable changes to this project are documented here.

The project uses semantic versioning for user-facing releases. Earlier
`-production` suffixes were dropped beginning with the 1.5.0 line.

## [Unreleased]

- No unreleased changes documented yet.

## [1.6.0] - 2026-06-13

### Changed

- Promoted the former beta HTML build to the canonical `Arculus_Recovery.html`.
- Moved the previous canonical HTML build to `Arculus_Recovery_LTS.html`.
- Updated package metadata, Tauri metadata, release guidance, and packaged HTML assets for the 1.6.0 release line.
- Rewrote the root documentation and manual source files for the current repository layout and release flow.

### Added

- Hidden-seed handling for manually entered mnemonics after successful derivation.
- Press-and-hold reveal behavior shared by generated, imported, and manually entered hidden seeds.
- XRP QR rendering improvements, including dedicated rendering, wider modal sizing, and better mobile canvas behavior.
- QR capacity calculation fixes for payload sizing.
- PySide6 WebEngine GUI shell around the canonical HTML interface.
- Python package metadata, optional GUI extra, and package entry point.
- Tauri v2 desktop wrapper and native export bridge for PDF, JSON, CSV, TXT, `.arc`, and QR PNG saves.
- Terminal theme.
- Cross-platform Tauri asset preparation helpers.
- Windows, macOS, and Linux release documentation for desktop artifacts.

### Fixed

- XRP QR destination-tag payload formatting.
- Tagless XRP QR handling.
- QR canvas overflow on narrow viewports.
- Offline PDF export behavior by embedding jsPDF in the standalone HTML app.
- Tauri/WebView PDF initialization by avoiding an eval-based jsPDF loader.
- Tauri export failure reporting.
- Tauri asset preparation for Unicode seed-mask text.
- Listener accumulation around imported seed path/coin refresh logic.
- Misleading XRP Taproot network metadata.
- Litecoin QR URI prefix ambiguity around Bitcoin-style `3...` addresses.

## [1.5.0] - 2026-06-05

### Added

- QR Export subsystem with local QR generation and URI scheme detection.
- Forced black-on-white QR rendering for scanner reliability.
- Larger QR quiet zone.
- Settings dialog with Light, Dark, Dark+, and Terminal-oriented UI support.
- PDF export with embedded title block, root fingerprint, extended keys, and address table.
- Documentation and screenshots under the `docs/` tree.

### Fixed

- QR structural-module masking bugs.
- QR format-bit placement.
- QR mask scoring across mixed matrix cell types.
- PDF export dependency behavior for offline use.

## Earlier History

Earlier releases introduced the core offline recovery workflow:

- BIP39 validation and mnemonic generation.
- BIP32 derivation.
- Bitcoin, Litecoin, Dogecoin, Ethereum / ERC-20, and XRP support.
- P2PKH, P2WPKH-P2SH, P2WPKH, and Taproot-style derivation where supported.
- Encrypted `.arc` seed export/import.
- JSON, CSV, and TXT export.
- Python CLI support.

For exact behavior, use the current README and `docs/` reference files as the
source of truth.
