from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "WhitePaper.pdf"


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "WhitePaperTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "WhitePaperSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=8,
        ),
        "kicker": ParagraphStyle(
            "WhitePaperKicker",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#6B7280"),
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "WhitePaperH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#111827"),
            spaceBefore=14,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "WhitePaperH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=11,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "WhitePaperH3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#374151"),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "WhitePaperBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "WhitePaperSmall",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#374151"),
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "WhitePaperBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.8,
            textColor=colors.HexColor("#111827"),
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "caption": ParagraphStyle(
            "WhitePaperCaption",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#6B7280"),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "WhitePaperCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=9.2,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#F3F4F6"),
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.35,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "callout": ParagraphStyle(
            "WhitePaperCallout",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#F8FAFC"),
            borderColor=colors.HexColor("#94A3B8"),
            borderWidth=0.6,
            borderPadding=8,
            spaceBefore=5,
            spaceAfter=9,
        ),
    }


class Rule(Flowable):
    def __init__(self, width=6.2 * inch, color=colors.HexColor("#CBD5E1")):
        super().__init__()
        self.width = width
        self.height = 8
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.75)
        self.canv.line(0, 4, self.width, 4)


def p(text: str, style):
    return Paragraph(esc(text), style)


def bullets(items: list[str], st):
    return ListFlowable(
        [ListItem(p(item, st["bullet"])) for item in items],
        bulletType="bullet",
        leftIndent=18,
        bulletFontSize=5,
        spaceAfter=6,
    )


def table(data, widths, header=True):
    rows = []
    for row in data:
        rows.append([Paragraph(esc(str(cell)), styles()["small"]) for cell in row])
    ts = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        ts.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
            ]
        )
    return Table(rows, colWidths=widths, repeatRows=1 if header else 0, style=TableStyle(ts))


def section(story, st, title: str):
    story.append(Paragraph(esc(title), st["h1"]))


def subsection(story, st, title: str):
    story.append(Paragraph(esc(title), st["h2"]))


def subsubsection(story, st, title: str):
    story.append(Paragraph(esc(title), st["h3"]))


def add_architecture_diagram(story, st):
    data = [
        ["User interface", "Standalone HTML", "PySide6 WebEngine", "Tauri WebView"],
        ["Shared semantics", "BIP39 validation, derivation path handling, QR and export workflows", "Loads canonical HTML for UI parity", "Loads generated canonical HTML copy"],
        ["Python engine", "N/A", "CLI and compatibility launcher", "N/A"],
        ["Native boundary", "Browser file APIs", "Qt file dialogs and WebEngine profile", "Rust save_export command and native save dialog"],
        ["Distribution", "Single offline HTML file", "Python package plus GUI dependency", "Platform-specific installers and application bundles"],
    ]
    story.append(table(data, [1.15 * inch, 1.9 * inch, 1.65 * inch, 1.65 * inch]))
    story.append(Paragraph("Figure 1. Deployment surfaces and responsibility boundaries.", st["caption"]))


