from __future__ import annotations

from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageTemplate,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "YellowSphere_Manual.pdf"
LOGO = ROOT / "src-tauri" / "icons" / "icon.png"
VERSION = "1.6.6"

DOC_ORDER = [
    "Recovery.txt",
    "OpSec.txt",
    "LinuxRelease.txt",
    "BuildReproducability.txt",
    "Passphrase.txt",
    "FileFormat.txt",
    "Encryption.txt",
    "Derivation.txt",
    "QR.txt",
    "TestVectors.txt",
]

SCREENSHOTS = [
    ("yellowsphere-main-recovery.png", "Figure 1. Main recovery workspace with test-vector mnemonic validation controls."),
    ("yellowsphere-derived-output.png", "Figure 2. Derived output table after address derivation, with output tabs and export controls."),
    ("yellowsphere-qr-export.png", "Figure 3. QR Export modal generating an address QR code without external services."),
    ("yellowsphere-settings.png", "Figure 4. Settings dialog with theme selection and advanced recovery preferences."),
    ("yellowsphere-light.png", "Figure 5. Light theme interface."),
    ("yellowsphere-dark.png", "Figure 6. Dark theme interface."),
    ("yellowsphere-dark-plus.png", "Figure 7. Dark+ theme interface."),
    ("yellowsphere-terminal.png", "Figure 8. Terminal theme interface."),
]


def clean_text(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u00d7": "x",
        "\u2265": ">=",
        "\u2208": "in",
        "\u00b7": ".",
        "\ufffd": "?",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def first_heading(lines: list[str], index: int) -> tuple[str | None, int]:
    if index + 1 >= len(lines):
        return None, 0
    underline = lines[index + 1].strip()
    if lines[index].strip() and len(underline) >= 3:
        if set(underline) <= {"="}:
            return lines[index].strip(), 1
        if set(underline) <= {"-"}:
            return lines[index].strip(), 2
    return None, 0


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ManualTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=35,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "ManualSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=12,
        ),
        "kicker": ParagraphStyle(
            "ManualKicker",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#B45309"),
            spaceAfter=8,
        ),
        "toc_title": ParagraphStyle(
            "ManualTocTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#111827"),
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "ManualH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "ManualH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "ManualBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
            spaceAfter=5,
        ),
        "lead": ParagraphStyle(
            "ManualLead",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=8,
        ),
        "diagram_title": ParagraphStyle(
            "ManualDiagramTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3,
        ),
        "diagram_box": ParagraphStyle(
            "ManualDiagramBox",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=9.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
        ),
        "diagram_arrow": ParagraphStyle(
            "ManualDiagramArrow",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#B45309"),
        ),
        "diagram_note": ParagraphStyle(
            "ManualDiagramNote",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=9.5,
            textColor=colors.HexColor("#374151"),
            spaceAfter=6,
        ),
        "caption": ParagraphStyle(
            "ManualCaption",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4B5563"),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "code": ParagraphStyle(
            "ManualCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=8.8,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#F3F4F6"),
            borderColor=colors.HexColor("#D1D5DB"),
            borderWidth=0.25,
            borderPadding=5,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "ManualBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.5,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "note": ParagraphStyle(
            "ManualNote",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.5,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#FEF3C7"),
            borderColor=colors.HexColor("#F59E0B"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "toc_l1": ParagraphStyle(
            "ManualTocLevel1",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=3,
        ),
        "toc_l2": ParagraphStyle(
            "ManualTocLevel2",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            leftIndent=18,
            firstLineIndent=0,
            textColor=colors.HexColor("#374151"),
        ),
    }


