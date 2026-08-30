from pathlib import Path

OUT = Path(__file__).resolve().parent

A4_W = 595.276
A4_H = 841.89
SVG_W = 794
SVG_H = 1123
CHOICES = ["A", "B", "C", "D", "E"]

TEMPLATES = {
    "20q": {
        "title": "SmartGrade 20-Question Standard Template",
        "subtitle": "Two-column OMR answer sheet with a 9-digit student ID grid",
        "student_rect": (0.18, 0.20, 0.64, 0.25),
        "id_radius": 0.014,
        "bubble_radius": 0.016,
        "choice_spacing_x": 0.062,
        "questions": [
            (q, 0.12 if q <= 10 else 0.56, 0.54 + ((q - 1) if q <= 10 else (q - 11)) * 0.038)
            for q in range(1, 21)
        ],
    },
    "50q": {
        "title": "SmartGrade 50-Question Standard Template",
        "subtitle": "Two-column OMR answer sheet with a 9-digit student ID grid",
        "student_rect": (0.20, 0.14, 0.60, 0.24),
        "id_radius": 0.012,
        "bubble_radius": 0.012,
        "choice_spacing_x": 0.065,
        "questions": [
            (q, 0.10 if q <= 25 else 0.55, 0.44 + ((q - 1) if q <= 25 else (q - 26)) * 0.021)
            for q in range(1, 51)
        ],
    },
}

MARKERS = [(0.05, 0.04), (0.95, 0.04), (0.05, 0.96), (0.95, 0.96)]
MARKER_SIZE = 0.035


def svg_xy(x: float, y: float) -> tuple[float, float]:
    return x * SVG_W, y * SVG_H


