# Security Policy

## Supported Versions

| Version | Support status |
| --- | --- |
| 1.6.x | Active |
| 1.5.x / LTS HTML copy | Best-effort migration and documentation support |
| Older versions | Not supported |

Use the newest verified v1.6.x build whenever real seed material is involved.
Keep the HTML file, packaged assets, Python package, desktop wrapper, and docs
from the same release set.

## Security Model

Arculus Recovery is an offline local recovery tool. It does not require an
account, server, telemetry endpoint, hosted script, CDN, balance API, or
blockchain node during normal recovery use.

The security promise is local execution, deterministic derivation, and explicit
local export. That promise only holds when the user runs a verified copy on a
trusted machine.

## Sensitive Material

Treat these as critical:

- BIP39 mnemonic
- BIP39 passphrase
- `.arc` password
- raw keyfile bytes
- encrypted keyfile password
- combined `.arc` credential
- `.arc` seed file
- master private key and chain code
- account extended private keys
- WIF/private-key hex values
- Stellar secret seeds
- Monero private spend and private view keys
- Cardano private keys
- JSON, CSV, TXT, and PDF exports containing private fields

Addresses and root fingerprints are not secret, but they can reveal wallet
structure and activity when correlated with public chain data.

## Recommended Use

1. Verify hashes from a trusted source.
2. Move the verified files to a trusted offline machine.
3. Disable all network interfaces before entering secrets.
4. Use a clean browser profile or live operating system.
5. Enter or import seed material only after the machine is offline.
6. Verify a root fingerprint or known address before relying on output.
7. Export only the material required.
8. Store exports on encrypted removable media.
9. Click **Clear All**, close the app, and power down when finished.

## `.arc` Security

Current v1.6.4 protected `.arc` exports use `ARCULUS-ARC-V2` outer armor with
internal `arculus-encrypted-seed-v3`:

- AES-256-GCM with a 128-bit tag
- 32-byte random salt
- 12-byte random nonce
- fixed 512-byte plaintext padding
- authenticated JSON metadata as additional authenticated data
- PBKDF2-HMAC-SHA512 at 1,000,000 iterations for Password mode
- HKDF-SHA512 for Keyfile and combined modes

Protection modes:

- Password
- Keyfile
- Keyfile + Password

Unprotected export stores plaintext mnemonic JSON inside `.arc` armor. It is
not encrypted and should not be used for real funds except in controlled offline
procedures where plaintext handling is intentional.

The `.arc` file stores the mnemonic only. It does not store the BIP39
passphrase or derived keys.

### ARC V3 and Encrypted-Keyfile v2

`Arculus_Beta.html` v1.6.4 writes newly protected `.arc` exports as internal format
`arculus-encrypted-seed-v3`. It retains the existing outer armor header but
uses AES-256-GCM with a 32-byte salt, 12-byte nonce, 128-bit authentication tag,
and a fixed 512-byte padded plaintext.

Password mode pre-hashes the NFKD-normalized password with SHA-512 before
PBKDF2-HMAC-SHA512 at 1,000,000 iterations. Keyfile and combined modes use
HKDF-SHA512. The combined construction requires both raw keyfile bytes and the
password and is salted by the `.arc` file.

All V3 bundle metadata, including the credential-mode hint, is authenticated as
AES-GCM additional authenticated data. Modifying the header, credential mode,
or ciphertext causes authentication failure. V3 does not use a separate MAC.

New beta encrypted keyfiles use AES-256-GCM with SHA-512 password pre-hashing,
PBKDF2-HMAC-SHA512 at 1,000,000 iterations, and a 12-byte nonce. Their magic and
format fields are authenticated. Legacy ARC formats and encrypted keyfiles are
still read by their original compatibility paths.

## Clipboard, Display, and Memory

Avoid copying seeds, passphrases, private keys, and keyfile secrets. Clipboard
managers, browser extensions, remote desktop software, malware, and host OS
features may retain clipboard contents.

The app masks generated, imported, and successfully derived manually entered
seeds. This reduces accidental display but does not protect against DOM
inspection, screen capture, memory scraping, or malicious extensions.

JavaScript strings cannot be reliably zeroized. Some typed arrays are cleared
after use, but process memory remains under browser and operating-system
control.

## Out of Scope

The project does not defend against:

- malware already present on the device
- malicious browser, WebView, Python runtime, OS, firmware, or hardware
- keyloggers and screen recorders
- browser extensions with page access
- clipboard monitors
- cloud sync watching exports
- physical access to a live or recently used machine
- social engineering
- weak or forgotten BIP39 passphrases
- weak or forgotten `.arc` passwords
- lost keyfiles
- wrong coin, path, script type, range, or passphrase selection

## Reporting Vulnerabilities

Report security issues privately when possible. Include:

- affected version and file
- reproduction steps
- expected and actual behavior
- potential impact
- whether `.arc`, keyfiles, mnemonic handling, derivation, export, QR, or
  packaging is affected
- suggested fix, if known

Do not include real seed phrases, private keys, funded addresses, production
`.arc` files, or production keyfiles in a report.