ENCRYPTION_DIAGRAMS = [
    {
        "title": "ARC V3 Password Mode",
        "steps": [
            "Password\nUTF-8(NFKD)",
            "SHA-512\npre-hash",
            "PBKDF2-HMAC-SHA512\nsalt 32 bytes\n1,000,000 iterations",
            "AES-256-GCM key\n32 bytes",
            ".arc metadata as AAD\nciphertext_b64 = 512 bytes + 16-byte tag",
        ],
        "note": "The normalized mnemonic JSON is zero-padded to 512 bytes before AES-GCM encryption. Metadata key order is authenticated by additionalData.",
    },
    {
        "title": "ARC V3 Keyfile Mode",
        "steps": [
            "Keyfile bytes",
            "ASCII credential\narc-keyfile-v1:<base64>",
            "HKDF-SHA512\nsalt 32 bytes\ninfo: YellowSphere ARC v3 AES-256-GCM key",
            "AES-256-GCM key\n32 bytes",
            ".arc metadata as AAD\ncredential_mode = keyfile",
        ],
        "note": "The complete ASCII credential string is the HKDF input key material; the raw keyfile is not stored in the .arc payload.",
    },
    {
        "title": "ARC V3 Keyfile + Password Mode",
        "steps": [
            "keyfile_bytes || UTF8(NFKD(password))",
            "HKDF-SHA512\ninfo: yellowsphere-arc-v3-combined-key\nlen 64",
            "combined_secret\narc-combined-v1:<base64>",
            "HKDF-SHA512\nARC AES-key info\nlen 32",
            "AES-256-GCM key\ncredential_mode = both",
        ],
        "note": "Combined mode first builds a 64-byte combined secret and then follows the ARC V3 HKDF AES-key derivation path.",
    },
    {
        "title": "Encrypted-Keyfile Version 2",
        "steps": [
            "Keyfile plaintext\n64 bytes",
            "Password\nUTF-8(NFKD) -> SHA-512",
            "PBKDF2-HMAC-SHA512\nsalt 16 bytes\n1,000,000 iterations",
            "AES-256-GCM\nnonce 12 bytes\nAAD magic+format",
            "ciphertext_b64\n64 bytes + 16-byte tag",
        ],
        "note": "The encrypted keyfile keeps magic and format strings stable while version 2 selects AES-256-GCM and the SHA-512 password pre-hash.",
    },
]


COIN_DERIVATION_DIAGRAMS = [
    {
        "coin": "Bitcoin",
        "path": "m/0'",
        "family": "BIP39 seed -> secp256k1 BIP32, HMAC-SHA512 key 'Bitcoin seed'",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "P2PKH, P2WPKH-P2SH, P2WPKH, or P2TR address"],
        "note": "Auto script type follows path purpose; testnet script defaults use coin type 1 paths.",
    },
    {
        "coin": "Bitcoin Cash",
        "path": "m/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "HASH160", "CashAddr bitcoincash:q... or legacy Base58"],
        "note": "Only P2PKH is supported; the legacy-address toggle changes display/export encoding, not private-key derivation.",
    },
    {
        "coin": "Litecoin",
        "path": "m/84'/2'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "Litecoin P2PKH, nested SegWit, native SegWit, or P2TR"],
        "note": "Mainnet uses Litecoin version bytes where applicable; native SegWit uses ltc Bech32 HRP.",
    },
    {
        "coin": "Dogecoin",
        "path": "m/44'/3'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "HASH160", "Dogecoin Base58 address"],
        "note": "Dogecoin uses Dogecoin BIP32 versions and WIF prefixes; Taproot is not configured.",
    },
    {
        "coin": "Ethereum / ERC-20",
        "path": "m/44'/60'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "uncompressed public key", "Keccak-256 public-key tail", "0x EIP-55-style account address"],
        "note": "ERC-20 tokens use the same Ethereum account address; token state is not queried.",
    },
    {
        "coin": "BNB Chain",
        "path": "m/44'/60'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Ethereum-compatible account node", "branch 0/1", "index i", "uncompressed public key", "Keccak-256", "0x EVM address"],
        "note": "BNB Chain shares the Ethereum coin type and address construction in YellowSphere.",
    },
    {
        "coin": "Avalanche C-Chain",
        "path": "m/44'/60'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Ethereum-compatible account node", "branch 0/1", "index i", "uncompressed public key", "Keccak-256", "0x EVM address"],
        "note": "Only the C-Chain EVM account format is represented; no X-Chain or P-Chain discovery is performed.",
    },
    {
        "coin": "Polygon",
        "path": "m/44'/60'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Ethereum-compatible account node", "branch 0/1", "index i", "uncompressed public key", "Keccak-256", "0x EVM address"],
        "note": "Polygon PoS uses the same secp256k1 account key and 0x address form as Ethereum.",
    },
    {
        "coin": "Tron / TRC-20",
        "path": "m/44'/195'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "uncompressed public key", "Keccak-256 public-key tail", "0x41-prefixed payload", "Base58Check T... address"],
        "note": "TRC-20 tokens use the same Tron account address; the hex address is also exported.",
    },
    {
        "coin": "Cosmos / ATOM",
        "path": "m/44'/118'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "HASH160", "Bech32 HRP cosmos address"],
        "note": "YellowSphere derives account addresses only; staking state, validators, and balances are external.",
    },
    {
        "coin": "Solana",
        "path": "m/44'/501'/0'",
        "family": "BIP39 seed -> SLIP-0010 Ed25519 hardened derivation",
        "steps": ["Ed25519 master key", "hardened account path", "accountPathForIndex / direct path", "Ed25519 public key", "Base58 address"],
        "note": "SLIP-0010 Ed25519 derivation accepts hardened path indexes only.",
    },
    {
        "coin": "Stellar",
        "path": "m/44'/148'/0'",
        "family": "BIP39 seed -> SLIP-0010 Ed25519 hardened derivation",
        "steps": ["Ed25519 master key", "hardened account path", "accountPathForIndex", "Ed25519 public key", "StrKey public address + secret seed"],
        "note": "The exported Stellar secret seed is derived from the same Ed25519 child key.",
    },
    {
        "coin": "Cardano",
        "path": "m/1852'/1815'/0'/0/0",
        "family": "Mnemonic entropy + passphrase -> Cardano Icarus Ed25519-BIP32",
        "steps": ["Icarus root from entropy", "payment path", "staking path", "payment and stake public keys", "Shelley base address addr... / addr_test..."],
        "note": "Cardano uses CIP-1852 style paths and builds a Shelley base address from payment and staking keys.",
    },
    {
        "coin": "XRP",
        "path": "m/44'/144'/0'",
        "family": "BIP39 seed -> secp256k1 BIP32",
        "steps": ["Account node", "branch 0/1", "index i", "compressed public key", "account identifier", "XRP classic r... address"],
        "note": "Destination tags are never derived and must be supplied separately by exchanges or custodians.",
    },
]


class ManualDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, styles, **kwargs):
        self.styles = styles
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
            showBoundary=0,
        )
        self.addPageTemplates([PageTemplate(id="Manual", frames=[frame], onPage=header_footer)])

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        level_by_style = {"ManualH1": 0, "ManualH2": 1}
        level = level_by_style.get(flowable.style.name)
        if level is None:
            return
        text = flowable.getPlainText()
        key = getattr(flowable, "_bookmarkName", None)
        if level > 0:
            return
        if key:
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (level, text, self.page, key))
        else:
            self.notify("TOCEntry", (level, text, self.page))


def heading(text: str, style, key_prefix: str, sequence: int) -> Paragraph:
    paragraph = Paragraph(escape(text), style)
    paragraph._bookmarkName = f"{key_prefix}-{sequence}"
    return paragraph


def classify_block(block: list[str]) -> str:
    stripped = [line.rstrip() for line in block]
    if not stripped:
        return "blank"
    non_empty = [line for line in stripped if line.strip()]
    if not non_empty:
        return "blank"
    if all(re.match(r"^\s*(-|\d+\.|\[[ xX]\])\s+", line) for line in non_empty):
        return "list"
    if any(line.startswith("  ") or line.startswith("\t") for line in stripped):
        return "code"
    if len(non_empty) >= 2 and any("  " in line.strip() for line in non_empty):
        return "code"
    return "para"


def add_text_doc(story, path: Path, styles, slug: str):
    text = clean_text(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    i = 0
    pending: list[str] = []
    heading_count = 0

    def flush():
        nonlocal pending
        if not pending:
            return
        kind = classify_block(pending)
        if kind == "list":
            items = []
            for line in pending:
                content = re.sub(r"^\s*(-|\d+\.|\[[ xX]\])\s+", "", line).strip()
                items.append(ListItem(Paragraph(escape(content), styles["bullet"])))
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=18, bulletFontSize=5))
        elif kind == "code":
            story.append(Preformatted(clean_text("\n".join(pending)).rstrip(), styles["code"], maxLineLength=92))
        elif kind == "para":
            paragraph = " ".join(line.strip() for line in pending if line.strip())
            style = styles["note"] if paragraph.startswith(("Note:", "Security note:", "Desktop wrapper requirement:")) else styles["body"]
            story.append(Paragraph(escape(paragraph), style))
        pending = []

    while i < len(lines):
        heading_text, level = first_heading(lines, i)
        if heading_text:
            flush()
            heading_count += 1
            story.append(heading(heading_text, styles["h1" if level == 1 else "h2"], slug, heading_count))
            i += 2
            continue
        if not lines[i].strip():
            flush()
        else:
            pending.append(lines[i])
        i += 1
    flush()


