# Migration Guide - Arculus Recovery

This document covers how to upgrade between versions of Arculus Recovery and how to migrate encrypted seed files (`.arc`) and derived-output exports across format changes.

---

## Upgrading to the Current Release

### Step 1 - Download the new files

Obtain the latest project folder from the repository, including `Arculus_Recovery.html`, `Arculus_Recovery.py`, `src/`, `vendor/`, `requirements.txt`, and `pyproject.toml`.

### Step 2 - Verify SHA256 hashes

Always verify file integrity before use. Run:

```bash
shasum -a 256 Arculus_Recovery.html Arculus_Recovery.py src/arculus_recovery/*.py src/arculus_recovery/assets/* vendor/jspdf/jspdf.umd.min.js
```

Or, from the current repository layout:

```bash
find Arculus_Recovery.html Arculus_Recovery.py src/arculus_recovery vendor/jspdf scripts/prepare_tauri_assets.py src-tauri/tauri.conf.json src-tauri/icons \
  docs/Arculus_Recovery_Manual.pdf \
  -type f ! -name '._*' -print0 | sort -z | xargs -0 shasum -a 256
```

Compare the output against the expected hashes published in the README. Do not proceed if any hash does not match.

If you are migrating to a packaged desktop build, also verify the installer or
DMG hash published in the README. On macOS, choose the universal DMG for both
Apple Silicon and Intel Macs, or choose the architecture-specific DMG when you
need a smaller single-architecture package.

### Step 3 - Replace old files

Replace your previous project folder with the verified new folder. The HTML file, Python launcher, `src/` package, and vendored assets are designed to be used together; always update them as a set.

### Step 4 - Test with a known mnemonic

Before relying on the updated tool for real seed recovery work, validate it with a known-good test mnemonic (e.g., the BIP39 test vector `abandon abandon ... about`) and confirm that derived addresses match expected values.

---

## `.arc` Encrypted Seed File Migration

### Format History

| Format identifier | Introduced in | KDF | Cipher | Notes |
|---|---|---|---|---|
| Legacy XOR-HMAC (no magic header) | Pre-release | PBKDF2-SHA256 | XOR + HMAC | Oldest format; no `magic` field |
| `arculus-encrypted-seed-python-v1` | Pre-release | PBKDF2-SHA256 | Varies | Python-only legacy format |
| `arculus-encrypted-seed-v1` (browser) | Pre-release | PBKDF2 | AES-GCM | HTML version only; not cross-compatible |
| `arculus-encrypted-seed-v2` (JSON) | Early release | PBKDF2-HMAC-SHA512, 600K+ iterations | HMAC-SHA512 counter stream | Cross-compatible; `magic: "ARCULUS-ARC"`, `version: 2` |
| `ARCULUS-ARC-V2` (armored) | Current release | PBKDF2-HMAC-SHA512, 1,000,000 iterations | HMAC-SHA512 counter stream | Current format; armored UTF-8; cross-compatible |

### What the current tool can read

The current release imports all of the following:

- Current armored `ARCULUS-ARC-V2` files
- JSON `arculus-encrypted-seed-v2` files with `magic: "ARCULUS-ARC"` and `version: 2`
- Legacy PBKDF2-SHA256 + XOR-HMAC files (no magic header)
- Legacy `arculus-encrypted-seed-python-v1` files
- `arculus-encrypted-seed-v1` files (HTML version only)

### Migrating old `.arc` files to the current format

If you have `.arc` files created by an earlier version, you should re-export them in the current armored format to benefit from the higher KDF iteration count (1,000,000 vs. 600,000) and the cross-compatible file structure.

**Procedure:**

1. Open the current version of `Arculus_Recovery.html` or run `Arculus_Recovery.py --gui` on a trusted, offline machine.
2. Use `Import Seed` to load the old `.arc` file and enter its password.
3. Once the seed is loaded (it will remain hidden on screen), use `Encrypt/Export Seed` to save a new `.arc` file.
4. Verify the new file can be re-imported successfully before deleting the old one.
5. Store the new `.arc` file on encrypted removable media.

**Note:** The re-exported file will use a new random salt and nonce. The password you choose at export time does not need to match the old file's password, though you may reuse it.

---

## Derived-Output Export Migration

Derived-output exports (JSON, CSV, TXT) are point-in-time snapshots. They do not have a version format that needs migration. If you generated exports with an earlier version of the tool:

- **Addresses:** may differ if derivation path defaults have changed. Re-derive from the seed to confirm current addresses.
- **Extended keys:** format has not changed; xpub/xprv serialization follows BIP32 throughout.
- **Taproot outputs:** only available in the current release. Earlier exports will not contain P2TR fields.

If you need Taproot-derived addresses from a seed you previously derived without Taproot support, re-run derivation with the current tool using script type `P2TR` and path `m/86'/coin'/0'`.

---

## Python Environment Migration

The Python CLI core uses the Python standard library. The desktop GUI now requires PySide6 because it renders the canonical HTML interface in a Qt WebEngine window. The tool has been tested on Python 3.x; Python 2 is not supported.

If you are moving the tool to a new machine:

1. Transfer the project folder to the new machine via encrypted media.
2. Verify the SHA256 hash matches the expected value from the README.
3. Confirm Python 3 is available: `python3 --version`.
4. Install GUI dependencies if needed: `python3 -m pip install -r requirements.txt`.
5. Run `python3 Arculus_Recovery.py --gui` or the appropriate CLI command.

---

## HTML Version Migration

`Arculus_Recovery.html` is the canonical browser app. The current repository does not ship a separate `index.html` copy.

Browser storage is used only to persist the theme preference. There is no stored seed data to migrate. When updating the HTML file, the theme preference in browser storage will be carried forward automatically.

---

## Cross-Version Compatibility Matrix

| Exporting version | Current armored `.arc` | JSON v2 `.arc` | Legacy formats |
|---|---|---|---|
| Current release (HTML) | Reads | Reads | Reads |
| Current release (Python) | Reads | Reads | Reads |
| Older HTML (v1 AES-GCM) | Cannot read current | - | Reads own format only |
| Older Python (v1) | Cannot read current | - | Reads own format only |

Recommendation: always use the current release for both exporting and importing. Older versions cannot read files produced by the current release.

---

## Summary Checklist for Upgrading

- [ ] Download the new project folder, including `Arculus_Recovery.html`, `Arculus_Recovery.py`, `src/`, and `vendor/`
- [ ] Verify SHA256 hashes against the README on an offline machine
- [ ] Replace the HTML, Python launcher, source package, and vendored assets together (never mix versions)
- [ ] Re-import and re-export any old `.arc` files to migrate them to the current armored format
- [ ] Verify re-exported `.arc` files can be imported before deleting old copies
- [ ] Store updated `.arc` files on encrypted removable media
- [ ] Test with a known mnemonic to confirm derivation output is correct


