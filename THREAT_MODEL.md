# Threat Model — Arculus Recovery

**Version:** 1.1.0-production  
**Last Updated:** 2026-06-01  
**Scope:** `Arculus_Recovery.html`, `index.html`, `Arculus_Recovery.py`

---

## 1. Overview

Arculus Recovery is an offline BIP39/BIP32 seed recovery and key-derivation utility. It is available as a self-contained HTML file opened directly in a browser and as a Python script with both a desktop GUI (Tkinter) and a CLI. The tool performs all computation locally. It requires no server, cloud API, network request, telemetry endpoint, or external package.

The current derivation scope includes Bitcoin, Litecoin, Dogecoin, Ethereum / ERC-20, and XRP. Ethereum and XRP support are account-address derivation features; they do not query balances, inspect tokens, or fetch ledger data.

Version 1.1.0-production adds two significant input surfaces: a **Generate Random Seed** function that produces cryptographically random 12-word or 24-word mnemonics using the platform CSPRNG, and an **individual word-entry grid** that replaces the previous single-textarea mnemonic input.

The fundamental security promise is: **seed phrases, passphrases, private keys, and derived output never leave the user's machine through the application itself.**

---

## 2. Assets

The following assets are considered sensitive and are the primary targets of any attack against this tool.

| Asset | Description | Sensitivity |
|---|---|---|
| BIP39 mnemonic | 12- or 24-word seed phrase (typed, imported, or generated) | Critical |
| BIP39 passphrase | Optional 25th-word extension | Critical |
| CSPRNG entropy | Raw entropy bytes used during mnemonic generation | Critical (transient) |
| Master private key | Root HD wallet key derived from seed | Critical |
| Master chain code | Root HD wallet chain code | Critical |
| Derived private keys | Child keys at specific derivation paths | Critical |
| Extended private keys (xprv) | Serialized HD private keys | Critical |
| `.arc` encrypted seed file | Password-protected mnemonic backup | High |
| `.arc` encryption password | Password used to protect the `.arc` file | High |
| Derived addresses | Public-facing addresses; less sensitive but linkable across transactions, tokens, and accounts | Low-Medium |
| Destination tags / token metadata | Exchange or application routing metadata; not derived by the tool | Out of scope |
| Derived extended public keys (xpub) | Watch-only wallet keys | Medium |
| JSON/CSV/TXT derived-output exports | May contain private keys | Critical (if xprv included) |

---

## 3. Trust Boundaries

```
┌─────────────────────────────────────────────────────────┐
│                   USER'S MACHINE                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Arculus Recovery Application             │   │
│  │   (HTML in browser  /  Python GUI or CLI)        │   │
│  │                                                  │   │
│  │  • BIP39 validation     • Key derivation         │   │
│  │  • Random seed gen      • .arc encrypt/decrypt   │   │
│  │  • Word-grid input      • Export (JSON/CSV/TXT)  │   │
│  └──────────────────────────────────────────────────┘   │
│            │                       │                    │
│   OS CSPRNG (os.urandom /          │                    │
│   crypto.getRandomValues)          │                    │
│   (entropy input only;       Local filesystem only      │
│    no network)               (file open/save dialogs    │
│                               or CLI paths)             │
│  ┌───────────────────┐   ┌───────────────────────────┐  │
│  │  Browser storage  │   │  OS clipboard / memory    │  │
│  │  (dark-mode pref  │   │  (ephemeral; shared with  │  │
│  │   only — no seeds)│   │   other processes)        │  │
│  └───────────────────┘   └───────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         ║
         ║  ← No network traffic crosses this boundary
         ║     during normal tool operation
         ▼
    [ Internet / Remote Services ]   ← Out of scope for this tool
```

---

## 4. Threat Actors

| Actor | Capability | Motivation |
|---|---|---|
| Remote attacker (network) | Can intercept traffic, serve malicious pages | Steal funds by capturing seed |
| Local attacker (same machine) | Can read process memory, clipboard, temp files | Steal seed material from a compromised session |
| Malicious file supplier | Can distribute a backdoored copy of the tool | Exfiltrate seed on first use, or bias generated mnemonics |
| Physical attacker | Can access a powered-off or unattended machine | Extract keys from disk or memory |
| Passive observer | Can see screen, capture photos/video | Visual exposure of seed or private keys |