def pdf_xy(x: float, y: float) -> tuple[float, float]:
    return x * A4_W, A4_H - y * A4_H


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_svg(key: str, tpl: dict) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" viewBox="0 0 {SVG_W} {SVG_H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(tpl["title"])}</title>',
        '<desc id="desc">Printable SmartGrade Scanner OMR template showing alignment markers, student ID grid, and answer bubbles.</desc>',
        '<rect width="100%" height="100%" fill="#f6f8fb"/>',
        '<rect x="32" y="28" width="730" height="1068" rx="18" fill="white" stroke="#d0d7de" stroke-width="2"/>',
        f'<text x="397" y="78" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#0f172a">{esc(tpl["title"])}</text>',
        f'<text x="397" y="108" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="15" fill="#475569">{esc(tpl["subtitle"])}</text>',
        '<text x="397" y="136" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#64748b">Fill bubbles completely with a dark pen. Keep the sheet flat and aligned when scanning.</text>',
    ]

    marker_px = MARKER_SIZE * SVG_W
    for mx, my in MARKERS:
        cx, cy = svg_xy(mx, my)
        parts.append(f'<rect x="{cx - marker_px / 2:.1f}" y="{cy - marker_px / 2:.1f}" width="{marker_px:.1f}" height="{marker_px:.1f}" rx="4" fill="#111827"/>')

    sx, sy, sw, sh = tpl["student_rect"]
    gx, gy = svg_xy(sx, sy)
    gw, gh = sw * SVG_W, sh * SVG_H
    parts.extend([
        f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}" rx="10" fill="#eff6ff" stroke="#60a5fa" stroke-width="2"/>',
        f'<text x="{gx + gw / 2:.1f}" y="{gy - 14:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#1d4ed8">Student ID Grid (9 columns × 10 digits)</text>',
    ])

    cols, rows = 9, 10
    col_w, row_h = gw / cols, gh / rows
    id_r = tpl["id_radius"] * SVG_W
    for c in range(cols):
        parts.append(f'<text x="{gx + (c + 0.5) * col_w:.1f}" y="{gy - 32:.1f}" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">D{c + 1}</text>')
    for row in range(rows):
        parts.append(f'<text x="{gx - 14:.1f}" y="{gy + (row + 0.5) * row_h + 4:.1f}" text-anchor="middle" font-family="Arial" font-size="11" fill="#64748b">{row}</text>')
        for c in range(cols):
            cx = gx + (c + 0.5) * col_w
            cy = gy + (row + 0.5) * row_h
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{id_r:.1f}" fill="white" stroke="#2563eb" stroke-width="1.4"/>')

    parts.append('<text x="115" y="430" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="700" fill="#0f172a">Answers</text>')
    q_r = tpl["bubble_radius"] * SVG_W
    spacing = tpl["choice_spacing_x"] * SVG_W
    for q, start_x, y in tpl["questions"]:
        x, yy = svg_xy(start_x, y)
        parts.append(f'<text x="{x - 38:.1f}" y="{yy + 5:.1f}" text-anchor="end" font-family="Arial" font-size="12" font-weight="700" fill="#334155">Q{q}</text>')
        for idx, choice in enumerate(CHOICES):
            cx = x + idx * spacing
            parts.append(f'<circle cx="{cx:.1f}" cy="{yy:.1f}" r="{q_r:.1f}" fill="white" stroke="#111827" stroke-width="1.3"/>')
            parts.append(f'<text x="{cx:.1f}" y="{yy + q_r + 14:.1f}" text-anchor="middle" font-family="Arial" font-size="8" fill="#64748b">{choice}</text>')

    parts.extend([
        '<rect x="56" y="1035" width="682" height="34" rx="8" fill="#f1f5f9"/>',
        '<text x="397" y="1057" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#475569">Generated from SmartGradeScanner/Services/DefaultTemplateFactory.swift coordinates.</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text_cmd(x: float, y: float, text: str, size: float = 10, align: str = "left") -> str:
    approx_width = len(text) * size * 0.52
    if align == "center":
        x -= approx_width / 2
    elif align == "right":
        x -= approx_width
    return f"BT /F1 {size:.1f} Tf {x:.2f} {y:.2f} Td ({pdf_escape(text)}) Tj ET"


def circle_cmd(cx: float, cy: float, r: float) -> str:
    k = 0.5522847498
    return (
        f"{cx + r:.2f} {cy:.2f} m "
        f"{cx + r:.2f} {cy + k * r:.2f} {cx + k * r:.2f} {cy + r:.2f} {cx:.2f} {cy + r:.2f} c "
        f"{cx - k * r:.2f} {cy + r:.2f} {cx - r:.2f} {cy + k * r:.2f} {cx - r:.2f} {cy:.2f} c "
        f"{cx - r:.2f} {cy - k * r:.2f} {cx - k * r:.2f} {cy - r:.2f} {cx:.2f} {cy - r:.2f} c "
        f"{cx + k * r:.2f} {cy - r:.2f} {cx + r:.2f} {cy - k * r:.2f} {cx + r:.2f} {cy:.2f} c S"
    )


class PDF:
    def __init__(self) -> None:
        self.objects: list[bytes] = []

    def add(self, content: str | bytes) -> int:
        if isinstance(content, str):
            content = content.encode("latin-1")
        self.objects.append(content)
        return len(self.objects)

    def add_stream(self, content: str) -> int:
        data = content.encode("latin-1")
        return self.add(b"<< /Length " + str(len(data)).encode("ascii") + b" >>\nstream\n" + data + b"\nendstream")

    def write(self, path: Path, root_obj: int) -> None:
        body = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for idx, obj in enumerate(self.objects, 1):
            offsets.append(len(body))
            body.extend(f"{idx} 0 obj\n".encode("ascii"))
            body.extend(obj)
            body.extend(b"\nendobj\n")
        xref = len(body)
        body.extend(f"xref\n0 {len(self.objects) + 1}\n".encode("ascii"))
        body.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            body.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        body.extend(f"trailer\n<< /Size {len(self.objects) + 1} /Root {root_obj} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
        path.write_bytes(body)


def make_pdf(path: Path, tpl: dict) -> None:
    cmds: list[str] = [
        "1 1 1 rg 0 0 595.28 841.89 re f",
        "0.82 0.84 0.88 RG 1.2 w 24 24 547.28 793.89 re S",
        text_cmd(A4_W / 2, 790, tpl["title"], 18, "center"),
        text_cmd(A4_W / 2, 768, tpl["subtitle"], 10, "center"),
        text_cmd(A4_W / 2, 752, "Fill bubbles completely with a dark pen. Keep the page flat and aligned.", 8.5, "center"),
    ]

    marker = MARKER_SIZE * A4_W
    cmds.append("0 0 0 rg")
    for mx, my in MARKERS:
        cx, cy = pdf_xy(mx, my)
        cmds.append(f"{cx - marker / 2:.2f} {cy - marker / 2:.2f} {marker:.2f} {marker:.2f} re f")

    sx, sy, sw, sh = tpl["student_rect"]
    gx = sx * A4_W
    gy_top = A4_H - sy * A4_H
    gw = sw * A4_W
    gh = sh * A4_H
    gy = gy_top - gh
    cmds.extend([
        "0.12 0.37 0.72 RG 1.1 w",
        f"{gx:.2f} {gy:.2f} {gw:.2f} {gh:.2f} re S",
        text_cmd(gx + gw / 2, gy_top + 10, "Student ID Grid (9 columns x 10 digits)", 11, "center"),
    ])

    cols, rows = 9, 10
    col_w, row_h = gw / cols, gh / rows
    id_r = tpl["id_radius"] * A4_W
    for c in range(cols):
        cmds.append(text_cmd(gx + (c + 0.5) * col_w, gy_top + 23, f"D{c + 1}", 6, "center"))
    for row in range(rows):
        cy = gy_top - (row + 0.5) * row_h
        cmds.append(text_cmd(gx - 12, cy - 2, str(row), 6, "center"))
        for c in range(cols):
            cx = gx + (c + 0.5) * col_w
            cmds.append(circle_cmd(cx, cy, id_r))

    cmds.append(text_cmd(70, 530, "Answers", 13))
    cmds.append("0 0 0 RG 0.85 w")
    q_r = tpl["bubble_radius"] * A4_W
    spacing = tpl["choice_spacing_x"] * A4_W
    for q, start_x, y in tpl["questions"]:
        x, yy = pdf_xy(start_x, y)
        cmds.append(text_cmd(x - 27, yy - 3, f"Q{q}", 7, "right"))
        for idx, choice in enumerate(CHOICES):
            cx = x + idx * spacing
            cmds.append(circle_cmd(cx, yy, q_r))
            cmds.append(text_cmd(cx, yy - q_r - 9, choice, 5, "center"))

    cmds.append(text_cmd(A4_W / 2, 38, "Generated from SmartGradeScanner/Services/DefaultTemplateFactory.swift coordinates.", 7.5, "center"))
    content = "\n".join(cmds)

    pdf = PDF()
    pages = pdf.add("<< /Type /Pages /Kids [] /Count 1 >>")
    font = pdf.add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    stream = pdf.add_stream(content)
    page = pdf.add(f"<< /Type /Page /Parent {pages} 0 R /MediaBox [0 0 {A4_W:.2f} {A4_H:.2f}] /Resources << /Font << /F1 {font} 0 R >> >> /Contents {stream} 0 R >>")
    pdf.objects[pages - 1] = f"<< /Type /Pages /Kids [{page} 0 R] /Count 1 >>".encode("latin-1")
    catalog = pdf.add(f"<< /Type /Catalog /Pages {pages} 0 R >>")
    pdf.write(path, catalog)


def main() -> None:
    for key, tpl in TEMPLATES.items():
        (OUT / f"smartgrade-template-{key}.svg").write_text(make_svg(key, tpl), encoding="utf-8")
        make_pdf(OUT / f"smartgrade-template-{key}.pdf", tpl)

    print("Generated template assets:")
    for path in sorted(OUT.glob("smartgrade-template-*.*")):
        print(f"- {path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()