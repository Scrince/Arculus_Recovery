# Changelog ? Arculus Recovery

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

Changes on `main` not yet tagged in a formal release.

### Changed

**Beta Build**
- Renamed the next-release working build to `Arculus_Recovery_Beta.html` and documented it as the Beta validation target before promotion to the main HTML.

### Fixed

**XRP QR Code — Missing `?` in Destination Tag URI (`Arculus_Recovery_Beta.html`)**
- The original `toBip21Uri()` produced `rADDRESS dt=NNNN` (no `?`) for tagged XRP addresses, making the URI malformed and causing scanner failures. Fixed by inserting the missing `?` separator.

**XRP QR Code — Tagless Addresses Not Resolving (`Arculus_Recovery_Beta.html`)**
- A bare `rADDRESS` with no query string gave wallet scanners no signal to identify the payload as XRP, causing silent resolution failures. Tagless XRP QR codes now always append `?dt=00000` as a dummy destination tag, matching the format scanners expect without affecting transaction routing.

### Added

**XRP QR Code — Dedicated `renderXrpQr()` Function (`Arculus_Recovery_Beta.html`)**
- Extracted XRP QR rendering into a dedicated function that renders at 320 px (vs 256 px for other coins) with a 4-module quiet zone for improved decode reliability. XRP addresses are now detected and routed to this renderer before the generic `toBip21Uri()` path runs.

**XRP QR Code — `xrp-mode` Modal Widening (`Arculus_Recovery_Beta.html`)**
- When displaying an XRP QR, the modal widens to `min(400px, calc(100vw - 40px))` to accommodate the larger 320 px canvas. The `xrp-mode` class is correctly removed on reset so the wider sizing does not persist after closing.

**QR Canvas — Responsive Sizing CSS (`Arculus_Recovery_Beta.html`)**
- Added `max-width: 100%; height: auto` to `#qrCanvas` so the canvas scales correctly on narrow viewports without overflow.

**QR Code Generator — Capacity Calculation Fix (`Arculus_Recovery_Beta.html`)**
- The version-selection loop now correctly accounts for terminator bits (`+4`) before rounding up to whole codewords, and removes a hardcoded `v===10` short-circuit that could cause incorrect QR version selection for certain payload lengths.

**Python GUI - PySide6 HTML Shell**
- Replaced the legacy Tkinter GUI with a PySide6 WebEngine desktop shell that loads the canonical `Arculus_Recovery.html` interface unchanged.
- Kept CLI derivation mode available through `Arculus_Recovery.py` and added package entry points under `src/arculus_recovery/`.
- Added Python packaging metadata, an optional `gui` extra, and `requirements.txt` with the new PySide6 dependency.
- Added vendored and packaged jsPDF assets, with optional PySide6 page injection retained as a fallback for older HTML assets.
- Updated the PySide6 save dialog so PDF exports default to the `PDF Files (*.pdf)` filter and append `.pdf` when omitted.
- Embedded jsPDF directly into `Arculus_Recovery.html`, allowing raw HTML PDF export to work offline with no external files or network access.
- Replaced the Base64/eval jsPDF loader with a preserved raw inline script so Tauri/WebView can initialize PDF export without eval.

**Repository Layout**
- Moved technical documentation and screenshots from `Documentation/` to `docs/`.
- Split the Python code into core derivation logic, CLI handling, GUI launcher modules, and packaged GUI assets while keeping the root compatibility script.

### Added

**Tauri Desktop Builds**
- Added a Tauri v2 wrapper that packages the canonical HTML app as a native desktop application.
- Added a Windows Tauri build output, including standalone `.exe`, NSIS setup `.exe`, and MSI installer artifacts.
- Added a GitHub Actions workflow to build Windows, macOS, and Linux Tauri artifacts on native runners.
- Kept a Tauri download handler fallback for browser-style downloads.
- Added a Tauri native save command for PDF, JSON, CSV, TXT, encrypted seed, and QR exports so blob downloads no longer depend on WebView download behavior.
- Added an explicit Tauri v2 capability for the main window and bundled export save command so desktop exports can invoke native file writing reliably.
- Added an injected Tauri export bridge (`window.arculusTauriSaveExport`) so the packaged WebView can call the native save command without depending on the global Tauri JavaScript object.
- Hardened the HTML export path so native Tauri save failures are shown as explicit UI errors instead of being hidden by browser-style blob download fallback.
- Added a Terminal theme to the HTML and PySide6-rendered GUI, using a black terminal surface, neon text colors, and a monospace font stack.
- Updated the generated Tauri HTML copy to use the inline jsPDF bundle for offline PDF export.
- Fixed Tauri asset preparation to preserve bullet-mask and Unicode UI text in the packaged app.
- Changed Tauri asset preparation to byte-copy the canonical HTML and repaired mojibake in the HTML/docs so Unicode UI text renders correctly in the packaged app.
- Restored the damaged inline jsPDF block and repaired stripped JavaScript conditionals so the standalone HTML and rebuilt Tauri app initialize correctly again.
- Rebuilt and refreshed the Windows Tauri executable, MSI installer, and NSIS setup artifacts after the HTML repair.
- Updated the Tauri native export command to open a Save dialog for PDF, JSON, CSV, TXT, encrypted seed, and QR exports instead of silently writing to Downloads.
- Added macOS Tauri release artifacts for Apple Silicon, Intel x64, and universal builds, including verified DMGs and ad-hoc signed `.app` bundles.
- Added cross-platform Python Tauri asset preparation for macOS and Linux build hosts without modifying the canonical HTML application.
- Updated release documentation, hash verification, and installation guidance for Windows, macOS, Linux, and universal macOS packages.

