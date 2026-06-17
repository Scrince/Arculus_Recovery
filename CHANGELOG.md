# Changelog - Arculus Recovery

All notable user-facing and compatibility-relevant changes are documented here.
The current source of truth is `Arculus_Recovery.html` v1.6.0 plus the
byte-level references in `docs/`.

The project originally used a rolling `Arculus_Recovery` release tag, then
`-production` suffixes, and now uses plain semantic versions for promoted
releases. Older entries below preserve that history while normalizing the
format.

## [Unreleased]

### Changed

- Relocated inline jsPDF third-party attribution and license comments from
  `Arculus_Beta.html` into `docs/ThirdPartyNotices.txt` without changing
  executable HTML behavior.
- Cleaned garbled non-license comments in `Arculus_Beta.html` while leaving
  functional code unchanged.

## [1.6.0] - 2026-06-14

### Release Identity

- Promoted the repaired beta line to the canonical `Arculus_Recovery.html`
  v1.6.0 release.
- Kept the previous canonical HTML build as `Arculus_Recovery_LTS.html`.
- Updated Python package metadata, Tauri package metadata, Tauri app metadata,
  packaged HTML assets, and manual generation metadata for v1.6.0.
- Rewrote the root documentation and `docs/` technical references around the
  current byte-level behavior.
- Rebuilt `docs/Arculus_Recovery_Manual.pdf` from the updated text sources.
- Built v1.6.0 macOS Tauri release artifacts for Intel, Apple Silicon, and
  universal macOS distribution.
- Built v1.6.0 Linux Tauri release artifacts for amd64 distribution.

### Added

- Bitcoin Cash derivation in the canonical HTML app, including CashAddr output
  and optional legacy Base58 display.
- Solana derivation using SLIP-0010 Ed25519 hardened paths and Base58 public
  address output.
- Stellar derivation using SLIP-0010 Ed25519, StrKey public addresses, and
  Stellar secret seed output.
- Monero derivation using SLIP-0010 Ed25519-derived spend material, private
  spend/view keys, public spend/view keys, and standard mainnet address output.
- Cardano Icarus/CIP-1852 Shelley base address derivation.
- `.arc` Password, Keyfile, and Keyfile + Password protection modes.
- Raw keyfile format `arculus-recovery-keyfile-v1`.
- Encrypted keyfile format `arculus-recovery-keyfile-enc-v1`.
- Unprotected armored `.arc` export mode for controlled offline/test handling.
- Manual-entry seed auto-mask after successful derivation, using the same hidden
  seed workflow as generated and imported seeds.
- Shared press-and-hold reveal behavior for generated, imported, and manually
  entered hidden seeds.
- Tauri v2 desktop wrapper around the canonical HTML app.
- Tauri native save bridge for PDF, JSON, CSV, TXT, `.arc`, keyfile, and QR PNG
  exports.
- GitHub Actions workflow for native Tauri builds.
- PySide6 WebEngine GUI shell around the packaged HTML app.
- Python package layout under `src/arculus_recovery/`, optional GUI dependency,
  and package entry point.
- Terminal theme.
- Cross-platform Tauri asset preparation scripts for Windows, macOS, and Linux
  build hosts.
- macOS Tauri `.app` bundles and DMGs for `x86_64-apple-darwin`,
  `aarch64-apple-darwin`, and `universal-apple-darwin`.
- Linux Tauri amd64 release binary plus Debian `.deb` and RPM `.rpm` packages.

### Changed

- Current protected `.arc` export uses armored `ARCULUS-ARC-V2` text with
  PBKDF2-HMAC-SHA512, 1,000,000 iterations, 32-byte salt, 24-byte nonce,
  HMAC-SHA512 stream encryption, and HMAC-SHA512 authentication.
- ARC V2 import rejects iteration counts below 600,000.
- The v1.6.0 docs distinguish the full canonical HTML feature set from the
  narrower Python CLI compatibility surface.
- Tauri asset preparation byte-copies the canonical HTML to preserve Unicode
  seed-mask text and inline assets.
- PDF export uses the inline jsPDF bundle rather than an eval-based or remote
  loader.
- Tauri export failures are surfaced as explicit UI errors.
- Release documentation now treats checked-in `releases/` files as local build
  artifacts that require per-release hash verification.
- v1.6.0 macOS release `.app` bundles are ad-hoc signed and DMGs are generated
  from the signed app bundles.

### Fixed

- XRP QR payload formatting now uses `?dt=` with a valid separator.
- Tagless XRP QR output now appends `?dt=00000` for scanner compatibility.
- XRP QR rendering uses a dedicated 320 px renderer and wider modal sizing.
- QR canvas CSS now scales on narrow viewports without overflow.
- QR capacity selection accounts for terminator bits and removes an incorrect
  version-10 short-circuit.
