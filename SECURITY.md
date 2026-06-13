# Security Policy

## Supported Versions

| Version | Support status |
| --- | --- |
| 1.6.x | Active |
| 1.5.x / LTS HTML copy | Best-effort documentation support |
| Older versions | Not supported |

Use the newest verified release whenever real seed material is involved. Keep the HTML file, Python package, documentation, and packaged desktop assets from the same release together.

## Security Model

Arculus Recovery is designed for offline local execution. It does not require an account, server, remote API, telemetry endpoint, hosted script, or CDN at runtime.

The tool can protect against accidental use of hosted recovery pages by running locally. It cannot protect secrets from a compromised machine.

## Sensitive Material

Treat all of the following as funds-controlling or security-sensitive:

- BIP39 mnemonic
- BIP39 passphrase
- `.arc` password
- `.arc` encrypted seed file
- Master private key and chain code
- Derived private keys
- WIF keys
- Extended private keys
- JSON, CSV, TXT, and PDF exports that include private key material

Addresses and root fingerprints are not secret, but they can reveal wallet structure and activity when correlated with on-chain history.

## Recommended Use

1. Verify hashes from a trusted release source.
2. Transfer the verified files to a trusted offline machine.
3. Disable all network interfaces physically where possible.
4. Use a clean browser profile or live operating system.
5. Enter or import seed material only after the machine is offline.
6. Verify the root fingerprint or a known address before acting on output.
7. Export only what is needed.
8. Store exports on encrypted removable media.
9. Clear the session and power down when finished.

## `.arc` File Security

Current `.arc` exports use armored `ARCULUS-ARC-V2` files. The format encrypts only the mnemonic.

It does not store or protect:

- The BIP39 passphrase
- Derived private keys
- Extended private keys
- JSON, CSV, TXT, or PDF exports
- QR PNG output

A strong `.arc` password is mandatory. A weak password can be guessed offline by anyone who obtains the file.

## Clipboard and Display Risk

Avoid copying seeds, passphrases, or private keys. Clipboard managers, remote desktop tools, browser extensions, and malware may read clipboard contents.

The app masks generated, imported, and successfully derived manually entered seeds, but this reduces accidental display only. It does not protect against screen capture, DOM inspection, memory scraping, or a malicious browser extension.

## Out of Scope

The project does not defend against:

- Malware already present on the device
- Keyloggers
- Clipboard monitors
- Screen recording or shoulder-surfing
- Browser, OS, firmware, Python, or WebView vulnerabilities
- Physical access to a live or recently used machine
- Social engineering
- Weak or forgotten BIP39 passphrases
- Wrong derivation path, wrong passphrase, or wrong coin selection

## Reporting Vulnerabilities

Please report security issues privately when possible. Include:

- Affected version and file
- Reproduction steps
- Expected and actual behavior
- Potential impact
- Whether `.arc`, mnemonic handling, derivation, export, or packaging is affected
- Suggested fix, if known

Do not include real seed phrases, private keys, or funded addresses in a report.