---

## [1.5.0] - 2026-06-05

### Added

**QR Code - BIP21 / URI Scheme Auto-Detection (HTML)**
- A new `toBip21Uri()` function inspects the pasted address before encoding and prepends the correct URI scheme automatically, producing the format that wallet apps expect to scan rather than a bare address string.
- Detection rules: `bc1?` / `1?` / `3?` -> `bitcoin:`, `ltc1?` / `L?` / `M?` -> `litecoin:`, `D?` / `A?` -> `dogecoin:`, `0x?` (40 hex chars) -> `ethereum:`. XRP classic addresses (`r?`) are encoded as bare addresses with no scheme prefix, which is the safest cross-wallet approach; `xrp:` is not a recognised standard and `xrpl:` (XLS-7d) has inconsistent wallet support.
- Addresses that already carry a scheme (e.g. manually typed `bitcoin:?`) are passed through unchanged.
- The address label displayed beneath the QR canvas shows the full URI so the user can verify exactly what was encoded.

**QR Code - Forced Black-on-White Rendering (HTML)**
- QR codes now always render with a `#000000` foreground on a `#ffffff` background regardless of the active theme.
- Previously, Dark+ mode rendered an orange-on-dark-gray QR (`#e86926` / `#1a1a1a`) which caused silent scan failures on many wallet camera decoders tuned for high-contrast black-on-white.

**QR Code - Increased Quiet Zone (HTML)**
- The quiet zone around the QR matrix increased from 3 modules to 4 modules, matching the minimum recommended by the QR specification and improving decode reliability on scanners that crop near the canvas edge.

### Fixed

**QR Code Generator - Structural Module Type Collision (HTML)**
- The original `makeMatrix()` used JavaScript `true`/`false` for finder patterns, timing strips, alignment patterns, and the dark module. Since `applyMask()` identified data modules by checking `typeof cell === 'boolean'`, structural cells were incorrectly masked, corrupting the QR matrix.
- Fixed by using integer `1`/`0` for all structural modules and reserving `boolean` values exclusively for data and error-correction modules.

**QR Code Generator - `applyMask()` XOR on Booleans (HTML)**
- `out[r][c] ^= fn(r,c)` on a boolean operand produces an integer (`0` or `1`), not a boolean, silently breaking all subsequent `=== true` / `=== false` comparisons downstream.
- Fixed by replacing the XOR with `out[r][c] = out[r][c] !== fn(r,c)`, which preserves the boolean type.

**QR Code Generator - `writeFormat()` Incorrect Bit Placement (HTML)**
- The original `writeFormat()` contained a redundant loop that overwrote already-written bits and missed several of the 15 format bit positions specified by the QR standard, producing unreadable format information strips.
- Rewritten to place all 15 format bits at their exact positions on both the top-left and top-right / bottom-left copy strips.

**QR Code Generator - `penaltyScore()` Mixed-Type Comparisons (HTML)**
- With the previous mixed `true`/`false`/`1`/`0` cell types, `m[r][c] === m[r][c-1]` cross-type comparisons always returned `false`, making the penalty scorer unable to detect runs of identical modules and causing suboptimal mask selection.
- Fixed by normalising all cell values through a `val(r,c) => !!m[r][c]` helper before comparison.