def add_screenshots(story, styles):
    story.append(PageBreak())
    story.append(heading("Interface Guide", styles["h1"], "interface", 1))
    story.append(
        Paragraph(
            "The screenshots below show the primary user-facing layout and theme variants. "
            "The HTML application is the canonical GUI surface. PySide6 and Tauri package "
            "the same interface for desktop use, so the screenshots apply to all GUI editions.",
            styles["lead"],
        )
    )
    max_width = 6.7 * inch
    max_height = 3.45 * inch
    for filename, caption in SCREENSHOTS:
        image_path = DOCS / "screenshots" / filename
        if not image_path.exists():
            continue
        img = Image(str(image_path))
        scale = min(max_width / img.imageWidth, max_height / img.imageHeight)
        img.drawWidth = img.imageWidth * scale
        img.drawHeight = img.imageHeight * scale
        figure = Table(
            [[img], [Paragraph(escape(caption), styles["caption"])]],
            colWidths=[max_width],
            style=TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
                    ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
                    ("LINEBELOW", (0, 0), (0, 0), 0.35, colors.HexColor("#E5E7EB")),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ]
            ),
        )
        story.append(KeepTogether([figure, Spacer(1, 0.08 * inch)]))


def flow_diagram(title: str, steps: list[str], note: str, styles, box_color="#FFFBEB"):
    max_width = 6.7 * inch
    rows = [[Paragraph(escape(title), styles["diagram_title"])]]
    for index, step in enumerate(steps):
        rows.append([Paragraph(escape(step).replace("\n", "<br/>"), styles["diagram_box"])])
        if index < len(steps) - 1:
            rows.append([Paragraph("=>", styles["diagram_arrow"])])
    if note:
        rows.append([Paragraph(escape(note), styles["diagram_note"])])
    style_commands = [
        ("SPAN", (0, 0), (0, 0)),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F3F4F6")),
    ]
    for row_idx in range(1, len(rows)):
        cell_text = rows[row_idx][0].getPlainText()
        if cell_text == "=>":
            style_commands.extend(
                [
                    ("BACKGROUND", (0, row_idx), (0, row_idx), colors.HexColor("#FFFFFF")),
                    ("TOPPADDING", (0, row_idx), (0, row_idx), 1),
                    ("BOTTOMPADDING", (0, row_idx), (0, row_idx), 1),
                ]
            )
        elif note and cell_text == note:
            style_commands.append(("BACKGROUND", (0, row_idx), (0, row_idx), colors.HexColor("#F9FAFB")))
        else:
            style_commands.extend(
                [
                    ("BACKGROUND", (0, row_idx), (0, row_idx), colors.HexColor(box_color)),
                    ("BOX", (0, row_idx), (0, row_idx), 0.35, colors.HexColor("#F59E0B")),
                ]
            )
    return Table(rows, colWidths=[max_width], style=TableStyle(style_commands))


