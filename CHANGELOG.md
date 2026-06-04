# Changelog — Arculus Recovery

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

Changes on `main` not yet tagged in a formal release.

### Added

**PDF Key Export (HTML)**
- New `PDF` option in the Export format selector triggers a full key export as a landscape A4 PDF via jsPDF (loaded on demand from cdnjs; no network required unless PDF export is actually used).
- Page 1 opens with a title block ("Arculus Key Export"), a meta line showing coin, app version, UTC timestamp, and root fingerprint, followed by an **Extended Keys** section and then the address table.
- Extended Keys section lists all present root and account extended keys (xprv, xpub, zprv, zpub, yprv, ypub, trprv, trpub) vertically in order — label on the left, full value spanning the remaining page width — separated from the address table by a horizontal rule.
- Address table columns: Branch, Path, Address, and the appropriate private key column — Private Key WIF for UTXO coins (Bitcoin, Litecoin, Dogecoin) or Private Key Hex for Ethereum and XRP. Branch values are colour-coded (green for receiving, grey for change). Rows use alternating background shading.
- Continuation pages repeat the title/meta block and table header without the extended keys section.
- File saved as `Arculus_Key_Export_<coin>.pdf`.

**Extended Keys Tab (HTML)**
- A third output tab, "Extended Keys", added after "Raw JSON".
- Displays all present root and account extended keys for the most recent derivation run, in a two-group layout (root / account) separated by a divider, each entry with an individual copy button (⧉).
- Tab content is populated when derivation completes and cleared when output is reset.

**Per-Cell Copy Buttons for Address and WIF (HTML)**
- Address and Private Key WIF cells in the Table View each include an inline ⧉ copy button that copies the cell value to the clipboard with a brief ✓ confirmation.

### Changed

**PDF Export — Root Fingerprint in Meta Line (HTML)**
- The root fingerprint is now displayed inline on the PDF meta line (after the UTC timestamp) using the same `·` separator style as the other meta fields, making it easy to identify which account was exported at a glance.
- The fingerprint is sourced from the live root fingerprint display and omitted gracefully if unavailable.
- Previously the fingerprint appeared on a dedicated second line below the meta row; that line has been removed.

**PDF Export — Network Identifier Removed (HTML)**
- The network name (e.g. "Mainnet") is no longer included in the PDF meta line.

**PDF Export — Coin Name Capitalization (HTML)**
- Coin names in the PDF header now use proper display capitalization: `Bitcoin`, `Ethereum`, `Litecoin`, `Dogecoin`, `XRP`. Previously the raw internal identifier (e.g. `bitcoin`) was used.

**PDF Export — Default Format (HTML)**
- `PDF` is now the pre-selected option in the Export format dropdown. Previously `JSON` was the default.

**Table View — Column Ordering (HTML)**
- Address and Private Key WIF columns are now promoted to appear before all other data columns.
- Branch and Path columns precede Address and Private Key WIF.

**Table View — No Truncation on Hex and Key Columns (HTML)**
- `public_key_hex`, `private_key_hex`, and all taproot and Ethereum hex variant columns (`ethereum_public_key_hex`, `taproot_internal_public_key_hex`, `taproot_internal_private_key_hex`, `taproot_output_public_key_hex`, `taproot_output_private_key_hex`, `taproot_tweak_hex`) now display in full with an inline ⧉ copy button, matching the behavior of Address and Private Key WIF. Previously they were truncated at 260 px with an ellipsis.
- Address and Private Key WIF cells no longer apply `max-width` / `text-overflow` truncation; they display in full.

**Table View — Suppressed Columns (HTML)**
- The following fields are no longer rendered as table columns, as they are surfaced elsewhere (Extended Keys tab or page header): `root_xprv`, `root_xpub`, `root_zprv`, `root_zpub`, `root_yprv`, `root_ypub`, `root_trprv`, `root_trpub`, `account_xprv`, `account_xpub`, `account_zprv`, `account_zpub`, `account_yprv`, `account_ypub`, `account_trprv`, `account_trpub`, `network`, `word_count`, `derivation`, `account_script_type_used`, `coin`.

**PDF Export — Coin-Appropriate Private Key Column (HTML)**
- For Ethereum and XRP exports the PDF address table now shows a **Private Key Hex** column in place of Private Key WIF, since WIF encoding does not apply to those coins. UTXO coins (Bitcoin, Litecoin, Dogecoin) continue to use Private Key WIF. The column header updates accordingly.

**Export Format Selector — Renamed PDF Option (HTML)**
- The export option previously labelled "Dump" is now labelled "PDF".

---

## [1.4.0-production] — 2026-06-03

### Added

**Passphrase Visibility Toggle (HTML)**
- The passphrase field now defaults to `type="password"` so the value is masked by default.
- An eye-icon button placed inside the field's right edge toggles between masked and plain-text display.
- Button label and `aria-label` update to reflect current state ("Show passphrase" / "Hide passphrase").

**Clipboard Auto-Clear (HTML)**
- After copying a seed phrase via the Copy Seed button, the clipboard is automatically overwritten with an empty string after 60 seconds.
- A live countdown badge appears inline beside the status message, ticking down each second and disappearing when the clipboard is cleared.

**Inactivity Auto-Clear (HTML)**
- A 5-minute idle timer watches for mouse, keyboard, touch, and scroll events across the page.
- At 4 minutes of inactivity a warning banner appears at the top of the app: "Idle timeout in 60 seconds. All fields will be cleared."
- At 5 minutes all seed fields, the passphrase, the output area, and any in-memory seed state are cleared automatically, matching the behavior of the existing Clear All button.
- Any user interaction resets the timer and dismisses the warning banner.

**Derived Output Table View (HTML)**
- After a successful "Derive Keys + Addresses" run, the output area switches to a tabbed interface with two views: **Table View** and **Raw JSON**.
- Table View renders a sticky-header scrollable table with one row per derived address. Each column is auto-sized and truncated with an ellipsis for long values; hovering a cell shows the full value via the native `title` attribute.
- Null-only columns are suppressed from the table automatically.
- The branch column renders color-coded badges (green for receiving, gray for change) for quick visual scanning.
- Raw JSON remains accessible via the Raw JSON tab and is unchanged from previous behavior.
- The tab strip is hidden when the output panel shows validation results or is empty, and is cleared when Clear All is triggered.

**Copy-per-Row Address Buttons (HTML)**
- Each row in the Table View includes a "Copy" button in the first column that copies that row's address to the clipboard with a 1.5-second "Copied!" confirmation.

**Derivation Progress Indicator (HTML)**
- A thin progress bar appears below the status line when "Derive Keys + Addresses" is clicked.
- Progress advances from 5 % at start through proportional increments as each address is derived (10–90 %) to 100 % on completion, then hides after 400 ms.
- The UI thread is yielded every 3 addresses so the bar animates smoothly during large derivation runs.
- Progress bar accent color follows the active theme (blue for Light/Dark, orange for Dark+).

### Changed

**Version bump (HTML)**
- `APP_VERSION` and the title-bar badge updated from `1.3.0-production` to `1.4.0-production`.

**Passphrase Field Default Type (HTML)**
- Changed from `type="text"` to `type="password"` so the value is hidden on load. The visibility toggle restores previous behavior when needed.

**Output Area Border (HTML)**
- When the output tab strip is shown, the output `<textarea>` border is managed by the wrapping `#outputWrap` container so that the top edge aligns cleanly with the active tab.

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
