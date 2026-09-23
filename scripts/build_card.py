"""Render the neofetch-style profile card to assets/card-{dark,light}.svg.

Edit FIELDS / PROJECTS below, then run: python3 scripts/build_card.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

USER = "jakub@quantumkuba"

FIELDS = [
    ("Role", "PhD researcher · Artificial Intelligence"),
    ("Focus", "Retrieval-augmented generation, LLM evaluation"),
    ("Also", "AI safety, bias & robustness auditing"),
    ("Building", "DeRAG · agentic RAG · research tooling"),
    ("Stack", "Python · TypeScript · PyTorch · React · Postgres"),
    ("Motto", "Measure carefully. Explain clearly. Ship responsibly."),
]

PROJECTS = [
    ("NLS-RAG", "retrieval research"),
    ("obsidian-brainhack", "knowledge tooling"),
]

THEMES = {
    "dark": {
        "bg": "#0b1622",
        "border": "#1c3347",
        "text": "#d6e4ee",
        "muted": "#6f8799",
        "accent": "#00c2a8",
        "accent2": "#4aa8ff",
        "orbit": "#2a5878",
        "blocks": ["#1c3347", "#ff6b6b", "#3ddc97", "#f7c948", "#4aa8ff", "#b48cff", "#00c2a8", "#d6e4ee"],
    },
    "light": {
        "bg": "#f7fafc",
        "border": "#d3dee6",
        "text": "#1b2a36",
        "muted": "#6b7f8e",
        "accent": "#008f7c",
        "accent2": "#1f6fc4",
        "orbit": "#a9c2d4",
        "blocks": ["#1b2a36", "#d64545", "#1f9d68", "#c99a06", "#1f6fc4", "#7a4fd1", "#008f7c", "#b8c6d1"],
    },
}

W, H = 1000, 480
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FS = 15
CHAR_W = FS * 0.6  # typical monospace advance width
TEXT_X = 370
RULE_END = W - 40


def heading(y, label, c):
    x_end = TEXT_X + len(label) * CHAR_W + 10
    return (
        f'<text x="{TEXT_X}" y="{y}" fill="{c["accent"]}" font-weight="bold">{escape(label)}</text>'
        f'<line x1="{x_end:.0f}" y1="{y - 5}" x2="{RULE_END}" y2="{y - 5}" stroke="{c["border"]}" />'
    )


def row(y, key, value, c, value_x, key_color=None):
    dots_from = TEXT_X + len(key) * CHAR_W + 8
    return (
        f'<text x="{TEXT_X}" y="{y}" fill="{key_color or c["accent2"]}">{escape(key)}</text>'
        f'<line x1="{dots_from:.0f}" y1="{y - 4}" x2="{value_x - 10:.0f}" y2="{y - 4}" '
        f'stroke="{c["muted"]}" stroke-dasharray="1 5" stroke-linecap="round" />'
        f'<text x="{value_x:.0f}" y="{y}" fill="{c["text"]}">{escape(value)}</text>'
    )


def emblem(c):
    """Animated retrieval graph: a query node pulling signal from document nodes."""
    cx, cy = 180, 205
    docs = [(-110, -95), (-5, -150), (105, -100), (135, 15), (85, 120), (-30, 145), (-130, 55), (-145, -25)]
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0), (1, 3), (5, 7)]
    parts = [f'<g transform="translate({cx} {cy})">']
    for r in (70, 152):
        parts.append(f'<circle r="{r}" fill="none" stroke="{c["orbit"]}" stroke-dasharray="2 6" opacity=".7" />')
    for a, b in links:
        (x1, y1), (x2, y2) = docs[a], docs[b]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["orbit"]}" opacity=".6" />')
    for i, (x, y) in enumerate(docs):
        color = c["accent2"] if i % 2 else c["accent"]
        # edge to the query node, with a signal flowing inwards
        parts.append(
            f'<line x1="{x}" y1="{y}" x2="0" y2="0" stroke="{c["orbit"]}" stroke-width="1.5" />'
            f'<line x1="{x}" y1="{y}" x2="0" y2="0" stroke="{color}" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-dasharray="6 400" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="0;-190" dur="2.4s" '
            f'begin="{-i * 0.3:.1f}s" repeatCount="indefinite" /></line>'
        )
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="9" fill="{c["bg"]}" stroke="{color}" stroke-width="2.5">'
            f'<animate attributeName="opacity" values="1;.45;1" dur="2.4s" begin="{-i * 0.3:.1f}s" '
            f'repeatCount="indefinite" /></circle>'
        )
    parts.append(
        f'<circle r="30" fill="{c["accent"]}" opacity=".15">'
        f'<animate attributeName="r" values="24;36;24" dur="2.4s" repeatCount="indefinite" />'
        f"</circle>"
        f'<circle r="17" fill="{c["accent"]}" />'
        f'<circle cx="-2" cy="-2" r="6" fill="none" stroke="{c["bg"]}" stroke-width="2.5" />'
        f'<line x1="2.5" y1="2.5" x2="8" y2="8" stroke="{c["bg"]}" stroke-width="3" stroke-linecap="round" />'
    )
    parts.append("</g>")
    parts.append(
        f'<text x="{cx}" y="{cy + 200}" text-anchor="middle" fill="{c["muted"]}" '
        f'font-size="13">retrieval · reasoning · reliability</text>'
    )
    return "".join(parts)


def render(c):
    y = 62
    body = [
        f'<text x="{TEXT_X}" y="{y}" fill="{c["accent"]}" font-weight="bold">{USER}</text>',
        f'<line x1="{TEXT_X + len(USER) * CHAR_W + 10:.0f}" y1="{y - 5}" x2="{RULE_END}" y2="{y - 5}" stroke="{c["border"]}" />',
    ]
    y += 36
    value_x = TEXT_X + max(len(k) for k, _ in FIELDS) * CHAR_W + 32
    for key, value in FIELDS:
        body.append(row(y, key, value, c, value_x))
        y += 26
    y += 22
    body.append(heading(y, "Selected work", c))
    y += 32
    value_x = TEXT_X + max(len(k) for k, _ in PROJECTS) * CHAR_W + 32
    for key, value in PROJECTS:
        body.append(row(y, key, value, c, value_x, key_color=c["accent"]))
        y += 26
    y += 18
    for i, color in enumerate(c["blocks"]):
        body.append(f'<rect x="{TEXT_X + i * 34}" y="{y}" width="34" height="16" fill="{color}" />')

    prompt_y = H - 26
    prompt = "visitor@quantumkuba:~$"
    cursor_x = 24 + len(prompt) * CHAR_W + 6
    footer = (
        f'<line x1="0" y1="{H - 54}" x2="{W}" y2="{H - 54}" stroke="{c["border"]}" />'
        f'<text x="24" y="{prompt_y}" fill="{c["muted"]}">visitor@<tspan fill="{c["accent"]}">quantumkuba</tspan>:~$</text>'
        f'<rect x="{cursor_x:.0f}" y="{prompt_y - 13}" width="9" height="17" fill="{c["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite" />'
        f"</rect>"
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}" font-size="{FS}" role="img" aria-label="Jakub (QuantumKuba) profile card">'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}" />'
        f"{emblem(c)}{''.join(body)}{footer}</svg>\n"
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, colors in THEMES.items():
        (out / f"card-{name}.svg").write_text(render(colors), encoding="utf-8")
        print(f"wrote assets/card-{name}.svg")
