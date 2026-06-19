# Migration Guide - Arculus Recovery v1.6.4

This guide covers upgrading to the current v1.6.4 build and migrating `.arc`
seed backups. The canonical release-candidate implementation is `Arculus_Beta.html` v1.6.4.

## Upgrade Checklist

1. Transfer the full project folder or verified release artifact.
2. Verify hashes before entering real seed material.
3. Keep `Arculus_Beta.html`, promoted HTML/assets, Python files,
   Tauri files, docs, and release artifacts from the same build set.
4. Test with a known mnemonic before operational use.
5. Re-export older `.arc` files with v1.6.4 when practical.
6. Back up any new keyfiles created during migration.

Do not combine a v1.6.4 root HTML file with older packaged assets or wrappers
unless you are intentionally testing a compatibility boundary.

## Feature Migration Notes

The v1.6.4 HTML adds or formalizes:

- Bitcoin Cash, Solana, Stellar, Cardano, Tron, BNB Chain, Avalanche C-Chain,
  Polygon, Cosmos / ATOM, and XRP support in the canonical HTML app
- mainnet/testnet profiles for every production browser currency
- live derived-row filtering across addresses, private keys, and displayed data
- keyfile and keyfile + password `.arc` protection modes
- unprotected armored `.arc` export for controlled offline/test use
- hidden-seed handling for manually entered seeds after derivation
- Tauri v2 native save bridge
- byte-level documentation for file formats, encryption, derivation, and QR

The Python CLI is a compatibility superset with its own documented coin list,
including retained Monero automation. The production browser does not expose
Monero or Polkadot. Do not infer browser support from CLI choices.

Archived standalone builds now reside under `lts/`:

- `lts/Arculus_Recovery_v1.6.0_LTS.html`
- `lts/Arculus Recovery_v1.5.0_LTS.html`

## `.arc` Format History

| Format | Status / role | Notes |
| --- | --- | --- |
| `arculus-encrypted-seed-v3` inside `ARCULUS-ARC-V2` armor | Current v1.6.4 protected export | AES-256-GCM, authenticated metadata, 32-byte salt, 12-byte nonce, fixed 512-byte padded plaintext |
| `arculus-encrypted-seed-v2` inside `ARCULUS-ARC-V2` armor | Legacy protected import | PBKDF2-HMAC-SHA512, HMAC-SHA512 stream/MAC, 32-byte salt, 24-byte nonce |
| `ARCULUS-ARC-V2` armored plain | Current unprotected export option | Plain mnemonic JSON inside armor; not encrypted |
| Raw JSON `arculus-encrypted-seed-v2` | Import supported | Earlier V2 storage without armor |
| `arculus-encrypted-seed-python-v1` | Import supported | Legacy Python PBKDF2-SHA256/HMAC stream family |
| Browser `arculus-encrypted-seed-v1` | Browser import supported | Legacy PBKDF2-SHA256/AES-GCM family |
| Headerless legacy JSON | Import supported where structurally recognized | Old compatibility path |

In v1.6.4, the armor header remains `ARCULUS-ARC-V2`, but newly
protected bundles carry internal version 3 and format
`arculus-encrypted-seed-v3`. Do not identify the cryptographic format from the
armor line alone; decode the JSON bundle and inspect its `version` and `format`.

New v1.6.4 password-protected keyfiles carry `version: 2` while retaining the
`ARCULUS-KEYFILE-ENC` magic and `arculus-recovery-keyfile-enc-v1` format string.
They use AES-256-GCM. Version 1 encrypted keyfiles continue to use the legacy
stream-cipher and MAC path and remain importable.

## Migrating an Old `.arc` File

1. Start v1.6.4 on a trusted offline machine.
2. Click **Import Seed** and select the old `.arc` file.
3. Enter the old password or credential.
4. Confirm the imported mnemonic validates.
5. Enter the BIP39 passphrase if the wallet used one.
6. Verify the root fingerprint or a known address.
7. Click **Encrypt/Export Seed**.
8. Choose Password, Keyfile, or Keyfile + Password.
9. Save the new `.arc` file and any generated keyfile.
10. Re-import the new file once to confirm the recovery path.

The migration creates a fresh random salt and nonce. It does not store the BIP39
passphrase in the `.arc` file.

Re-exporting with v1.6.4 creates ARC V3 and, in combined
mode, an encrypted-keyfile v2 file. Keep the old backup until the new `.arc` and
all required credential factors have been successfully re-imported and checked
against a known root fingerprint or address.

## Keyfile Migration Rules

Password mode requires only the `.arc` file and password.

Keyfile mode requires:

- `Arculus_Encrypted_Seed.arc`
- `Arculus_Recovery_Keyfile.key`

Keyfile + Password mode requires:

- `Arculus_Encrypted_Seed.arc`
- `Arculus_Recovery_Keyfile.enc.key`
- encrypted-keyfile password

Losing a required keyfile or password makes recovery impossible through the
tool.

## Derived Export Migration

JSON, CSV, TXT, PDF, and QR PNG exports are snapshots. They are not migrated in
place. Re-derive and re-export when:

- the original export used an older schema
- you need Bitcoin Cash, Solana, Stellar, Monero, or Cardano output
- you need a different index range
- you need a different script type
- you suspect the old passphrase or derivation path was wrong
- you want v1.6.4 QR or PDF behavior

Derived exports containing private fields are plaintext key material. Handle
old and new exports as critical secrets.

## Desktop Package Migration

When moving to Tauri desktop packages:

- verify installer/executable hashes
- confirm the version shown by the app
- test JSON, CSV, TXT, PDF, `.arc`, keyfile, and QR PNG saves
- keep the standalone HTML file available as a fallback recovery surface

This repository may contain local release artifacts from multiple versions. The
presence of an artifact in `releases/` does not prove it belongs to the current
release. Verify filenames, metadata, and hashes.

## Hash Verification

Windows PowerShell:

```powershell
Get-ChildItem -Recurse -File Arculus_Beta.html,Arculus_Recovery.html,lts,Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

macOS/Linux:

```bash
find Arculus_Beta.html Arculus_Recovery.html lts Arculus_Recovery.py src vendor scripts src-tauri docs \
  -type f ! -name '._*' ! -path '*/screenshots/*' -print0 | sort -z | xargs -0 shasum -a 256
```

## Post-Upgrade Validation

Before relying on the upgraded tool:

- validate the standard `abandon ... about` mnemonic
- derive the Bitcoin vector in `docs/TestVectors.txt`
- import and export a test `.arc` file
- test password, keyfile, and combined credential modes if you plan to use them
- verify offline status after disconnecting networking
- confirm **Clear All** removes visible input and output
- rebuild or inspect `docs/Arculus_Recovery_Manual.pdf` when documentation changes