def add_sections(story, st):
    section(story, st, "Executive Summary")
    story.append(
        p(
            "Arculus Recovery is an offline recovery and key-derivation suite for BIP39 mnemonics, BIP32 account structures, BIP86 Taproot derivation, multi-coin address generation, encrypted seed backup, and offline export workflows. Its primary design objective is to minimize operational trust by allowing users to inspect, transfer, verify, and run the tool without network connectivity or hosted infrastructure.",
            st["body"],
        )
    )
    story.append(
        p(
            "The suite is organized around a canonical browser application, a Python command-line and desktop compatibility layer, and a Tauri desktop package. The HTML application is the primary user-facing interface. The Python GUI renders that same HTML interface through PySide6 WebEngine, and the Tauri package wraps a generated copy of the same interface while adding a native export bridge for save dialogs. This architecture avoids separate GUI behavior forks while preserving a scriptable Python derivation engine for command-line users.",
            st["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Central conclusion.</b> Arculus Recovery is best understood as an offline, user-verifiable recovery workstation rather than a network service. Its security posture depends on deterministic local computation, verified distribution artifacts, disciplined offline operation, and clear separation between seed material, derived outputs, encrypted backups, and release packaging.",
            st["callout"],
        )
    )
    story.append(
        bullets(
            [
                "Runs without hosted APIs, telemetry, analytics, or remote signing services during normal use.",
                "Supports standalone HTML use, Python CLI use, PySide6 GUI use, and Tauri desktop package use.",
                "Derives Bitcoin, Litecoin, Dogecoin, Ethereum, ERC-20-compatible account keys, and XRP addresses from BIP39 seed material.",
                "Exports derived outputs in JSON, CSV, TXT, PDF, encrypted seed, and QR-oriented formats depending on surface.",
                "Publishes SHA256 hashes for source, build-support assets, and packaged release artifacts to support independent verification.",
            ],
            st,
        )
    )

    section(story, st, "Scope and Non-Goals")
    story.append(
        p(
            "The application suite is designed for offline recovery, migration, verification, and controlled export. It is not a wallet, transaction signer, network broadcaster, portfolio tracker, exchange connector, or cloud backup service. This narrow scope is a security feature: avoiding network connectivity and custodial flows reduces the number of trust boundaries crossed while a user handles seed material.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Area", "In Scope", "Out of Scope"],
                ["Seed handling", "BIP39 validation, random mnemonic generation, passphrase-aware seed derivation, hidden imported-seed workflows", "Cloud seed storage, account recovery services, seed synchronization"],
                ["Key derivation", "BIP32/BIP44/BIP49/BIP84/BIP86-style account and child derivation, Arculus-native m/0' path behavior", "Online balance lookup, transaction signing, network broadcasting"],
                ["Export", "Local JSON, CSV, TXT, PDF, QR PNG, and encrypted .arc outputs", "Remote upload, hosted sharing links, third-party key management"],
                ["Packaging", "Source files, offline HTML, Python package metadata, Tauri desktop packages", "App-store distribution guarantees, notarization policy beyond documented verification"],
            ],
            [1.25 * inch, 2.55 * inch, 2.55 * inch],
        )
    )

    section(story, st, "System Architecture")
    story.append(
        p(
            "The suite uses a layered architecture. The canonical HTML application owns the interactive recovery interface and browser-based export logic. The Python package contains derivation, formatting, encryption, and command-line workflows. The PySide6 shell loads the canonical HTML app rather than reimplementing UI behavior. The Tauri package prepares a static WebView bundle from the canonical HTML and injects a native export bridge for file-save operations.",
            st["body"],
        )
    )
    add_architecture_diagram(story, st)
    subsection(story, st, "Canonical HTML Surface")
    story.append(
        p(
            "The HTML file is intentionally self-contained for direct browser use. Its PDF library is embedded inline, and its derivation, validation, QR, export, theme, and settings logic run locally. Direct file opening remains a primary deployment model because it lets users place the artifact on removable media, verify its hash, disconnect from the internet, and run the interface without installing an application package.",
            st["body"],
        )
    )
    subsection(story, st, "Python Package and Compatibility Launcher")
    story.append(
        p(
            "The root Python launcher is a compatibility shim that adds the src package path and delegates to arculus_recovery.cli.safe_main. CLI mode is available for deterministic derivation workflows, scripted verification, and text-based exports. GUI mode depends on PySide6 and renders the canonical HTML application in a desktop window, preserving visual and behavioral parity with browser use.",
            st["body"],
        )
    )
    subsection(story, st, "Tauri Package")
    story.append(
        p(
            "The Tauri package wraps the generated HTML distribution in a native shell. Its main native value is the export bridge: browser-style Blob downloads can be unreliable in desktop WebViews, so the Tauri build exposes save_export through a Rust command and native Save dialog. That command decodes base64 export data, sanitizes filenames, offers extension-specific filters, and writes only to the user-selected path.",
            st["body"],
        )
    )

    section(story, st, "Cryptographic Model")
    story.append(
        p(
            "The cryptographic design separates mnemonic validation, seed derivation, hierarchical key derivation, address encoding, encrypted backup, and QR/export representation. This separation makes it easier to reason about which operations require secrecy, which operations produce public or semi-public material, and which artifacts become sensitive once exported.",
            st["body"],
        )
    )
    subsection(story, st, "Mnemonic and Seed Processing")
    story.append(
        p(
            "BIP39 mnemonic validation verifies word count, word-list membership, entropy/checksum consistency, and passphrase-aware seed generation. The BIP39 passphrase is treated as part of the recovery secret: the same mnemonic with different passphrases produces different wallet roots. The application therefore avoids treating a valid mnemonic alone as sufficient proof that the user has selected the intended wallet.",
            st["body"],
        )
    )
    subsection(story, st, "Hierarchical Derivation")
    story.append(
        p(
            "BIP32 private child derivation is used to produce account-level and address-level keys. The suite supports common account templates for UTXO networks and script-aware variants for legacy, nested SegWit, native SegWit, and Taproot address families where applicable. Ethereum and XRP exports are represented using their respective address formats rather than WIF.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Output family", "Typical path family", "Private key representation", "Address representation"],
                ["Bitcoin", "m/44', m/49', m/84', m/86' or m/0'", "WIF and hex", "Base58Check, Bech32, or Bech32m depending on script"],
                ["Litecoin", "BIP44/BIP49/BIP84-style account paths", "WIF and hex", "Network-specific Base58Check or Bech32"],
                ["Dogecoin", "BIP44-style account paths", "WIF and hex", "Dogecoin Base58Check"],
                ["Ethereum", "m/44'/60'/0'/0/i", "Hex", "Keccak-derived EIP-55-style checksum address"],
                ["XRP", "m/44'/144'/0'/0/i", "Hex", "XRP classic address encoding"],
            ],
            [1.15 * inch, 1.8 * inch, 1.55 * inch, 1.85 * inch],
        )
    )
    subsection(story, st, "Encrypted Seed Backup")
    story.append(
        p(
            "The .arc export format is a local encrypted backup for mnemonic material. Current exports use a structured armored representation that includes versioned metadata, KDF parameters, salt, nonce, ciphertext, and authentication material. The model favors explicit KDF description and authenticated decryption failures over implicit or ambiguous file handling.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "Password-derived keys are separated by purpose so encryption and authentication do not reuse identical key material.",
                "Legacy import compatibility is maintained where documented, but users should re-export into the current format after successful recovery.",
                "Encrypted seed backups remain sensitive because their security is bounded by password quality, KDF cost, and custody of the file.",
            ],
            st,
        )
    )

    section(story, st, "Security Architecture")
    subsection(story, st, "Offline-First Assumption")
    story.append(
        p(
            "The primary security assumption is that users can run the suite on a trusted machine while disconnected from the internet. The application does not require network APIs to validate mnemonics, derive keys, create QR codes, or export files. This does not eliminate local compromise risk, but it removes remote request paths from normal recovery operation.",
            st["body"],
        )
    )
    subsection(story, st, "Sensitive Data Classes")
    story.append(
        table(
            [
                ["Data class", "Sensitivity", "Handling guidance"],
                ["Mnemonic words and BIP39 passphrase", "Critical", "Enter only on a trusted offline machine; clear after use; never paste into networked services."],
                ["Seed bytes and root private keys", "Critical", "Keep in process memory only; export only when intentionally creating backups."],
                ["Account private keys and WIF values", "Critical", "Treat exported tables and PDFs as wallet-equivalent material."],
                ["Extended public keys", "Medium-High", "Do not publish; they can reveal account activity and future receiving addresses."],
                ["Addresses and QR codes", "Low-Medium", "Public on-chain identifiers but linkable across activity and accounts."],
                ["Encrypted .arc files", "High", "Protect as encrypted backups; password strength matters."],
            ],
            [1.75 * inch, 1.05 * inch, 3.55 * inch],
        )
    )
    subsection(story, st, "Trust Boundaries")
    story.append(
        p(
            "Trust boundaries are intentionally local: the browser sandbox, the Python process, the WebEngine profile, the Tauri WebView, the native save dialog, and the filesystem. The suite does not claim to defend against malware with process inspection capability, compromised operating systems, hostile clipboard managers, malicious browser extensions, or tampered distribution artifacts that the user has not verified.",
            st["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>Security posture.</b> Hash verification, offline execution, short recovery sessions, and controlled exports are complementary controls. None of them independently protects a user who enters seed material on a compromised machine.",
            st["callout"],
        )
    )

    section(story, st, "Threat Model")
    story.append(
        p(
            "The most important threats are local compromise, artifact tampering, user workflow mistakes, and uncontrolled export sprawl. Network attackers are less central because the application does not depend on network traffic during normal use; however, network distribution remains relevant before the user obtains and verifies release files.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Threat", "Impact", "Mitigation"],
                ["Trojanized copy from mirror or attachment", "Critical seed compromise", "Verify SHA256 hashes from a trusted release; prefer repository tags and release assets."],
                ["Compromised workstation", "Critical seed compromise", "Use a clean offline system; minimize clipboard use; reboot or power down after session."],
                ["Browser extension or injected script", "Seed or private key capture", "Use a browser profile without extensions or use packaged desktop build after hash verification."],
                ["Accidental export retention", "Long-lived private key exposure", "Store outputs only on intended encrypted media; delete temporary exports; avoid cloud-synced folders."],
                ["Weak .arc password", "Offline password guessing", "Use high-entropy passwords; treat .arc files as sensitive even though encrypted."],
                ["Wrong path or passphrase", "Funds appear missing", "Verify with known addresses; document derivation path and passphrase policy."],
            ],
            [1.8 * inch, 1.75 * inch, 2.8 * inch],
        )
    )

    section(story, st, "Operational Security Guidance")
    story.append(
        p(
            "Operational security is the main differentiator between a safe recovery session and a dangerous one. The suite can compute keys offline, but the user must still control the environment, storage media, passphrase handling, and post-session cleanup.",
            st["body"],
        )
    )
    subsection(story, st, "Recommended Recovery Ceremony")
    story.append(
        bullets(
            [
                "Prepare a trusted machine, preferably freshly installed or booted from trusted removable media.",
                "Obtain release files from the repository or release page and verify SHA256 hashes before opening them.",
                "Disconnect networking before entering mnemonic words or passphrases.",
                "Enter or import seed material, derive the minimum necessary outputs, and verify expected addresses.",
                "Export only what is required; prefer encrypted storage for any private-key-bearing file.",
                "Clear the application state, close the app or browser tab, remove temporary files, and power down the machine after use.",
            ],
            st,
        )
    )
    subsection(story, st, "Export Discipline")
    story.append(
        p(
            "PDF exports, JSON exports, CSV exports, TXT exports, QR PNGs, and encrypted seed files have different sensitivity levels. A PDF or CSV containing private keys should be handled like a wallet backup. A QR code may encode a public address, BIP21-style URI, or XRP address plus destination tag; users should inspect the displayed value before scanning or sharing.",
            st["body"],
        )
    )

    section(story, st, "Release and Verification Model")
    story.append(
        p(
            "The release model publishes both source/build-support hashes and packaged artifact hashes. Source hashes support users who run the HTML or Python project directly. Packaged artifact hashes support users who install Tauri desktop builds. Because the README hash block is part of the repository, it must be updated after any final source, manual, icon, asset, or packaged artifact change.",
            st["body"],
        )
    )
    story.append(
        Paragraph(
            "Representative verification command:<br/><font name='Courier'>find Arculus_Recovery.html Arculus_Recovery.py src/arculus_recovery vendor/jspdf scripts/prepare_tauri_assets.py src-tauri/tauri.conf.json src-tauri/icons docs/Arculus_Recovery_Manual.pdf -type f ! -name '._*' -print0 | sort -z | xargs -0 shasum -a 256</font>",
            st["callout"],
        )
    )
    subsection(story, st, "GitHub Upload Set")
    story.append(
        p(
            "A GitHub-ready release folder should contain source files, documentation, workflows, packaging metadata, Tauri source/configuration, icons, vendored jsPDF, and selected release artifacts. It should exclude .git, old Documentation paths, build targets, generated Tauri schemas, tauri-dist, Python caches, AppleDouble metadata, and local tree dumps.",
            st["body"],
        )
    )

    section(story, st, "Data Lifecycle and State Management")
    story.append(
        p(
            "A recovery tool should be evaluated by the complete lifecycle of secret material: entry, normalization, validation, derivation, display, export, clearing, and post-session residue. Arculus Recovery reduces long-lived state by avoiding account creation, remote storage, browser databases for seeds, or background services. The main persistent browser state is the interface preference, not recovery material.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Lifecycle stage", "Primary risk", "Control"],
                ["Entry", "Shoulder-surfing, keylogging, clipboard interception", "Word-grid entry, hidden imported-seed workflow, offline trusted machine guidance"],
                ["Normalization", "Different Unicode forms or whitespace changing seed interpretation", "Mnemonic normalization before validation and seed derivation"],
                ["Validation", "False confidence from valid word list but invalid checksum", "Word count, word-list, checksum, and derived fingerprint feedback"],
                ["Derivation", "Wrong account namespace or script family", "Explicit coin, path, script-type, branch, range, and account-output display"],
                ["Display", "Private material visible longer than intended", "Hold-to-reveal patterns and clear-all workflow"],
                ["Export", "Private keys written into uncontrolled locations", "Explicit format selection, native save dialogs, hashable release artifacts, and export warnings"],
                ["Cleanup", "Residual files or copied secrets", "Clear All, close session, remove temporary exports, and power-down guidance"],
            ],
            [1.35 * inch, 2.25 * inch, 2.75 * inch],
        )
    )

    section(story, st, "Implementation Assurance")
    story.append(
        p(
            "The suite's assurance posture comes from simplicity, inspectability, deterministic behavior, and repeatable release artifacts. The code avoids hidden server authority and exposes enough intermediate context for users to reason about what was derived. Assurance is not equivalent to a formal audit; rather, it is a set of engineering choices that make independent review and offline verification practical.",
            st["body"],
        )
    )
    subsection(story, st, "Determinism and Reviewability")
    story.append(
        bullets(
            [
                "Mnemonic validation and deterministic derivation should produce stable output for the same mnemonic, passphrase, coin, path, branch, and index.",
                "Source files and packaged assets are hashable without relying on a build server response.",
                "The canonical HTML app can be opened and inspected directly, which helps reviewers compare browser, PySide6, and Tauri behavior.",
                "Release notes document behavior changes that affect QR encoding, export defaults, derivation display, and desktop packaging.",
            ],
            st,
        )
    )
    subsection(story, st, "Failure Modes")
    story.append(
        table(
            [
                ["Failure mode", "User-visible symptom", "Recommended diagnostic"],
                ["Wrong passphrase", "Valid mnemonic derives unexpected addresses", "Retry with passphrase policy used by original wallet; compare known receiving address"],
                ["Wrong script family", "Addresses valid but use different prefix or witness version", "Try common account paths and script-type variants for the coin"],
                ["Wrong account or branch index", "Expected address absent from first range", "Use range derivation and inspect receiving/change branches"],
                ["Corrupt .arc password or file", "Authentication/decryption failure", "Verify backup source and password; do not bypass authentication errors"],
                ["Desktop WebView export quirk", "Download does not appear or saves to unexpected path", "Use Tauri native export bridge and verify resulting file hash/contents"],
                ["Release hash mismatch", "Local artifact hash differs from README", "Stop; re-download from trusted source or rebuild and regenerate published hashes"],
            ],
            [1.55 * inch, 2.3 * inch, 2.5 * inch],
        )
    )

    section(story, st, "User Interface Safety Model")
    story.append(
        p(
            "The interface is part of the security model. Recovery applications should make dangerous operations explicit, keep user choices visible, and avoid hiding private-key-bearing output behind friendly labels. Arculus Recovery surfaces the active coin, path, root fingerprint, output table, extended keys, export format, theme, and QR payload so users can verify what the tool is about to derive or export.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "The root fingerprint helps users distinguish one wallet root from another without exposing the full seed.",
                "The output table keeps path and branch visible so receiving and change addresses are not confused.",
                "QR generation displays the payload value so users can review address schemes and XRP destination-tag behavior.",
                "Theme selection is persisted for usability, while seed material is not intentionally persisted in browser storage.",
                "Clear All is treated as an operational control, not as cryptographic erasure of a compromised host.",
            ],
            st,
        )
    )

    section(story, st, "Desktop Packaging Considerations")
    story.append(
        p(
            "Desktop packaging improves ergonomics but introduces native-platform verification requirements. Windows users should verify the standalone executable, NSIS setup executable, or MSI hash before launch. macOS users should verify the DMG hash and then evaluate signing/notarization status according to their local policy. Linux packages should be built on native Linux runners with required WebKit/GTK dependencies.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Platform", "Primary artifacts", "Release checks"],
                ["Windows", "Standalone .exe, setup .exe, MSI", "Hash verification, installer launch, export save smoke test"],
                ["macOS", "aarch64 DMG, x64 DMG, universal DMG, .app bundles", "Hash verification, architecture check, codesign/ad-hoc signature check, DMG verification"],
                ["Linux", "AppImage, deb, rpm, optional binary", "Native runner build, dependency check, launch/export smoke test"],
            ],
            [1.1 * inch, 2.2 * inch, 3.05 * inch],
        )
    )

    section(story, st, "Build Reproducibility and Artifact Custody")
    story.append(
        p(
            "A release package is only as trustworthy as the path used to produce, store, and publish it. The project separates source verification from binary artifact verification because they answer different questions. Source hashes answer 'did these inspectable files change?' Packaged hashes answer 'is this installer or DMG byte-for-byte the artifact that was published?'",
            st["body"],
        )
    )
    subsection(story, st, "Recommended Custody Pattern")
    story.append(
        bullets(
            [
                "Build platform-native desktop artifacts on native runners rather than cross-copying mutable build directories.",
                "Keep release artifact hashes in README synchronized with the final upload set, not with an intermediate build folder.",
                "Treat generated target directories, WebView staging folders, and schema caches as build byproducts rather than source release material.",
                "Exclude AppleDouble metadata, local tree dumps, caches, and temporary exports from GitHub upload folders.",
                "After upload, download the published release assets back from GitHub and verify their hashes against the release documentation.",
            ],
            st,
        )
    )

    section(story, st, "Interoperability and Recovery Correctness")
    story.append(
        p(
            "Recovery correctness depends on more than mnemonic validity. Users must know the intended passphrase, coin, derivation path, account index, script type, and address branch. The suite exposes common derivation families and an Arculus-native path, but a mismatch in any of these choices can produce valid keys for a different account namespace.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "Always test with a known address from the original wallet before assuming funds are absent.",
                "Record whether the original wallet used a BIP39 passphrase.",
                "Differentiate account-level extended keys from child private keys.",
                "For XRP deposits to exchanges, distinguish the classic address from the destination tag.",
                "For Ethereum-style accounts, remember that token balances share the same account key but require separate on-chain lookup outside this offline tool.",
            ],
            st,
        )
    )

    section(story, st, "Limitations")
    story.append(
        p(
            "The suite cannot prove that a machine is uncompromised, cannot validate live balances without network access, cannot notarize its own builds, and cannot recover funds when a user supplies the wrong mnemonic, passphrase, coin, path, or account model. It intentionally avoids online discovery because online discovery would expand the trust boundary and expose recovery sessions to remote dependencies.",
            st["body"],
        )
    )

    section(story, st, "Assurance Matrix")
    story.append(
        p(
            "The following matrix summarizes the evidence users and maintainers can collect before trusting a release. It is not a replacement for cryptographic review, but it provides concrete release gates that are observable by non-maintainers.",
            st["body"],
        )
    )
    story.append(
        table(
            [
                ["Assurance question", "Evidence", "Residual risk"],
                ["Did the source tree change after hashes were published?", "Run README source hash command in the release folder", "A malicious publisher could alter both files and hashes before users notice"],
                ["Do desktop artifacts match the release notes?", "Run packaged artifact hash command and compare filenames", "Hash match does not prove source reproducibility"],
                ["Does CLI derivation still work?", "Run a known BIP39 test mnemonic and inspect JSON output", "Smoke tests do not prove every coin/path combination"],
                ["Do WebView exports work?", "Save PDF, JSON, CSV, TXT, .arc, and QR PNG from packaged builds", "Manual tests may miss platform-specific edge cases"],
                ["Are docs free of stale paths?", "Search for old Documentation path, version mismatches, and mojibake", "Documentation can still omit newly introduced behavior"],
            ],
            [2.05 * inch, 2.45 * inch, 1.85 * inch],
        )
    )
    story.append(
        table(
            [
                ["Limitation", "Reason", "Recommended response"],
                ["No online balance discovery", "Network isolation is part of the security model", "Use a separate watch-only wallet or block explorer after recovery, without exposing private material."],
                ["No protection from local malware", "Malware can inspect memory, keystrokes, files, or clipboard", "Use a trusted offline machine and minimize session duration."],
                ["No universal path discovery guarantee", "Wallets vary in account and script conventions", "Try documented common paths and verify against known addresses."],
                ["No password recovery for .arc", "Encrypted backups rely on the user password", "Store password hints separately and use high-entropy password management."],
            ],
            [1.65 * inch, 2.25 * inch, 2.45 * inch],
        )
    )

    section(story, st, "Appendix A - Release Checklist")
    story.append(
        bullets(
            [
                "Run Python syntax checks and CLI smoke derivation.",
                "Run Tauri asset preparation and verify generated assets load.",
                "Run cargo test and fresh Tauri builds on target platforms.",
                "Smoke-test browser HTML offline, PySide6 GUI, and packaged desktop exports.",
                "Verify PDF, JSON, CSV, TXT, .arc, and QR PNG save flows.",
                "Regenerate all README hashes after final source and artifact changes.",
                "Remove generated build directories, caches, AppleDouble metadata, and local-only files from upload folders.",
            ],
            st,
        )
    )

    section(story, st, "Appendix B - Glossary")
    story.append(
        table(
            [
                ["Term", "Meaning"],
                ["BIP39", "Mnemonic and seed derivation standard based on word lists, checksum, and PBKDF2-HMAC-SHA512."],
                ["BIP32", "Hierarchical deterministic wallet standard for deriving child keys from parent keys."],
                ["BIP86", "Taproot single-key wallet derivation convention."],
                [".arc", "Arculus encrypted seed backup file format."],
                ["WIF", "Wallet Import Format for UTXO private keys."],
                ["xpub/zpub/ypub", "Extended public key encodings associated with account discovery and script families."],
                ["Destination tag", "XRP routing metadata commonly required by exchanges and custodial platforms."],
            ],
            [1.35 * inch, 5.0 * inch],
        )
    )

    section(story, st, "Appendix C - Maintenance Principles")
    story.append(
        p(
            "Future changes should preserve offline operation, keep the canonical HTML surface authoritative, avoid hidden network behavior, maintain source/package parity, and update verification material at the end of each release cycle. Any cryptographic change should be reviewed as a compatibility and safety event, not as an ordinary UI enhancement.",
            st["body"],
        )
    )


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, 0.45 * inch, "WhitePaper - Arculus Recovery v1.5.0")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    st = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.65 * inch,
        title="WhitePaper",
        author="",
        subject="Arculus Recovery technical white paper",
    )
    story = [
        Spacer(1, 1.45 * inch),
        Paragraph("WhitePaper", st["title"]),
        Paragraph("Arculus Recovery v1.5.0", st["subtitle"]),
        Paragraph(
            "Offline BIP39/BIP32 recovery, deterministic derivation, encrypted seed backup, QR export, and desktop packaging architecture",
            st["subtitle"],
        ),
        Paragraph("Generated June 7, 2026", st["kicker"]),
        Spacer(1, 0.18 * inch),
        Rule(),
        Spacer(1, 0.18 * inch),
        Paragraph(
            "This white paper describes the architecture, cryptographic model, security posture, operational controls, release process, and limitations of the Arculus Recovery application suite.",
            st["callout"],
        ),
        PageBreak(),
    ]
    add_sections(story, st)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    try:
        from pypdf import PdfReader, PdfWriter

        reader = PdfReader(str(OUT))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(
            {
                "/Title": "WhitePaper",
                "/Subject": "Arculus Recovery technical white paper",
                "/Creator": "",
                "/Producer": "ReportLab PDF Library - pypdf metadata scrub",
            }
        )
        tmp = OUT.with_suffix(".tmp.pdf")
        with tmp.open("wb") as fh:
            writer.write(fh)
        tmp.replace(OUT)
    except Exception:
        pass


if __name__ == "__main__":
    build()