- Repaired damaged inline jsPDF and stripped JavaScript conditionals in the
  beta line so standalone HTML and rebuilt Tauri apps initialize correctly.
- Preserved bullet-mask and Unicode UI text in packaged Tauri assets.
- Fixed listener accumulation around imported seed path/coin refresh behavior.
- Removed misleading XRP Taproot network metadata.
- Removed Litecoin QR URI ambiguity around Bitcoin-style `3...` addresses.
- Updated stale documentation that still described older release behavior.

### Compatibility Notes

- The canonical v1.6.0 HTML app supports Bitcoin, Bitcoin Cash, Litecoin,
  Dogecoin, Ethereum / ERC-20, Solana, Stellar, Monero, Cardano, and XRP.
- The Python CLI remains a compatibility/scripted surface for Bitcoin,
  Litecoin, Dogecoin, Ethereum, and XRP.
- Current `.arc` exports are armored ARC V2. Legacy JSON V2, Python V1,
  browser AES-GCM V1, and older PBKDF2-SHA256/XOR-HMAC import paths remain
  supported where implemented.

## [1.5.2-beta] - 2026-06-13

This was the beta stabilization line that became v1.6.0 after repair and
documentation cleanup.

### Added

- `Arculus_Recovery_Beta.html` as the validation target before promotion to the
  main HTML.
- Manual-entry seed masking after successful derivation.
- Dedicated XRP QR renderer with larger canvas and `xrp-mode` modal sizing.
- Responsive QR canvas sizing.
- PySide6 WebEngine shell replacing the older Tkinter-oriented GUI path.
- Packaged Python modules for core derivation logic, CLI handling, GUI launch,
  and HTML assets.
- Vendored and packaged jsPDF assets for offline PDF export.
- Tauri desktop build structure, native export command, capability entry, and
  injected `window.arculusTauriSaveExport` bridge.
- Windows Tauri executable, MSI, and NSIS setup artifacts.
- macOS Tauri `.app` and DMG build outputs for Apple Silicon, Intel, and
  universal packaging.

### Changed

- Embedded jsPDF directly in the HTML so raw HTML PDF export can work offline.
- Replaced a Base64/eval jsPDF loader with a raw inline script compatible with
  Tauri/WebView restrictions.
- Moved technical documentation and screenshots from `Documentation/` to
  `docs/`.
- Split Python code into package modules while keeping the root launcher.
- Updated release documentation, hash verification, and installation guidance
  for Windows, macOS, Linux, and universal macOS packages.

### Fixed

- Malformed XRP destination-tag QR URI missing the `?` separator.
- Tagless XRP QR scanner failures.
- QR version-selection capacity bug.
- Tauri/WebView PDF initialization without eval.
- Tauri native export writing silently to Downloads instead of prompting for a
  save location.
- Tauri asset-preparation mojibake and Unicode corruption.
- Damaged inline jsPDF block and stripped JavaScript conditionals after asset
  preparation.

## [1.5.0] - 2026-06-05

### Added

- BIP21/URI scheme auto-detection for QR payloads.
- Forced black-on-white QR rendering for scanner reliability.
- Four-module QR quiet zone.
- PDF key export through jsPDF, saved as `Arculus_Key_Export_<coin>.pdf`.
- PDF title block with coin, app version, UTC timestamp, and root fingerprint.
- PDF Extended Keys section and address table.
- Extended Keys output tab.
- Per-cell copy controls for address and private-key columns.
- Address Count `maxlength="15"`.
- Range input for deriving explicit `START-END` address indexes.
- Collapsible Advanced settings section.
- Opt-in Auto-Derive on settings change with 600 ms debounce.
- Expand/minimize control for the output panel.
- QR modal Edit button.

### Changed

- PDF became the default selected export format.
- PDF export removed the network label and improved coin display capitalization.
- PDF private-key column now uses WIF for UTXO coins and hex for Ethereum/XRP.
- Table View promotes Branch, Path, Address, and private-key columns.
- Table View displays key and hex fields without truncation and suppresses
  fields already shown in the Extended Keys tab or page metadata.
- XRP QR flow prompts for a destination tag/memo before rendering.
- Export option formerly labeled "Dump" was renamed to "PDF".

### Fixed

- QR matrix structural modules were no longer accidentally masked as data.
- QR mask XOR preserves boolean data-cell type.
- QR format bits are written to the correct positions.
- QR penalty scoring normalizes mixed matrix cell types.
- Imported-seed derivation info listeners are registered once at startup.
- XRP network definition no longer advertises spurious Taproot versions.
- Litecoin QR URI detection no longer claims Bitcoin-style `3...` addresses.

