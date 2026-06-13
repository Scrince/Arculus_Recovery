# Contributing to Arculus Recovery

Arculus Recovery handles seed phrases, private keys, and encrypted seed backups. Contributions are welcome, but changes must preserve offline operation, deterministic derivation, and cross-surface compatibility between the HTML app, Python CLI, PySide6 GUI, and Tauri wrapper.

## Project Boundaries

Accepted work should stay inside the project's purpose:

- Offline BIP39 mnemonic validation and generation
- BIP32/BIP44/BIP49/BIP84/BIP86 derivation
- Bitcoin, Litecoin, Dogecoin, Ethereum / ERC-20, and XRP address output
- Encrypted `.arc` seed import/export
- Local export of derived data
- Documentation, tests, packaging, and release tooling

Do not add telemetry, analytics, hosted services, remote scripts, CDN dependencies, balance lookups, cloud sync, or automatic update behavior.

## Development Rules

- Keep the standalone HTML app usable as a local file with no runtime network dependency.
- Keep cryptographic behavior deterministic for identical inputs.
- Maintain parity between HTML and Python behavior unless a difference is deliberate and documented.
- Treat changes to `.arc`, derivation, address encoding, or export schemas as security-sensitive.
- Update documentation and test vectors when behavior changes.
- Avoid broad refactors in security-critical code unless they are required for the change.

## Local Setup

Python CLI and packaging metadata:

```bash
python -m pip install .
```

Python GUI:

```bash
python -m pip install -r requirements.txt
python Arculus_Recovery.py --gui
```

Tauri packaging:

```bash
npm install
npm run prepare:tauri
npm run tauri -- build
```

Use the platform-specific build instructions in `README.md` when producing release artifacts.

## Required Testing

Before submitting a change, run the checks that match the touched surface:

- Open `Arculus_Recovery.html` locally and confirm no network access is required.
- Run `python Arculus_Recovery.py --help`.
- Run CLI derivation against the standard `abandon ... about` mnemonic.
- Test 12-word and 24-word validation when mnemonic handling changed.
- Test `.arc` export/import when seed storage changed.
- Test PDF, JSON, CSV, TXT, and QR export when UI or packaging changed.
- Test Tauri export behavior when `src-tauri/`, `tauri-dist/`, or asset preparation changed.
- Rebuild `docs/Arculus_Recovery_Manual.pdf` when files in `docs/` change.

## Pull Request Checklist

Every PR should include:

- What changed
- Why it changed
- User-visible impact
- Security considerations
- Testing performed
- `.arc` compatibility impact, if any
- Screenshots for UI changes
- Documentation updates, if behavior or workflows changed

## Cryptographic Review Checklist

Complete this checklist for any change touching mnemonic generation, BIP39, BIP32, Taproot, address encoding, `.arc`, private-key handling, or export schemas:

- [ ] Standard primitives only; no custom hash, MAC, KDF, or curve construction added.
- [ ] No downgrade in entropy, key length, MAC length, or KDF iteration policy.
- [ ] Existing `.arc` files still import unless a documented version break is intentional.
- [ ] New `.arc` exports are readable by both supported implementations.
- [ ] BIP39 seed output matches reference vectors.
- [ ] BIP32 derivation matches reference vectors.
- [ ] Taproot output matches reference vectors when touched.
- [ ] Ethereum EIP-55 and XRP classic-address output match reference vectors when touched.
- [ ] Sensitive values are not logged.
- [ ] Clipboard or display exposure is not increased without explicit user action.
- [ ] HTML and Python behavior remain equivalent, or the difference is documented.
- [ ] The app still works offline.

## Commit Style

Use concise conventional-style commits:

```text
feat(html): mask entered seed after derivation
fix(qr): encode XRP destination tag query correctly
docs: refresh v1.6 manual sources
build(tauri): prepare desktop export bridge assets
```

## Security Reports

Do not disclose vulnerabilities publicly before maintainers can investigate. Include reproduction steps, affected files, expected behavior, actual behavior, and possible impact.
