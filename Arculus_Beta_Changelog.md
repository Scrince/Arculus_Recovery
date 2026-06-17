# Arculus Beta Changelog

All notable changes specific to `Arculus_Beta.html` are documented here.
This file tracks beta-build behavior separately from promoted release notes.

## [Unreleased Beta] - 2026-06-15

### Added

- Added a Settings -> Advanced `Testnet` toggle for recovery testing workflows
  that use testnet seeds and addresses.
- Added testnet network profiles for Bitcoin, Bitcoin Cash, Litecoin, Dogecoin,
  Ethereum, Tron, BNB Chain, Avalanche, Cosmos, Polkadot, Solana, Stellar,
  Monero, Cardano, and XRP.
- Added UTXO-family testnet derivation defaults by script type:
  - P2PKH: `m/44'/1'/0'`
  - P2WPKH-P2SH: `m/49'/1'/0'`
  - P2WPKH: `m/84'/1'/0'`
  - P2TR: `m/86'/1'/0'`
- Added Bitcoin Cash testnet CashAddr output with `bchtest:` prefix.
- Added Litecoin testnet address/key encoding, including `tltc1` SegWit output.
- Added Dogecoin testnet P2PKH/P2SH/WIF prefixes.
- Added Monero standard testnet address encoding with network byte `0x35`.
- Added Cardano Shelley testnet base address encoding with `addr_test` HRP and
  testnet network id `0`.
- Added testnet output metadata for Ethereum, Solana, Stellar, and XRP, whose
  address text formats are shared with their main networks.
- Added testnet output metadata for Tron, BNB Chain, Avalanche C-Chain, and
  Cosmos, whose address text formats are shared with their main networks.
- Added Polkadot testnet SS58 encoding with prefix `42`.
- Added BIP-39 autocomplete suggestions to the numbered manual-entry word grid.
- Added recovery derivation support for Tron / TRC-20, BNB Chain, Avalanche
  C-Chain, Cosmos / ATOM, and Polkadot.
- Added `docs/third_party_notices.txt` to collect third-party attribution,
  copyright, and license comments removed from the beta HTML source.
- Added a Playwright browser smoke test for `Arculus_Beta.html` covering page
  load, seed generation, validation, all supported coin derivations, output
  tabs, settings, QR generation, and PDF export.
- Added a GitHub Actions `HTML Smoke Tests` workflow for running the standalone
  HTML smoke test on pull requests, pushes to `main`, and manual dispatch.


### Changed

- Replaced the coin picker `<input>` + `<datalist>` with a standard `<select>`
  dropdown, matching the format used in the promoted release build.
- Coin dropdown options are now ordered alphabetically with Bitcoin pinned first
  as the default selection.

- Derivation now selects the active network profile from the Advanced Testnet
  toggle while preserving the selected coin in output metadata.
- Switching Bitcoin or Litecoin script type while Testnet is enabled now updates
  the default derivation path to the matching testnet purpose path.
- The Testnet setting is generalized across supported coins instead of applying
  only to Bitcoin.
- QR modal elements are now cached in the shared `els` object instead of being
  repeatedly looked up with `document.getElementById(...)` in QR render and
  event-handler paths.
- `Generate Random Seed` now asks for confirmation before replacing an existing
  visible, generated, imported, or hidden seed.
- The QR modal now closes on `Escape` even when opened through the manual
  `open` attribute fallback path.
- Sensitive seed, passphrase, and derived-output fields now clear immediately
  when the browser tab loses visibility.
- Clipboard copy failures in derived tables and extended-key panes now show a
  brief failure status instead of being silently swallowed.
- Relocated inline jsPDF attribution, copyright, and license comment blocks
  from `Arculus_Beta.html` into `docs/third_party_notices.txt` without changing
  executable beta behavior.
- Cleaned remaining non-license source comments in `Arculus_Beta.html` to
  remove garbled separators and mojibake while preserving functional code.
- Added `npm run test:smoke` to run the standalone beta HTML browser smoke test.

### Verified

- Confirmed inline JavaScript parses successfully.
- Confirmed the Advanced settings toggle appears as a generic `Testnet` control.
- Confirmed sample Bitcoin, Bitcoin Cash, Litecoin, Dogecoin, Tron, BNB Chain,
  Avalanche C-Chain, Cosmos, Polkadot, Monero, Cardano, Ethereum, Solana,
  Stellar, and XRP testnet derivations return
  `network: testnet` with the expected address/network formatting.
- Confirmed `Arculus_Beta.html` loads in a browser with no console errors after
  attribution relocation and comment cleanup.
- Confirmed seed generation, BIP-39 validation, PDF export, settings dialog,
  output tabs, QR modal opening, and all 15 coin derivation flows still work in
  browser smoke testing.
- Confirmed the new Playwright smoke-test source parses successfully with Node.