## [1.4.0] - 2026-06-03

### Added

- Passphrase visibility toggle with accessible show/hide labels.
- Clipboard countdown after Copy Seed.
- Five-minute inactivity auto-clear with a one-minute warning banner.
- Derived output Table View and Raw JSON tabs.
- Copy-per-row address buttons.
- Derivation progress indicator with UI yielding during large derivations.

### Changed

- Passphrase input defaults to masked password mode.
- Output area border handling was adjusted for the tabbed output wrapper.

## [1.3.0] - 2026-06-02

### Added

- QR Export modal with self-contained QR generation on canvas.
- QR PNG save and address-copy controls.
- Enter-to-generate behavior in the QR address input.
- Dark+ theme.
- Three-way Light / Dark / Dark+ theme selector.
- Clear All button.
- Derivation path tooltip for the Arculus-native `m/0'` default.

### Changed

- Show Seed moved into the seed row near other seed-state controls.
- Copy Seed and Clear All buttons were restyled to use the default button style.
- Theme preference moved to `localStorage` key `arculusTheme` with migration
  from the older `arculusDarkMode` setting.

## [1.2.0] - 2026-06-02

### Added

- Laptop/small-screen responsive breakpoint at `max-width: 1280px`.
- More compact default Python GUI geometry and widget padding.

### Changed

- 12-word mode hides word-grid slots 13 through 24.
- Mnemonic textarea default height reduced to two lines.
- Output textarea default height reduced to ten lines.
- Hidden seed mask changed from asterisks to bullet groups.
- HTML body min-height changed from `100vh` to `100dvh` for modern browser
  viewport behavior.

## [1.1.0] - 2026-06-01

### Added

- Generate Random Seed button for 12-word and 24-word BIP39 mnemonics.
- Browser mnemonic generation through `crypto.getRandomValues`.
- Python GUI mnemonic generation through `os.urandom`.
- Numbered word-entry grid replacing the original single-textarea-first input
  workflow.
- 12/24-word selector and paste distribution across word fields.
- CLI `--all-common` flag for common BIP44/BIP49/BIP84/BIP86 paths.
- CLI `--coin bitcoin|litecoin|dogecoin|ethereum|xrp`.
- CLI `--testnet` for Bitcoin testnet parameters.
- Version string surfaced in the UI and CLI.

### Changed

- Generated seeds use the hidden-seed workflow introduced for imported `.arc`
  files.
- Documentation and security guidance were updated for generation and word-grid
  entry.

## [Arculus_Recovery] - 2026-04-24

First formal GitHub release, tagged at commit `e7cc84e`.

### Added

- Ethereum / ERC-20 address derivation.
- Offline Keccak-256 and EIP-55 checksum address support.
- ERC-20 export fields noting that Ethereum tokens use the same account
  address.
- XRP classic address derivation.
- Validation output for word count, wordlist validity, entropy bits, checksum
  bits, checksum match, BIP39 compliance, root fingerprint, keystore type,
  seed format, and passphrase warning.
- Deep validation output for BIP39 512-bit seed, master private key, and master
  chain code.
- Taproot/P2TR address derivation, Bech32m encoding, BIP86 purpose detection,
  taproot internal key fields, taproot tweak, taproot output key fields, and
  output key parity.
- HTML encrypted seed workflow with Encrypt/Export Seed, Import Seed, Show
  Seed press-and-hold, and inline root fingerprint display.
- Python GUI encrypted seed workflow matching the HTML flow.
- Shared `.arc` file format for HTML/Python compatibility.

### Changed

- Imported encrypted seeds remain hidden on screen while still usable for
  validation, derivation, and export.
- Common derivation handling was extended to include `m/86'/coin'/0'`.

### Compatibility

- Added import support for older encrypted seed formats while writing the shared
  `.arc` format for current exports.

## Pre-Release History

Earlier development included:

- Initial BIP39 validation for 12-word and 24-word English mnemonics.
- BIP32 secp256k1 derivation pipeline.
- Bitcoin, Litecoin, and Dogecoin support.
- P2PKH, P2WPKH-P2SH, and P2WPKH address derivation.
- BIP44, BIP49, and BIP84 derivation path table.
- JSON, CSV, and TXT export of derived keys and addresses.
- Python CLI mode with mnemonic, derivation, script type, count, and output
  format flags.
- Python desktop GUI launch through `--gui`.
- Original dark mode toggle.
- SHA-256 hash verification guidance.
- Initial security, contribution, license, and screenshot documentation.