---

## 5. Threat Scenarios

### 5.1 Network-Based Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| N-1 | User opens the HTML file while online; a browser extension exfiltrates form contents or generated entropy | Medium | Critical | Disconnect from internet before use; disable extensions; use a clean browser profile |
| N-2 | User downloads a trojanized copy from a malicious mirror | Medium | Critical | Verify SHA256 hashes published in the README before every use |
| N-3 | DNS or BGP hijack redirects a hosted copy | Low | Critical | The tool is designed to be opened as a local file, not served from a website |

### 5.2 Local / Host-Based Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| L-1 | Keylogger captures seed entry via the word-entry grid | Medium | Critical | Use an air-gapped machine; avoid general-purpose desktops for seed work |
| L-2 | Screen recorder or screenshot captures mnemonic display or word-grid contents | Medium | Critical | Cover screen when working; use press-and-hold reveal only when necessary |
| L-3 | Clipboard manager stores copied seed phrase | High | Critical | Avoid copying seed phrases; the app warns before clipboard use |
| L-4 | Browser stores word-grid field values or autofill history | Medium | High | Use a private/incognito window or a clean browser profile; autofill should be disabled |
| L-5 | Process memory scraping extracts the decrypted or generated mnemonic | Low | Critical | The mnemonic must exist in memory during use; minimize time in memory by closing the app promptly |
| L-6 | Derived-output export file (JSON/CSV/TXT) left unprotected | High | Critical | Treat every export as secret; store on encrypted media; delete after use |
| L-7 | Browser download history reveals that a seed tool was used | Low | Medium | Clear browser downloads and history after use |

### 5.3 Random Seed Generation Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| G-1 | Backdoored tool returns a biased or attacker-known mnemonic during generation | Low | Critical | Verify SHA256 hashes before use; review generation code (`generateRandomMnemonic` in HTML, `generate_random_mnemonic` in Python) |
| G-2 | Weak CSPRNG produces low-entropy output | Very Low | Critical | HTML uses `crypto.getRandomValues`; Python uses `os.urandom`; both delegate to OS-level cryptographic entropy sources |
| G-3 | Generated mnemonic exposed via clipboard before user reviews it | Medium | Critical | Generated seeds follow the same hidden-seed workflow as imported seeds; the phrase is not placed in the clipboard or word grid automatically |
| G-4 | User generates a seed while online, allowing a network-capable extension to observe the CSPRNG output or DOM | Medium | Critical | Disconnect from the internet before generating a seed |

### 5.4 Encrypted Seed File (`.arc`) Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| A-1 | Weak password enables offline brute-force of `.arc` file | High (if weak password) | Critical | Use a strong, unique passphrase; the KDF uses 1,000,000 PBKDF2-HMAC-SHA512 iterations to slow guessing |
| A-2 | MAC bypass attack against the `.arc` format | Very Low | Critical | HMAC-SHA512 covers all versioned metadata, KDF parameters, nonce, and ciphertext |
| A-3 | Nonce reuse in HMAC-SHA512 counter stream | Very Low | High | A 24-byte random nonce is generated fresh per export |
| A-4 | `.arc` file stored in an insecure location (cloud sync, email) | High | High | Store `.arc` files on encrypted removable media only; never cloud-sync them |
| A-5 | Older format imports (≥600,000 iterations) accepted alongside current exports | Low | Low | Legacy imports are accepted for compatibility; users should re-export to current format when possible |

### 5.5 Supply-Chain Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| S-1 | Malicious commit to repository injects backdoor or biases CSPRNG output | Low | Critical | Verify SHA256 hashes from the README on every download |
| S-2 | GitHub account compromise leads to backdoored release | Low | Critical | Hash verification is independent of GitHub trust |
| S-3 | Python standard library vulnerability exploited | Very Low | Medium | The tool uses only stdlib; keep the Python runtime patched |

