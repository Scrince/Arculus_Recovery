# Changelog — Arculus Recovery

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

Changes on `main` not yet tagged in a formal release.

---

## [1.2.0-production] — 2026-06-02

### Added

**Laptop / Small-Screen Layout (HTML)**
- New responsive breakpoint at `max-width: 1280px` (above the existing 980px collapse point) applies compact spacing without switching to single-column layout.
- At the laptop breakpoint: body and card padding reduced (20px → 8px / 16px → 10px), label column narrowed (260px → 180px), font sizes tightened (14px → 13px), button and input padding reduced, and word-grid gap tightened.

**Compact Default Sizing (Python GUI)**
- Default window geometry reduced from `1120×860` to `1040×760` to open comfortably on 13" screens without immediately hitting the minimum size constraint.
- Minimum window size reduced from `980×760` to `860×640`.
- `TButton` padding reduced from `(12, 8)` to `(8, 5)`; `TEntry` and `TCombobox` vertical padding reduced from `6` to `4`.

### Changed

**Word Grid — 12-Word Mode Hides Slots 13–24 (HTML & Python GUI)**
- Word entry cells 13–24 are now hidden when 12-word mode is active, cutting the numbered-words section roughly in half for the common case.
- Cells reappear immediately when the user switches to 24-word mode or pastes a 24-word mnemonic.
- In the HTML version, cells toggle via `display: none` inside `refreshWordEnabled()`. In the Python GUI, cells toggle via `grid_remove()` / `grid()` inside `on_seed_length_change()`.

**Mnemonic Textarea — Reduced Default Height (HTML & Python GUI)**
- Default height reduced from 4 lines (`min-height: 96px`) to 2 lines (`min-height: 60px`). The field remains user-resizable.

**Output Textarea — Reduced Default Height (HTML & Python GUI)**
- Default height reduced from 20 lines (`min-height: 280px`) to 10 lines (`min-height: 120px`). The field remains user-resizable, allowing expansion when reviewing full derivation output.

**Seed Mask Character Changed from Asterisks to Bullets (HTML & Python GUI)**
- The masking character used to obscure hidden seed words changed from `****` to `••••` in both the mnemonic textarea and the numbered word entries.
- Applies to both imported `.arc` seeds and generated seeds while in protected (hidden) state.

**`min-height: 100dvh` (HTML)**
- Replaced `100vh` with `100dvh` so macOS Safari correctly accounts for browser chrome height, preventing subtle overflow on 13" MacBook displays.

---

## [1.1.0-production] — 2026-06-01

### Added

**Generate Random Seed (HTML & Python GUI)**
- `Generate Random Seed` button produces a cryptographically random 12-word or 24-word BIP39 mnemonic using `crypto.getRandomValues` in the browser and `os.urandom` in Python.
- Generated seeds use the same hidden-seed workflow as imported `.arc` seeds: the phrase is kept out of the visible text box and is held in protected state until the user holds `Show Seed`.
- The inline root fingerprint display updates immediately after generation.

**Individual Word-Entry Grid (HTML & Python GUI)**
- The mnemonic input is now a numbered grid of individual word fields rather than a single text box, matching a common hardware wallet recovery UX.
- A 12/24-word radio selector controls which fields are active; switching automatically clears the inactive slots.
- Pasting a full mnemonic string into any field auto-distributes the words across the grid.

**`--all-common` CLI Flag (Python)**
- `--all-common` derives all applicable standard account paths for the selected coin in a single run: `m/44'/coin'/0'`, `m/49'/coin'/0'`, `m/84'/coin'/0'`, and `m/86'/coin'/0'`.
- For Ethereum and XRP, `--all-common` is a no-op because those coins use a single canonical derivation path.

**`--coin` CLI Flag (Python)**
- Explicit coin selection in CLI mode via `--coin bitcoin|litecoin|dogecoin|ethereum|xrp`.

**`--testnet` CLI Flag (Python)**
- Enables testnet network parameters for Bitcoin CLI derivation.

**Version Identifier**
- Both the HTML and Python versions now surface a version string (`v1.1.0-production`) in the UI and via `--version` on the CLI.

### Changed

- Updated README, security guidance, contribution checklist, and threat model to reflect the generate-seed workflow and word-grid input.
- Default mnemonic input mode is now the word grid; the previous single-textarea input is removed.

---

## [Arculus_Recovery] — 2026-04-24

Tagged release commit `e7cc84e`. This is the first formal GitHub release and represents a significant feature expansion over the initial commits.

### Added

**Ethereum / ERC-20 and XRP support**
- Ethereum / ERC-20 address derivation (HTML tool, Python GUI, Python CLI)
- Offline Keccak-256 and EIP-55 checksum address support for Ethereum addresses
- ERC-20 export fields clarifying that Ethereum token balances use the same derived account address
- XRP classic address derivation (HTML tool, Python GUI, Python CLI)

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

The project now uses a `major.minor.patch-channel` version string (`1.2.0-production`), surfaced in the UI title bar and via `--version` on the CLI. The README includes SHA256 hashes for `Arculus_Recovery.html`, `index.html`, and `Arculus_Recovery.py` so users can verify the exact file state they are running, independent of the version string.
