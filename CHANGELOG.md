# Changelog — Arculus Recovery

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

Changes on `main` not yet tagged in a formal release.

---

## [1.3.0-production] — 2026-06-02

### Added

**QR Export (HTML)**
- New `QR Export` button in the action toolbar opens a modal for generating QR codes from any address.
- The modal accepts a manually pasted address rather than auto-selecting from derived output, keeping the workflow explicit and independent of derivation state.
- QR codes render on an inline `<canvas>` element using a fully self-contained Reed-Solomon + QR matrix encoder with no external dependencies.
- Supports addresses of any length up to QR version 10 capacity; automatically selects the smallest version and best mask pattern.
- Error correction level M is used by default, escalating to Q for longer inputs.
- In Dark+ mode the QR renders with the Claude orange-on-dark-gray palette.
- Save PNG downloads the canvas as a named image file.
- Copy Address copies the pasted address to the clipboard with a brief confirmation.
- Enter key in the address input triggers generation without clicking Generate.

**Dark+ Theme (HTML)**
- New third theme option alongside Light and Dark, named `Dark+`.
- Uses Claude's design language: near-black backgrounds (`#1a1a1a` / `#222222`), warm gray text, and `#e86926` orange as the accent color.
- Orange accent applies to focus rings, the online network indicator dot, valid status messages, checked toggles, and primary buttons.
- Theme selection is persisted to `localStorage` under the `arculusTheme` key.
- Existing `arculusDarkMode` preference is automatically migrated on first load.

**Theme Selector (HTML)**
- Settings panel Dark Mode checkbox replaced with a three-way Light / Dark / Dark+ radio selector labeled "Theme".

**Clear All Button (HTML)**
- New `Clear All` button in the seed row (between `Show Seed` and `Generate Random Seed`) wipes all mnemonic fields, the passphrase field, the output area, and the root fingerprint display in one action.
- Also clears any imported or generated seed held in protected memory.
- Shows "All fields cleared." in the status bar on completion.

**Derivation Path Tooltip (HTML)**
- An info icon appears beside the Derivation Path label when the path is `m/0'` (the Arculus-native default), explaining why it differs from the standard BIP-44 convention and how to adjust it when recovering from a third-party wallet.
- The icon is hidden automatically whenever the user changes the path to anything other than `m/0'`, and reappears if the path is changed back.
- The icon also responds to coin selector changes: switching to a coin whose default path is not `m/0'` hides it immediately.

### Changed

**Show Seed Button Position (HTML)**
- `Show Seed` moved from the bottom action bar into the seed row, positioned between `Generate Random Seed` and `Clear All` for logical proximity to the other seed-state controls.

**Button Colors (HTML)**
- Removed the red background from the `Copy Seed` button; it now uses the default button style.
- Removed the amber background from the `Clear All` button; it now uses the default button style.

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
- Default height reduced from 20 lines (`min-height: 280px`) to 10 lines (`min-height: 120px`). The field remains user-resizable.

**Seed Mask Character Changed from Asterisks to Bullets (HTML & Python GUI)**
- The masking character used to obscure hidden seed words changed from `****` to `••••` in both the mnemonic textarea and the numbered word entries.

**`min-height: 100dvh` (HTML)**
- Replaced `100vh` with `100dvh` so macOS Safari correctly accounts for browser chrome height.

---

## [1.1.0-production] — 2026-06-01

### Added

**Generate Random Seed (HTML & Python GUI)**
- `Generate Random Seed` button produces a cryptographically random 12-word or 24-word BIP39 mnemonic using `crypto.getRandomValues` in the browser and `os.urandom` in Python.
- Generated seeds use the same hidden-seed workflow as imported `.arc` seeds.
- The inline root fingerprint display updates immediately after generation.

**Individual Word-Entry Grid (HTML & Python GUI)**
- The mnemonic input is now a numbered grid of individual word fields rather than a single text box, matching a common hardware wallet recovery UX.
- A 12/24-word radio selector controls which fields are active; switching automatically clears the inactive slots.
- Pasting a full mnemonic string into any field auto-distributes the words across the grid.

**`--all-common` CLI Flag (Python)**
- Derives all applicable standard account paths for the selected coin in a single run.

**`--coin` CLI Flag (Python)**
- Explicit coin selection in CLI mode via `--coin bitcoin|litecoin|dogecoin|ethereum|xrp`.

**`--testnet` CLI Flag (Python)**
- Enables testnet network parameters for Bitcoin CLI derivation.

**Version Identifier**
- Both the HTML and Python versions now surface a version string in the UI and via `--version` on the CLI.

### Changed

- Updated README, security guidance, contribution checklist, and threat model to reflect the generate-seed workflow and word-grid input.
- Default mnemonic input mode is now the word grid; the previous single-textarea input is removed.

---

## [Arculus_Recovery] — 2026-04-24

Tagged release commit `e7cc84e`. First formal GitHub release.

### Added

**Ethereum / ERC-20 and XRP support**
- Ethereum / ERC-20 address derivation with offline Keccak-256 and EIP-55 checksum address support.
- XRP classic address derivation.

**Validation output (HTML & Python)**
- Word count, wordlist validity, entropy bits, checksum bits, checksum match, BIP-39 compliance, root fingerprint, keystore type detection, seed format detection, passphrase warning, BIP-39 seed (512-bit), master private key, and master chain code.

**Taproot (P2TR) support (HTML & Python)**
- P2TR address derivation, Bech32m encoding, BIP86 purpose detection, taproot internal/output key fields, tweak field, and output key parity.

**Encrypted seed workflow (HTML & Python GUI)**
- `Encrypt/Export Seed`, `Import Seed`, and `Show Seed` press-and-hold actions.
- Inline root fingerprint display beside the `Show Seed` button.
- Shared `.arc` file format for cross-compatibility between HTML and Python versions.

### Changed

- Standardized encrypted seed export/import to the shared `.arc` file format.
- Updated imported-seed behavior so encrypted seeds remain hidden on screen while still usable for validation and derivation.
- Extended common derivation handling to include `m/86'/coin'/0'` (Taproot/BIP86).

### Compatibility

- Added support for reading older encrypted seed formats.

---

## Pre-Release History

### Earlier work included:

- Initial BIP39 mnemonic validation for 12-word and 24-word seeds (HTML and Python)
- BIP32 key derivation pipeline
- Address derivation for P2PKH, P2WPKH-P2SH, and P2WPKH
- Multi-coin support: Bitcoin, Litecoin, Dogecoin
- Derivation path table covering BIP44, BIP49, and BIP84 purposes
- Export of derived keys and addresses in JSON, CSV, and TXT formats
- Python CLI mode
- Python desktop GUI via `--gui` flag
- Dark mode toggle in HTML settings dialog and Python settings popup
- SHA256 hash verification instructions in the README
- `SECURITY.md`, `CONTRIBUTING.md`, and `LICENSE.md`
- Documentation screenshots

---

## Notes on Versioning

The project uses a `major.minor.patch-channel` version string (e.g. `1.3.0-production`), surfaced in the UI title bar and via `--version` on the CLI. The README includes SHA256 hashes for `Arculus_Recovery.html` and `Arculus_Recovery.py` so users can verify the exact file state they are running, independent of the version string.
