"""
build_pdf.py — Render homework-cost-estimator-EXPLAINED.md to a print-ready PDF.

Converts the markdown to styled HTML, then prints it to PDF with headless
Microsoft Edge or Google Chrome (whichever is installed). No external services.

Usage:
    python build_pdf.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_MD = os.path.join(HERE, "homework-cost-estimator-EXPLAINED.md")
OUT_PDF = os.path.join(HERE, "homework-cost-estimator-EXPLAINED.pdf")

# Print-optimised stylesheet: light background (saves ink, reads on paper), brand accents,
# clean tables, sensible page margins and page-break behaviour.
CSS = """
@page { size: A4; margin: 18mm 16mm 20mm; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1b2733; font-size: 11.5pt; line-height: 1.55; margin: 0;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 { font-size: 25pt; line-height: 1.15; margin: 0 0 4pt; letter-spacing: -.5pt; color: #0b3a5b; }
h2 { font-size: 16pt; margin: 22pt 0 6pt; padding-bottom: 4pt; border-bottom: 2px solid #5ec8ff;
     color: #0b3a5b; page-break-after: avoid; }
h3 { font-size: 12.5pt; margin: 14pt 0 4pt; color: #134a72; page-break-after: avoid; }
p { margin: 6pt 0; }
a { color: #1769aa; text-decoration: none; }
strong { color: #0b2e47; }
code { font-family: "Cascadia Code", "Consolas", monospace; font-size: 10pt;
       background: #eef3f7; border: 1px solid #d8e2ea; border-radius: 4px; padding: 1px 5px; }
hr { border: none; border-top: 1px solid #d8e2ea; margin: 18pt 0; }
ul, ol { margin: 6pt 0 6pt 4pt; padding-left: 18pt; }
li { margin: 3pt 0; }
blockquote { margin: 10pt 0; padding: 8pt 14pt; background: #fff8e6; border-left: 4px solid #d29922;
             border-radius: 0 6px 6px 0; color: #5c4a16; }
blockquote p { margin: 2pt 0; }
table { width: 100%; border-collapse: collapse; margin: 10pt 0; font-size: 10pt;
        page-break-inside: avoid; }
th { background: #0b3a5b; color: #fff; text-align: left; padding: 6pt 8pt; font-weight: 600; }
td { padding: 6pt 8pt; border-bottom: 1px solid #e3eaf0; vertical-align: top; }
tr:nth-child(even) td { background: #f6f9fb; }
table code { background: #fff; }
h2, h3, table, blockquote { page-break-inside: avoid; }
.doc-meta { color: #6b7888; font-size: 9.5pt; margin: 2pt 0 14pt;
            border-bottom: 1px solid #d8e2ea; padding-bottom: 12pt; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><style>{css}</style></head>
<body>
<div class="doc-meta">ClevStudy Tutor Engine · Homework Help (Tier 2) · cost-estimator companion guide</div>
{body}
</body></html>"""


def find_browser() -> str | None:
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    candidates = [
        os.path.join(pf, r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe"),
        os.path.join(pf, r"Google\Chrome\Application\chrome.exe"),
        os.path.join(pf86, r"Google\Chrome\Application\chrome.exe"),
    ]
    return next((c for c in candidates if os.path.exists(c)), None)


def main() -> int:
    with open(SRC_MD, "r", encoding="utf-8") as f:
        md_text = f.read()

    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
    )
    html = HTML_TEMPLATE.format(css=CSS, body=body)

    tmp_html = os.path.join(tempfile.gettempdir(), "homework-cost-estimator-explained.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    browser = find_browser()
    if not browser:
        print("No Edge/Chrome found. The styled HTML is at:", tmp_html)
        print("Open it and use the browser's 'Print > Save as PDF'.")
        return 1

    cmd = [
        browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={OUT_PDF}", f"file:///{tmp_html.replace(os.sep, '/')}",
    ]
    print("Rendering PDF with:", os.path.basename(browser))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if os.path.exists(OUT_PDF) and os.path.getsize(OUT_PDF) > 0:
        print("PDF written:", OUT_PDF, f"({os.path.getsize(OUT_PDF):,} bytes)")
        return 0
    print("PDF generation failed.\n", result.stdout, result.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
