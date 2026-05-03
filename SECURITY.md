# Security Policy

## Overview

**Arculus Recovery** is an **offline-only** BIP39/BIP32 seed recovery tool designed with security and privacy as top priorities. The tool performs all operations locally in your browser or on your machine — no data is ever sent over the internet.

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| Latest  | ✅ Active          |
| Older   | ❌ Not supported   |

We recommend always using the latest version from the main branch.

## Security Best Practices

### Recommended Usage

1. **Always use offline** — Disconnect from the internet before opening the HTML file or running the Python script.
2. **Use on a trusted device** — Preferably an air-gapped computer or a clean, dedicated machine.
3. **Never share sensitive data** — Do not share your seed phrase, passphrase, private keys, or exported `.arc` files.
4. **Verify outputs** — Always double-check derived addresses on your hardware wallet before using them.

### Encryption

- Encrypted `.arc` files use secure, industry-standard practices.
- The encryption key is derived from your password using strong key derivation.
- Never use a weak password for encrypted backups.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

**Please do not** open a public GitHub issue with vulnerability details.

### How to Report

Send a detailed report to:

**Email:** [your-email@domain.com] *(replace with actual email)*

Or open a **private vulnerability report** on GitHub (if enabled).

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

We will acknowledge your report within 48 hours and aim to provide a fix or response as soon as possible.

## Scope

**In Scope:**
- Issues in `Arculus_Recovery.html`
- Issues in `Arculus_Recovery.py`
- Encryption / decryption of `.arc` files
- Seed phrase handling and key derivation logic

**Out of Scope:**
- Social engineering attacks
- Physical access to your device
- Misuse of the tool (e.g., using it while online)
- Issues caused by using outdated browsers or Python versions

## Disclaimer

While we take security very seriously, **no software is 100% secure**.  
This tool is provided **as-is**. Users are responsible for following best security practices when handling their seed phrases.

---

Thank you for helping keep Arculus Recovery secure! 🙏