### 5.6 Operational Threats

| ID | Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| O-1 | User recovers or generates a seed on a machine already infected with malware | High | Critical | Use a dedicated air-gapped machine; run from a live OS if possible |
| O-2 | User shares exported files containing private keys | Medium | Critical | Exports are not encrypted; treat as plaintext secrets |
| O-3 | User forgets to disconnect from internet before use | High | Medium | The README and SECURITY.md both emphasize offline use; applies to both recovery and seed generation |
| O-4 | Physical shoulder-surfing during seed entry or reveal | Medium | Critical | Use the tool in a private environment |

---

## 6. Cryptographic Design Summary

| Component | Algorithm | Parameters |
|---|---|---|
| Random mnemonic generation (HTML) | `crypto.getRandomValues` | OS CSPRNG via Web Crypto API; entropy length matches word count (128-bit for 12 words, 256-bit for 24 words) |
| Random mnemonic generation (Python) | `os.urandom` | OS CSPRNG; same entropy lengths |
| BIP39 seed derivation | PBKDF2-HMAC-SHA512 | 2048 iterations, salt = `"mnemonic" + passphrase` (standard) |
| BIP32 master key | HMAC-SHA512 | Key = `"Bitcoin seed"` |
| `.arc` KDF | PBKDF2-HMAC-SHA512 | 1,000,000 iterations, 32-byte random salt |
| `.arc` encryption | HMAC-SHA512 counter stream | 24-byte random nonce |
| `.arc` authentication | HMAC-SHA512 | Covers versioned metadata, KDF params, nonce, and ciphertext |
| Key separation | Domain-specific HMAC-SHA512 labels | Encryption key ≠ authentication key |
| Password normalization | Unicode NFKD | Applied before KDF in both mnemonic and `.arc` contexts |
| Ethereum address formatting | Keccak-256 + EIP-55 | Uses uncompressed secp256k1 public key material and checksum casing |
| XRP classic address formatting | SHA256 + RIPEMD160 + XRPL base58check | Uses XRPL base58 alphabet and `0x00` account prefix |

---

## 7. Out of Scope

The following are explicitly outside the threat model of this tool:

- Malware already present on the host machine at the time of use
- Vulnerabilities in the user's browser, OS, Python runtime, or firmware
- Physical access by an adversary to a machine after use
- Side-channel attacks (timing, power, EM) against the cryptographic primitives
- Attacks against the BIP39 or BIP32 standards themselves
- Ledger-specific operational requirements outside derivation, such as XRP destination tags or ERC-20 contract selection
- Social engineering of the user

---

## 8. Residual Risks

Even with all recommended mitigations applied, the following residual risks remain:

1. **Memory exposure:** The decrypted or generated mnemonic must reside in process memory during validation and derivation. A sufficiently privileged attacker with access to the machine during a session can extract it.
2. **Password strength:** The security of `.arc` files at rest is bounded entirely by password entropy. No technical control compensates for a guessable password.
3. **Unencrypted derived exports:** JSON/CSV/TXT exports containing private keys have no built-in encryption. They are as sensitive as the mnemonic itself.
4. **CSPRNG trust:** Generated mnemonic security depends on the platform CSPRNG (`crypto.getRandomValues` / `os.urandom`). If the OS entropy source is compromised or the tool file is backdoored to bias output, generated seeds may be predictable.

---

## 9. Recommended Mitigations Summary

1. Use the tool on an air-gapped machine, ideally booted from a live OS.
2. Verify SHA256 hashes from the README before every use.
3. Disconnect from the internet before opening the HTML file or running the Python script — this applies equally to seed recovery and seed generation.
4. Use a clean browser profile with all extensions disabled.
5. Use a strong, unique password for `.arc` exports.
6. Store `.arc` files and derived-output exports on encrypted removable media.
7. Clear clipboard, download history, and terminal history after every session.
8. Avoid copying seed phrases, passphrases, or private keys to the clipboard.
9. Close the application promptly when done.
10. When generating a new seed, write it down on paper immediately after revealing it; do not store it digitally in plaintext.
