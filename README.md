# Arculus-BTC-Recovery
Arculus BTC Recovery

Arculus BTC Recovery is an offline Bitcoin seed recovery utility provided in two formats:
- Desktop Python app: Arculus_BTC_Recovery.py
- Standalone browser app: Arculus_BTC_Recovery.html

What it does
- Validates BIP39 English seed phrases (12 or 24 words), including checksum verification.
- Accepts custom derivation paths (supports hardened notation with ' or h).
- Derives and displays key data for Bitcoin accounts:
  - Root extended private/public keys
  - Account extended private/public keys
  - Receiving addresses
  - Change addresses
  - Derived private keys (hex + WIF)
- Exports generated results to a .txt file.

Key capabilities
- Works fully offline for seed validation and key/address derivation.
- Numbered word entry interface and mnemonic text entry are both supported.
- Script type selection supported:
  - Auto
  - P2PKH
  - P2WPKH-P2SH
  - P2WPKH

Quick start (Python app)
1. Install Python 3.10+.
2. Run:
   python Arculus_BTC_Recovery.py --gui

Quick start (HTML app)
1. Open Arculus_BTC_Recovery.html in a modern browser (Chrome/Edge/Firefox/Safari).
2. No server setup is required.

Suggested GitHub notes for users
- Security warning: Never share your real seed phrase, private keys, or exported output.
- Use on an air-gapped/offline machine when possible.
- Verify downloaded files (checksums/signatures/releases) before use.
- This tool performs local derivation only; it does not query blockchain services.
- The project is intended for recovery/inspection workflows, not as a daily-use wallet.

Recommended repository additions
- Include this file as part of your README/release notes.
- Add a LICENSE file.
- Add SECURITY.md with responsible disclosure and handling guidance.
- Add clear version tags/releases and changelog entries.
