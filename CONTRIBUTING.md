# Contributing to Arculus_Recovery

Arculus_Recovery is an offline, deterministic recovery tool for BIP39/BIP32/BIP86 workflows with both HTML/JS and Python implementations. Because this project handles sensitive cryptographic material, contributions must meet strict security, correctness, and reproducibility standards. This document defines the requirements for contributing code, documentation, or tests.

## 1. Project Scope

Arculus_Recovery supports:

- Offline mnemonic validation
- BIP39 seed generation
- BIP32 and BIP86 key derivation
- Multi‑coin derivation (BTC, LTC, DOGE)
- Taproot (BIP86) support
- Encrypted seed export/import using the .arc format
- Browser‑based and Python‑based offline workflows

Contributions must remain within this scope. Features that introduce network activity, telemetry, analytics, or remote dependencies will not be accepted.

## 2. Security Requirements

All contributions must follow these rules:

- No external network requests
- No remote scripts or CDNs
- No analytics or telemetry
- No dependencies that auto‑update or communicate externally
- All cryptographic operations must be deterministic
- All key‑handling code must avoid unnecessary data copies
- No code may weaken .arc file confidentiality or integrity
- Any change affecting cryptographic behavior must include a full review checklist (Section 8)

## 3. Workflow for Contributors

### Step 1 — Fork and Branch

```bash
git clone https://github.com/<your-username>/Arculus_Recovery
git checkout -b feature/my-change
```

### Step 2 — Make Focused Changes

- Keep changes atomic
- Update both HTML and Python versions when applicable
- Maintain parity between implementations unless intentionally diverging
- Update documentation when behavior changes

### Step 3 — Follow Coding Standards

**HTML/JavaScript**
- No external libraries unless stored locally
- Keep crypto logic isolated and explicit
- Avoid unnecessary DOM complexity
- Maintain offline compatibility across browsers

**Python**
- Python 3.10+
- Prefer standard library
- Keep GUI code minimal and cross‑platform
- Avoid unnecessary dependencies

## 4. Commit Message Format

Use conventional commits:

```
feat(html): add BIP86 fingerprint display
fix(python): correct hardened path parsing
docs: update .arc format description
refactor: simplify mnemonic validation logic
```

## 5. Pull Request Requirements

Every PR must include:

- Description of the change
- Rationale for the change
- Security considerations
- Testing steps
- Impact on .arc compatibility
- Screenshots for UI changes

PRs modifying cryptographic logic must include:

- Test vectors
- Before/after behavior
- Validation that legacy .arc files still import correctly

## 6. Testing Requirements

Before submitting a PR:

- Test both HTML and Python versions
- Validate 12‑word and 24‑word mnemonics
- Verify derivation for BTC, LTC, and DOGE
- Confirm BIP86 behavior
- Test .arc export and import
- Confirm offline operation

If adding new features:

- Include test cases
- Ensure no regressions in derivation paths or fingerprints

## 7. Documentation Requirements

When updating documentation:

- Keep explanations concise and technical
- Update screenshots if UI changes
- Document new CLI flags or UI elements
- Maintain consistency between HTML and Python documentation

## 8. Cryptographic Review Checklist

Any PR that modifies cryptographic behavior, key handling, or .arc file logic must complete this checklist. PRs missing this section will not be reviewed.

### 8.1 Algorithm and Primitive Review

- [ ] All cryptographic primitives are standard and widely reviewed
- [ ] No custom cipher, MAC, or KDF is introduced
- [ ] No deprecated primitives (e.g., SHA‑1, PBKDF2 with low iteration count)
- [ ] No reduction in entropy or key length

### 8.2 Determinism and Reproducibility

- [ ] All operations produce deterministic output for identical inputs
- [ ] No hidden randomness
- [ ] All randomness (if used) is explicitly sourced and documented

### 8.3 Key Handling

- [ ] No unnecessary copies of sensitive data
- [ ] Sensitive data is zeroed when possible
- [ ] No logging of sensitive material
- [ ] No exposure of intermediate values unless explicitly intended

### 8.4 .arc File Format Compatibility

- [ ] Existing .arc files remain importable
- [ ] New .arc files remain readable by older versions (unless version bump is intentional)
- [ ] Versioning is updated if format changes
- [ ] HMAC or integrity checks remain intact

### 8.5 Derivation Path Correctness

- [ ] BIP39 seed generation matches reference vectors
- [ ] BIP32 derivation matches reference vectors
- [ ] BIP86 derivation matches reference vectors
- [ ] Hardened vs. non‑hardened paths are handled correctly

### 8.6 Implementation Parity

- [ ] HTML and Python implementations match behavior
- [ ] Differences are documented if intentional

### 8.7 Offline Integrity

- [ ] No new network calls
- [ ] No new external dependencies
- [ ] No remote resources

### 8.8 Test Vectors

- [ ] Test vectors included for all modified operations
- [ ] Before/after comparison provided
- [ ] Edge cases tested (empty passphrase, long passphrase, hardened paths, etc.)

## 9. Reporting Issues

When opening an issue, include:

- Clear description
- Steps to reproduce
- Expected vs. actual behavior
- Browser or Python environment
- Whether .arc import/export is affected
- Screenshots or logs if relevant

Security‑related issues should be reported privately.

## 10. Code of Conduct

All contributors must maintain a professional and respectful environment. Harassment or hostile behavior will not be tolerated.

## 11. Acknowledgment

Your contributions strengthen a tool designed for offline security and deterministic recovery. Thank you for helping maintain a high standard of correctness and cryptographic integrity.