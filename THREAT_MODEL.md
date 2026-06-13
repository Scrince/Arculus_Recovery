# Threat Model

## Overview

Arculus Recovery is an offline local recovery tool for BIP39/BIP32 wallet inspection. It supports the standalone HTML app, PySide6 GUI, Python CLI, and Tauri desktop wrapper. Its central security promise is that the application itself does not transmit seed phrases, passphrases, private keys, or derived output over a network.

That promise holds only when the user runs a verified copy on a trusted machine.

## Assets

| Asset | Sensitivity | Notes |
| --- | --- | --- |
| BIP39 mnemonic | Critical | Controls the wallet tree, subject to passphrase use |
| BIP39 passphrase | Critical | Produces a separate key tree; wrong value gives no error |
| `.arc` password | Critical | Protects encrypted seed backups |
| `.arc` file | High | Encrypted mnemonic backup, vulnerable to offline guessing if password is weak |
| Master private key | Critical | Root HD private key |
| Derived private keys / WIF | Critical | Controls individual addresses |
| Extended private keys | Critical | Controls a subtree |
| Derived exports | Critical when private fields are present | JSON, CSV, TXT, and PDF are plaintext |
| Addresses | Public, linkable | Not secret, but can expose wallet activity |
| Root fingerprint | Public verification value | Useful for confirming mnemonic/passphrase combination |

## Trust Boundaries

```text
User-controlled offline machine
  |
  |-- Arculus Recovery app
  |     |-- mnemonic validation
  |     |-- seed generation
  |     |-- BIP32 derivation
  |     |-- .arc encryption/decryption
  |     |-- local export
  |
  |-- OS CSPRNG
  |-- local filesystem
  |-- browser/WebView memory
  |-- clipboard and display

No application network dependency during normal operation.
```

## Threat Actors

| Actor | Capability | Mitigation |
| --- | --- | --- |
| Malicious file supplier | Ships a backdoored copy | Verify hashes and trusted source |
| Network attacker | Observes or alters traffic | Run the app locally and offline |
| Browser extension | Reads page contents | Use a clean profile with extensions disabled |
| Local malware | Captures memory, screen, or clipboard | Use a trusted live/offline OS |
| Physical observer | Sees screen or keyboard | Use private physical controls |
| Offline `.arc` attacker | Guesses file password | Use high-entropy password and current KDF |

## In-Scope Protections

- Local-only mnemonic validation and derivation
- CSPRNG-based mnemonic generation
- Authenticated `.arc` encrypted seed storage
- Detection of `.arc` tampering through MAC verification
- Hidden-seed display workflow
- Offline export generation
- Deterministic derivation for repeatable verification

## Out-of-Scope Risks

- An already-compromised operating system
- Malicious browser, Python runtime, WebView, or firmware
- Hardware keyloggers
- Side-channel attacks against the host machine
- Cloud backup or sync tools watching exported files
- User disclosure of seeds, passphrases, private keys, or exports
- On-chain discovery, balances, gap-limit scanning, or transaction signing

## Key Scenarios

| ID | Scenario | Impact | Mitigation |
| --- | --- | --- | --- |
| N-1 | User runs an altered HTML file | Critical | Verify release hashes |
| N-2 | User opens the app online with malicious extensions enabled | Critical | Airgap and use a clean profile |
| L-1 | Clipboard manager stores seed or private key | Critical | Avoid clipboard use for secrets |
| L-2 | Export file with private keys is left on disk | Critical | Store only on encrypted media |
| A-1 | Weak `.arc` password is guessed offline | Critical | Use random high-entropy password |
| A-2 | `.arc` metadata is tampered with | Low likelihood, high impact | MAC-bound metadata detects changes |
| P-1 | Wrong BIP39 passphrase is entered | Critical | Verify root fingerprint or known address |
| P-2 | Wrong derivation path is selected | High | Test known addresses and standard paths |

## Residual Risk

Even under correct offline use, the mnemonic and derived private keys must exist in process memory while the tool works. A privileged local attacker can still read them. Plaintext derived exports remain sensitive indefinitely. A lost BIP39 passphrase or `.arc` password cannot be recovered by the tool.

## Recommended Controls

- Prefer a live operating system with no persistent storage.
- Keep the machine offline before, during, and after seed entry.
- Verify hashes before use.
- Disable browser extensions.
- Record and verify the root fingerprint.
- Store `.arc` files and private-key exports separately.
- Keep `.arc` passwords and BIP39 passphrases backed up separately from the mnemonic.
- Destroy or securely archive retired private-key exports after sweeping funds.