**Listener Leak in `applyImportedSeed()` (HTML)**
- `applyImportedSeed()` registered new `input` and `change` listeners on the derivation path field and coin selector, plus a `DOMContentLoaded` listener on `window`, every time it was called. Importing multiple seeds in one session accumulated unbounded duplicate listeners.
- The `refreshDerivationInfoIcon` helper and its two event listeners have been moved to `bindUI()` where they are registered exactly once at startup.

**XRP Network Definition - Spurious Taproot Versions (HTML)**
- The XRP network object incorrectly included a `p2tr` entry with Bitcoin xprv/xpub version bytes. XRP Ledger does not use Taproot. While this caused no runtime error (the script type for XRP is always `'xrp'`), it was misleading and inconsistent with the Dogecoin entry which correctly sets `p2tr: null`.
- Fixed by setting `p2tr: null` in the XRP network definition.

**Litecoin URI Regex - Ambiguous `3?` Prefix (HTML)**
- The Litecoin branch in `toBip21Uri()` matched addresses starting with `3`, which is the Bitcoin P2SH prefix, not Litecoin. Litecoin P2SH addresses use an `M` prefix. The `3` branch was unreachable in practice (the Bitcoin rule above it fires first) but has been removed to eliminate the ambiguity.

### Added

**PDF Key Export (HTML)**
- New `PDF` option in the Export format selector triggers a full key export as a landscape A4 PDF via jsPDF.
- Page 1 opens with a title block ("Arculus Key Export"), a meta line showing coin, app version, UTC timestamp, and root fingerprint, followed by an **Extended Keys** section and then the address table.
- Extended Keys section lists all present root and account extended keys (xprv, xpub, zprv, zpub, yprv, ypub, trprv, trpub) vertically in order a label on the left, full value spanning the remaining page width ? separated from the address table by a horizontal rule.
- Address table columns: Branch, Path, Address, and the appropriate private key column ? Private Key WIF for UTXO coins (Bitcoin, Litecoin, Dogecoin) or Private Key Hex for Ethereum and XRP. Branch values are colour-coded (green for receiving, grey for change). Rows use alternating background shading.
- Continuation pages repeat the title/meta block and table header without the extended keys section.
- File saved as `Arculus_Key_Export_<coin>.pdf`.

**Extended Keys Tab (HTML)**
- A third output tab, "Extended Keys", added after "Raw JSON".
- Displays all present root and account extended keys for the most recent derivation run, in a two-group layout (root / account) separated by a divider, each entry with an individual copy button (?).
- Tab content is populated when derivation completes and cleared when output is reset.

**Per-Cell Copy Buttons for Address and WIF (HTML)**
- Address and Private Key WIF cells in the Table View each include an inline copy button that copies the cell value to the clipboard with a brief copied confirmation.

### Changed

**PDF Export - Root Fingerprint in Meta Line (HTML)**
- The root fingerprint is now displayed inline on the PDF meta line (after the UTC timestamp) using the same `?` separator style as the other meta fields, making it easy to identify which account was exported at a glance.
- The fingerprint is sourced from the live root fingerprint display and omitted gracefully if unavailable.
- Previously the fingerprint appeared on a dedicated second line below the meta row; that line has been removed.

**PDF Export - Network Identifier Removed (HTML)**
- The network name (e.g. "Mainnet") is no longer included in the PDF meta line.

**PDF Export - Coin Name Capitalization (HTML)**
- Coin names in the PDF header now use proper display capitalization: `Bitcoin`, `Ethereum`, `Litecoin`, `Dogecoin`, `XRP`. Previously the raw internal identifier (e.g. `bitcoin`) was used.

**PDF Export - Default Format (HTML)**
- `PDF` is now the pre-selected option in the Export format dropdown. Previously `JSON` was the default.

**Table View - Column Ordering (HTML)**
- Address and Private Key WIF columns are now promoted to appear before all other data columns.
- Branch and Path columns precede Address and Private Key WIF.

**Table View - No Truncation on Hex and Key Columns (HTML)**
- `public_key_hex`, `private_key_hex`, and all taproot and Ethereum hex variant columns (`ethereum_public_key_hex`, `taproot_internal_public_key_hex`, `taproot_internal_private_key_hex`, `taproot_output_public_key_hex`, `taproot_output_private_key_hex`, `taproot_tweak_hex`) now display in full with an inline copy button, matching the behavior of Address and Private Key WIF. Previously they were truncated at 260 px with an ellipsis.
- Address and Private Key WIF cells no longer apply `max-width` / `text-overflow` truncation; they display in full.

