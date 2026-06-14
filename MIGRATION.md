# Migration Guide - Arculus Recovery v1.6.0

This guide covers upgrading to the current v1.6.0 build and migrating `.arc`
seed backups. The canonical implementation is `Arculus_Recovery.html` v1.6.0.

## Upgrade Checklist

1. Transfer the full project folder or verified release artifact.
2. Verify hashes before entering real seed material.
3. Keep `Arculus_Recovery.html`, `src/arculus_recovery/assets/`, Python files,
   Tauri files, docs, and release artifacts from the same build set.
4. Test with a known mnemonic before operational use.
5. Re-export older `.arc` files with v1.6.0 when practical.
6. Back up any new keyfiles created during migration.

Do not combine a v1.6.0 root HTML file with older packaged assets or wrappers
unless you are intentionally testing a compatibility boundary.

## Feature Migration Notes

The v1.6.0 HTML adds or formalizes:

- Bitcoin Cash, Solana, Stellar, Monero, and Cardano support in the canonical HTML app
- keyfile and keyfile + password `.arc` protection modes
- unprotected armored `.arc` export for controlled offline/test use
- hidden-seed handling for manually entered seeds after derivation
- Tauri v2 native save bridge
- byte-level documentation for file formats, encryption, derivation, and QR

The Python CLI remains a compatibility surface for Bitcoin, Litecoin, Dogecoin,
Ethereum, and XRP. Use the HTML app for the full v1.6.0 coin set.

## `.arc` Format History

| Format | Status in v1.6.0 | Notes |
| --- | --- | --- |
| `ARCULUS-ARC-V2` armored encrypted | Current protected export | PBKDF2-HMAC-SHA512, 1,000,000 iterations, 32-byte salt, 24-byte nonce |
| `ARCULUS-ARC-V2` armored plain | Current unprotected export option | Plain mnemonic JSON inside armor; not encrypted |
| Raw JSON `arculus-encrypted-seed-v2` | Import supported | Earlier V2 storage without armor |
| `arculus-encrypted-seed-python-v1` | Import supported | Legacy Python PBKDF2-SHA256/HMAC stream family |
| Browser `arculus-encrypted-seed-v1` | Browser import supported | Legacy PBKDF2-SHA256/AES-GCM family |
| Headerless legacy JSON | Import supported where structurally recognized | Old compatibility path |

New protected exports should use `ARCULUS-ARC-V2`.

## Migrating an Old `.arc` File

1. Start v1.6.0 on a trusted offline machine.
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
- you want v1.6.0 QR or PDF behavior

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
Get-ChildItem -Recurse -File Arculus_Recovery.html,Arculus_Recovery_LTS.html,Arculus_Recovery.py,src,vendor,scripts,src-tauri,docs |
  Where-Object { $_.Name -notlike '._*' -and $_.FullName -notmatch '\\screenshots\\' } |
  Sort-Object FullName |
  Get-FileHash -Algorithm SHA256
```

macOS/Linux:

```bash
find Arculus_Recovery.html Arculus_Recovery_LTS.html Arculus_Recovery.py src vendor scripts src-tauri docs \
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
