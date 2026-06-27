# Contributing to YellowSphere

YellowSphere handles funds-controlling secrets. Contributions are welcome,
but changes must preserve offline execution, deterministic derivation, explicit
secret boundaries, and compatibility with the canonical v1.6.4 HTML behavior.

## Project Boundaries

Accepted work should stay within:

- offline BIP39 mnemonic validation and generation
- BIP39 passphrase handling
- deterministic key derivation and address encoding
- `.arc` seed import/export
- keyfile and combined credential support
- local JSON, CSV, TXT, PDF, and QR PNG export
- Python compatibility CLI and GUI wrappers
- Tauri desktop packaging
- documentation, test vectors, and release tooling

Do not add telemetry, analytics, remote scripts, CDN runtime dependencies,
hosted recovery flows, balance lookups, automatic updates, cloud sync, or any
network-required recovery feature.

## Source of Truth

The canonical v1.6.4 production implementation is `YellowSphere.html`.
The docs in `docs/` specify v1.6.4 byte-level behavior. The Python CLI is
a compatibility superset and may retain explicitly documented currencies that
the browser selector does not expose.

If HTML, Python, Tauri, and documentation disagree, either fix the disagreement
or document the compatibility boundary explicitly.

## Development Rules

- Keep `YellowSphere.html` usable as a direct local file.
- Keep runtime recovery independent of internet access.
- Treat `.arc`, keyfile, BIP39, BIP32, Ed25519, address encoding, QR payload,
  and export schema changes as security-sensitive.
- Use deterministic output for identical inputs except where randomness is part
  of the specification.
- Update `docs/` and `TestVectors.txt` when byte behavior changes.
- Rebuild `docs/YellowSphere_Manual.pdf` only after text docs are updated.
- Avoid unrelated refactors in secret-handling code.
- Do not log seed words, passphrases, private keys, keyfiles, or decrypted
  payloads.

## Local Setup

Python package and CLI:

```bash
python -m pip install .
python YellowSphere.py --help
```

Python GUI:

```bash
python -m pip install -r requirements.txt
python YellowSphere.py --gui
```

Tauri:

```bash
npm install
npm run prepare:tauri
npm run tauri -- build
```

Manual PDF:

```bash
python scripts/build_manual_pdf.py
```

If system Python lacks ReportLab, use an isolated environment with ReportLab or
the bundled workspace runtime when available.

## Required Testing

Run the checks that match the touched surface:

- Run `npm run test:html` for changes to `YellowSphere.html` or its browser
  harness. Use `test:smoke` or `test:crypto` for a focused iteration.
- Run `npm run test:python` for Python core, CLI, launcher, packaging, or GUI
  asset-discovery changes.
- Run `npm run test:tauri` for Tauri/Rust or prepared-asset changes. Before
  publishing, run `npm run test:tauri:windows`, `npm run test:tauri:macos`, or
  `npm run test:tauri:linux` on the matching build host. Use the corresponding
  `:validate` command to verify published artifacts without rebuilding.
- Open `YellowSphere.html` locally with networking disabled.
- Validate the standard `abandon ... about` mnemonic.
- Generate and validate both 12-word and 24-word mnemonics when BIP39 changed.
- Derive at least one known Bitcoin address vector.
- Test expanded HTML coins when their derivation code changes.
- Export and import protected `.arc` files for password, keyfile, and combined modes when seed protection changed.
- Test unprotected `.arc` import/export if that path changed.
- Export JSON, CSV, TXT, PDF, and QR PNG when export or Tauri code changed.
- Run `python YellowSphere.py --help` when Python code changed.
- Test Tauri native save behavior when `src-tauri/`, asset preparation, or packaged HTML changes.
- Rebuild and inspect the manual PDF when root docs or `docs/` change.

## Security Review Checklist

For changes touching mnemonic generation, BIP39, BIP32, SLIP-0010, Ed25519,
Cardano, Monero, Taproot, Ethereum, XRP, `.arc`, keyfiles, exports, or QR:

- [ ] No reduction in entropy, key length, nonce length, MAC length, or KDF policy.
- [ ] New randomness uses browser/OS CSPRNG.
- [ ] Existing supported `.arc` files still import unless a version break is intentional.
- [ ] MAC verification happens before decryption where specified.
- [ ] Serialization changes are reflected in `docs/FileFormat.txt`.
- [ ] Cryptographic transcript changes are reflected in `docs/Encryption.txt`.
- [ ] Derivation changes are reflected in `docs/Derivation.txt`.
- [ ] Test vectors are updated or explicitly documented as unchanged.
- [ ] Sensitive values are not logged or exposed without explicit user action.
- [ ] Clipboard exposure is not increased silently.
- [ ] Offline operation still works.

## Pull Request Checklist

Every PR should include:

- Summary of what changed
- Reason for the change
- Affected surfaces: HTML, Python CLI, PySide6 GUI, Tauri, docs, release assets
- Security impact
- `.arc` compatibility impact
- Test commands and manual checks performed
- Screenshots for UI changes
- Documentation updates

## Commit Style

Use concise conventional-style commits:

```text
feat(html): add keyfile arc export mode
fix(qr): render xrp destination tag payload consistently
docs: rewrite v1.6 byte-level references
build(tauri): update native export bridge assets
```

## Vulnerability Reports

Do not disclose vulnerabilities publicly before maintainers can investigate.
Never include real seed phrases, private keys, funded addresses, or production
keyfiles in a report.