def coin_diagram(coin: dict, styles):
    display_path = escape(coin["path"]).replace("'", "&#39;")
    rows = [
        [Paragraph(escape(coin["coin"]), styles["diagram_title"]), Paragraph(f"Default path: {display_path}", styles["diagram_note"])],
        [Paragraph("Derivation family", styles["diagram_box"]), Paragraph(escape(coin["family"]), styles["diagram_note"])],
    ]
    for step_index, step in enumerate(coin["steps"], start=1):
        rows.append([Paragraph(str(step_index), styles["diagram_arrow"]), Paragraph(escape(step), styles["diagram_box"])])
    rows.append([Paragraph("Note", styles["diagram_box"]), Paragraph(escape(coin["note"]), styles["diagram_note"])])
    return Table(
        rows,
        colWidths=[0.85 * inch, 5.85 * inch],
        style=TableStyle(
            [
                ("SPAN", (0, 0), (0, 0)),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
                ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#FFFBEB")),
                ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#FFFFFF")),
                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
                ("INNERGRID", (0, 1), (-1, -1), 0.25, colors.HexColor("#E5E7EB")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        ),
    )


def add_encryption_diagrams(story, styles):
    story.append(PageBreak())
    story.append(heading("Encryption Scheme Diagrams", styles["h1"], "encryption-diagrams", 1))
    story.append(
        Paragraph(
            "These diagrams summarize the protected seed and encrypted keyfile paths before the byte-level specification. "
            "They do not replace the normative field ordering, lengths, and validation rules in the Encryption Subsystem Internals section.",
            styles["lead"],
        )
    )
    for diagram in ENCRYPTION_DIAGRAMS:
        story.append(KeepTogether([flow_diagram(diagram["title"], diagram["steps"], diagram["note"], styles), Spacer(1, 0.1 * inch)]))


def add_coin_derivation_diagrams(story, styles):
    story.append(PageBreak())
    story.append(heading("Coin Derivation Diagrams", styles["h1"], "coin-derivation-diagrams", 1))
    story.append(
        Paragraph(
            "Each production v1.6.6 coin below shows the deterministic route from mnemonic material to exported address rows. "
            "The diagrams preserve the implementation defaults while leaving the full byte-level mechanics in the Derivation Engine Internals section.",
            styles["lead"],
        )
    )
    for index, coin in enumerate(COIN_DERIVATION_DIAGRAMS):
        story.append(KeepTogether([coin_diagram(coin, styles), Spacer(1, 0.1 * inch)]))
        if index in (4, 9):
            story.append(PageBreak())


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.restoreState()
        return
    canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, letter[1] - 0.45 * inch, letter[0] - doc.rightMargin, letter[1] - 0.45 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, 0.45 * inch, f"YellowSphere v{VERSION} Programmer's Manual")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def add_cover(story, styles):
    story.append(Spacer(1, 0.85 * inch))
    if LOGO.exists():
        logo = Image(str(LOGO), width=0.9 * inch, height=0.9 * inch)
        story.append(Table([[logo]], colWidths=[6.7 * inch], style=TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")])))
        story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph("OFFLINE RECOVERY REFERENCE", styles["kicker"]))
    story.append(Paragraph(f"YellowSphere v{VERSION}", styles["title"]))
    story.append(Paragraph("Programmer's Manual and User Guide", styles["subtitle"]))
    story.append(
        Paragraph(
            "A shelf-ready guide to the standalone HTML application, Python wrapper, Tauri desktop package, "
            "cryptographic export formats, deterministic derivation behavior, QR workflows, and operational procedures.",
            styles["subtitle"],
        )
    )
    story.append(Spacer(1, 0.18 * inch))
    story.append(
        Table(
            [
                ["Primary GUI", "Standalone HTML application"],
                ["Desktop GUI", "PySide6 WebEngine wrapper"],
                ["Desktop Package", "Tauri wrapper with native export bridge"],
                ["CLI", "Python derivation and export interface"],
                ["Manual Scope", "User workflow plus byte-faithful technical reference sections"],
                ["Generated", "June 18, 2026"],
            ],
            colWidths=[1.6 * inch, 4.9 * inch],
            style=TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                    ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#374151")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
                    ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#D97706")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#FCD34D")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )
    story.append(PageBreak())


def add_toc(story, styles):
    story.append(Paragraph("Contents", styles["toc_title"]))
    story.append(
        Paragraph(
            "Use this guide from front to back for operational setup, or jump directly to the reference sections "
            "when validating exact derivation, encryption, file-format, QR, and test-vector behavior.",
            styles["lead"],
        )
    )
    toc = TableOfContents()
    toc.levelStyles = [styles["toc_l1"], styles["toc_l2"]]
    story.append(toc)
    story.append(PageBreak())


def build():
    styles = make_styles()
    doc = ManualDocTemplate(
        str(OUT),
        styles,
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.65 * inch,
        title=f"YellowSphere v{VERSION} Programmer's Manual and User Guide",
        author="YellowSphere",
    )

    story = []
    add_cover(story, styles)
    add_toc(story, styles)

    add_text_doc(story, DOCS / "UserGuide.txt", styles, "user-guide")
    add_screenshots(story, styles)
    add_encryption_diagrams(story, styles)
    add_coin_derivation_diagrams(story, styles)

    for doc_name in DOC_ORDER:
        story.append(PageBreak())
        add_text_doc(story, DOCS / doc_name, styles, doc_name.lower().replace(".", "-"))

    doc.multiBuild(story)


if __name__ == "__main__":
    build()