**Table View - Suppressed Columns (HTML)**
- The following fields are no longer rendered as table columns, as they are surfaced elsewhere (Extended Keys tab or page header): `root_xprv`, `root_xpub`, `root_zprv`, `root_zpub`, `root_yprv`, `root_ypub`, `root_trprv`, `root_trpub`, `account_xprv`, `account_xpub`, `account_zprv`, `account_zpub`, `account_yprv`, `account_ypub`, `account_trprv`, `account_trpub`, `network`, `word_count`, `derivation`, `account_script_type_used`, `coin`.

**PDF Export - Coin-Appropriate Private Key Column (HTML)**
- For Ethereum and XRP exports the PDF address table now shows a **Private Key Hex** column in place of Private Key WIF, since WIF encoding does not apply to those coins. UTXO coins (Bitcoin, Litecoin, Dogecoin) continue to use Private Key WIF. The column header updates accordingly.

**Export Format Selector - Renamed PDF Option (HTML)**
- The export option previously labelled "Dump" is now labelled "PDF".

**QR Code - XRP Destination Tag / Memo Prompt (HTML)**
- Generating a QR code for an XRP address now triggers a two-step flow instead of rendering immediately.
- After clicking **Generate** (or pressing Enter), a prompt appears explaining what a destination tag is and when exchanges such as Robinhood require one. The user can enter a numeric tag and click **Generate QR**, or click **Skip - No Tag** to encode the bare address without a tag.
- When a tag is provided the QR encodes `rADDRESSdt=TAGNUMBER`, the `dt=` query parameter format recognised by Robinhood, Coinbase, Binance, and XUMM/Xaman. When skipped, the bare `rADDRESS` is encoded as before.
- The same prompt appears when the row QR button is clicked directly from a table row for an XRP address, keeping both entry points consistent.
- All non-XRP coins (Bitcoin, Ethereum, Litecoin, Dogecoin) are unaffected; their QR codes continue to render immediately on Generate with no extra step.
- A new `isXrpAddress()` helper and `resetQrOutput()` utility have been extracted from the QR UI logic to support the two-step flow cleanly and avoid duplicated state-reset code.

**Address Count - 15-Character Input Limit (HTML)**
- The Address Count input is now capped at `maxlength="15"` characters.

**Address Count - Range Input (HTML)**
- A **Range** label and accompanying text input (max 20 characters) have been added inline to the right of the Address Count field.
- Entering a range in `START-END` format (e.g. `100-200`) causes the Derive Keys + Addresses button to derive addresses starting at the `START` index and ending at the `END` index on the active derivation path.
- The Path column in the output table reflects the actual child indices derived (e.g. `m/84'/0'/0'/0/100` through `m/84'/0'/0'/0/200`), not a loop counter starting from zero.
- When the Range input is active the Address Count box is blanked, disabled, and dimmed to 40% opacity to make it clear it is not in use. The last manually entered count value is saved and restored automatically when the Range input is cleared.
- If the Range input is empty the tool falls back to the Address Count value, deriving from index `0` as before.
- The Range label uses the same `font-weight: 600` style as the Address Count label for visual consistency.

**Settings - Advanced Section (HTML)**
- A collapsible **Advanced** section has been added at the bottom of the Settings dialog, below the Theme row.
- The section is collapsed by default and toggled open by clicking the **Advanced** heading, which displays a collapsed chevron that rotates when expanded. The `aria-expanded` attribute updates accordingly for accessibility.
- Keeping it collapsed by default avoids cluttering the settings for users who do not need these options.

**Settings - Auto-Derive on Settings Change (HTML)**
- An **Auto-Derive on Settings Change** toggle has been added inside the Advanced section of Settings.
- When enabled, changing the Coin, Script Type, Derivation Path, Address Count, or Range field after an initial derive has run automatically triggers a re-derive after a 600 ms debounce, keeping the output in sync without requiring a manual button press.
- The toggle is **off by default**, making the feature strictly opt-in. When off, `scheduleAutoderive()` exits immediately without scheduling any work.
- The toggle uses the same `.toggle` / `.toggle-track` component already used elsewhere in the UI for visual consistency.
- The status bar shows "Re-deriving?" while the automatic derive is in progress, and reverts to "Derivation complete." on success or an error message on failure, identical to a manual derive.

