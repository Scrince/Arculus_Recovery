# Threat Model - Arculus Recovery v1.6.0

## Overview

Arculus Recovery is a local offline recovery tool for BIP39/BIP32 wallet
inspection, encrypted seed backup, deterministic address derivation, and local
export. The canonical v1.6.0 surface is `Arculus_Recovery.html`. Python and
Tauri surfaces package or automate parts of that workflow.

The central security objective is that the application does not transmit seed
phrases, passphrases, keyfiles, private keys, or derived exports over a network.
This objective depends on users running a verified copy on a trusted offline
machine.

## Assets

| Asset | Sensitivity | Notes |
| --- | --- | --- |
| BIP39 mnemonic | Critical | Controls wallet tree, subject to BIP39 passphrase |
| BIP39 passphrase | Critical | Creates a different wallet tree; wrong value can look valid |
| `.arc` password | Critical | Protects encrypted seed backup in password mode |
| Raw keyfile bytes | Critical | Protects `.arc` backup in keyfile mode |
| Encrypted keyfile password | Critical | Required with encrypted keyfile in combined mode |
| `.arc` file | High to critical | Contains encrypted or plaintext mnemonic depending on mode |
| Master/account private keys | Critical | Controls root/account subtrees |
| Derived row private keys | Critical | Controls individual addresses/accounts |
| Extended private keys | Critical | Controls child keyspace below the extended node |
| Stellar secret seed | Critical | Controls Stellar account |
| Monero private spend/view keys | Critical | Spend/view authority for derived Monero address |
| Cardano private keys | Critical | Controls derived payment/staking material |
| Derived exports | Critical | JSON/CSV/TXT/PDF may contain private fields |
| QR PNG | Low to medium | Address payload only, but can reveal address ownership |
| Addresses/fingerprints | Public but linkable | Useful for verification and chain correlation |

## Trust Boundaries

```text
User-controlled offline machine
  |
  |-- Browser/WebView executing Arculus_Recovery.html
  |     |-- BIP39 validation and generation
  |     |-- BIP39 seed stretching
  |     |-- secp256k1 / Ed25519 derivation
  |     |-- .arc encryption/decryption
  |     |-- keyfile generation/decryption
  |     |-- local exports and QR rendering
  |
  |-- OS CSPRNG
  |-- local filesystem/downloads
  |-- clipboard and display
  |-- optional Tauri native save bridge
  |-- optional Python wrapper/CLI

No required application network dependency during normal recovery.
```

## Threat Actors

| Actor | Capability | Primary mitigation |
| --- | --- | --- |
| Malicious file supplier | Ships modified HTML, wrapper, or installer | Verify hashes and source |
| Network attacker | Alters downloads or observes traffic | Transfer verified files; run offline |
| Browser extension | Reads DOM, clipboard, or page data | Use clean profile or extension-free browser |
| Local malware | Captures memory, keys, files, screen, clipboard | Use trusted offline/live OS |
| Physical observer | Watches screen or keyboard | Private workspace and screen discipline |
| Offline `.arc` attacker | Brute-forces password | Strong password, keyfile, or combined mode |
| Cloud sync/backup tool | Copies exported files | Disable sync; use encrypted removable media |
| User error | Wrong path/passphrase/coin/range | Verify known addresses and root fingerprint |

## In-Scope Protections

- Local-only recovery workflow.
- BIP39 checksum validation.
- CSPRNG mnemonic generation.
- Deterministic derivation for reproducible verification.
- ARC V2 authentication before decryption.
- Keyfile and combined `.arc` protection modes.
- Hidden-seed UI for generated/imported/manual seeds.
- Local export with explicit user action.
- QR export limited to address payloads.
- Idle timeout that clears visible UI state.

## Out-of-Scope Risks

- Compromised host OS, browser, WebView, Python runtime, or firmware.
- Hardware keyloggers and malicious peripherals.
- Side-channel attacks against CPU/browser/OS.
- Memory forensics after use.
- Browser extension compromise.
- Clipboard manager persistence.
- Screen recording and shoulder-surfing.
- Blockchain balance discovery or wallet gap-limit scanning.
- Transaction signing and broadcast safety.
- Recovery from forgotten BIP39 passphrases, `.arc` passwords, or lost keyfiles.

## Key Scenarios

| ID | Scenario | Impact | Mitigation |
| --- | --- | --- | --- |
| S-1 | User runs altered `Arculus_Recovery.html` | Critical | Verify release hashes; compare known test vectors |
| S-2 | User opens tool with malicious extension enabled | Critical | Use clean offline browser profile |
| S-3 | Weak `.arc` password is guessed offline | Critical | Use high-entropy password or keyfile/combined mode |
| S-4 | Keyfile is lost | Critical | Back up keyfile separately from `.arc` |
| S-5 | Unprotected `.arc` is mistaken for encrypted backup | Critical | Treat `arculus-plain-seed-v1` as plaintext mnemonic |
| S-6 | Wrong BIP39 passphrase is entered | High | Verify root fingerprint and multiple known addresses |
| S-7 | Wrong derivation path/script is selected | High | Match original wallet path; test receive/change indexes |
| S-8 | Derived JSON/PDF is left on disk | Critical | Store encrypted; delete or archive intentionally |
| S-9 | Clipboard stores seed/private key | Critical | Avoid clipboard use; clear session; distrust clipboard managers |
| S-10 | XRP destination tag omitted for custodian deposit | High | Obtain destination tag from custodian; tags are not derived |

## ARC V2 Threat Notes

ARC V2 protects confidentiality and integrity of the mnemonic payload against
offline file attackers when a strong credential is used. The MAC transcript
binds magic, format, version, created_at, KDF parameters, cipher name, salt,
nonce, and ciphertext.

The credential-mode hint is UI metadata and must not be treated as a security
policy boundary by external tools. The BIP39 passphrase is intentionally not
inside `.arc` files.

## Residual Risk

During use, seed words and private material exist in process memory. JavaScript
strings cannot be reliably zeroized. Plaintext derived exports remain sensitive
for as long as they exist. A privileged local attacker can still compromise
secrets even if the app itself performs no network I/O.

## Recommended Controls

- Use a verified offline machine.
- Prefer a fresh live OS for high-value recovery.
- Disable browser extensions and sync.
- Verify output with `docs/TestVectors.txt` before operational use.
- Verify real recovery with known addresses before exporting or moving funds.
- Store `.arc`, keyfile, BIP39 passphrase, and `.arc` password separately.
- Destroy temporary plaintext exports after use.