**Output Panel - Expand / Minimize (HTML)**
- A **? Expand** button has been added as a fourth item in the output tab bar, positioned at the far right and visually distinguished from the three content tabs with a transparent border and muted colour.
- Clicking it expands the output panel to fill the full viewport: the tab bar fixes to the top of the screen and the content area stretches to fill everything below it, with a solid backdrop covering the rest of the page.
- The button label and title change to **? Minimize** while expanded. Clicking it again restores the panel to its normal inline position.
- All three content tabs (Table View, Raw JSON, Extended Keys) remain fully switchable while the panel is expanded.
- In expanded state, `max-height` is removed from the Table View so it uses the full available height rather than being capped at 420 px; the Raw JSON textarea and Extended Keys pane also stretch to fill the viewport.
- Three ways to minimize: clicking **? Minimize**, clicking the backdrop, or pressing **Escape**. All three restore normal page scroll.
- Page scroll is locked (`overflow: hidden` on `<body>`) while the panel is expanded to prevent the underlying content from scrolling behind it.

**QR Modal - Edit Button (HTML)**
- A **Edit** button has been added alongside Save PNG and Copy Address in the QR actions row, visible after a QR code has been generated.
- Clicking it collapses back to the appropriate input step without closing the modal or clearing any values: for XRP addresses it returns to the destination tag prompt with focus on the memo field; for all other addresses it restores focus to the address input.
- This allows the user to adjust the address or memo and regenerate without re-pasting or reopening the modal.

---

---

## [1.4.0] - 2026-06-03

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
- Progress advances from 5 % at start through proportional increments as each address is derived (10?90 %) to 100 % on completion, then hides after 400 ms.
- The UI thread is yielded every 3 addresses so the bar animates smoothly during large derivation runs.
- Progress bar accent color follows the active theme (blue for Light/Dark, orange for Dark+).

### Changed

**Version bump (HTML)**
- `APP_VERSION` and the title-bar badge updated from `1.4.0-production` to `1.5.0`.

**Passphrase Field Default Type (HTML)**
- Changed from `type="text"` to `type="password"` so the value is hidden on load. The visibility toggle restores previous behavior when needed.

**Output Area Border (HTML)**
- When the output tab strip is shown, the output `<textarea>` border is managed by the wrapping `#outputWrap` container so that the top edge aligns cleanly with the active tab.

---

## [1.3.0] - 2026-06-02

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

## [1.2.0] - 2026-06-02

### Added

**Laptop / Small-Screen Layout (HTML)**
- New responsive breakpoint at `max-width: 1280px` (above the existing 980px collapse point) applies compact spacing without switching to single-column layout.
- At the laptop breakpoint: body and card padding reduced (20px ? 8px / 16px ? 10px), label column narrowed (260px ? 180px), font sizes tightened (14px ? 13px), button and input padding reduced, and word-grid gap tightened.

**Compact Default Sizing (Python GUI)**
- Default window geometry reduced from `1120?860` to `1040?760` to open comfortably on 13" screens without immediately hitting the minimum size constraint.
- Minimum window size reduced from `980?760` to `860?640`.
- `TButton` padding reduced from `(12, 8)` to `(8, 5)`; `TEntry` and `TCombobox` vertical padding reduced from `6` to `4`.

### Changed

**Word Grid - 12-Word Mode Hides Slots 13?24 (HTML & Python GUI)**
- Word entry cells 13?24 are now hidden when 12-word mode is active, cutting the numbered-words section roughly in half for the common case.
- Cells reappear immediately when the user switches to 24-word mode or pastes a 24-word mnemonic.
- In the HTML version, cells toggle via `display: none` inside `refreshWordEnabled()`. In the Python GUI, cells toggle via `grid_remove()` / `grid()` inside `on_seed_length_change()`.

**Mnemonic Textarea - Reduced Default Height (HTML & Python GUI)**
- Default height reduced from 4 lines (`min-height: 96px`) to 2 lines (`min-height: 60px`). The field remains user-resizable.

**Output Textarea - Reduced Default Height (HTML & Python GUI)**
- Default height reduced from 20 lines (`min-height: 280px`) to 10 lines (`min-height: 120px`). The field remains user-resizable.

**Seed Mask Character Changed from Asterisks to Bullets (HTML & Python GUI)**
- The masking character used to obscure hidden seed words changed from `****` to `????` in both the mnemonic textarea and the numbered word entries.

**`min-height: 100dvh` (HTML)**
- Replaced `100vh` with `100dvh` so macOS Safari correctly accounts for browser chrome height.

---

## [1.1.0] - 2026-06-01

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

## [Arculus_Recovery] - 2026-04-24

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

The project uses a `major.minor.patch` version string (e.g. `1.5.0`), surfaced in the UI title bar and via `--version` on the CLI. The `-production` channel suffix used in versions 1.1.0 through 1.4.0 has been dropped from 1.5.0 onwards. The README includes SHA256 hashes for the HTML app, Python launcher, source package, and vendored assets so users can verify the exact file state they are running, independent of the version string.
