#!/usr/bin/env python3
"""Generate the README hero assets for dsh-plugin-dev (docs/assets/).

Outputs (idempotent overwrite):
  dsh-plugin-dev-flow-light.svg
  dsh-plugin-dev-flow-dark.svg
      Hero dispatcher diagram. Two hand-written SVG files (vector — never
      rasterized to webp), one per GitHub theme. Every label is a command
      token (dsh-dev new, dsh-plugin-start, DSH_HOME, ...), so all five
      README languages share the same pair.

Pillow and the CJK font probe are part of the family skeleton: every
PerryLink asset generator must fail loudly instead of silently rendering
Chinese as tofu boxes, even when the current asset happens to be
ASCII-only.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow (pip install pillow)
"""
from __future__ import annotations

import os
import sys

from PIL import ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

# --- palette: PerryLink family (accent) + GitHub page backgrounds ----------
FAMILY = "#4B67B4"   # family accent (badges use labelColor #2B3245)
GREEN = {"light": "#16a34a", "dark": "#3fb950"}
SKIN = {
    "light": dict(bg="#ffffff", box="#f6f8fa", border="#d0d7de",
                  text="#1f2328", sub="#57606a"),
    "dark": dict(bg="#0d1117", box="#161b22", border="#30363d",
                 text="#f0f6fc", sub="#8b949e"),
}

# --- CJK font probe: Chinese must never render as tofu boxes ----------------
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",      # Microsoft YaHei
    r"C:\Windows\Fonts\simhei.ttf",    # SimHei
    r"C:\Windows\Fonts\Deng.ttf",      # DengXian
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
if FONT_PATH is None:
    sys.exit("FATAL: no CJK font found (looked for msyh.ttc, simhei.ttf, "
             "Deng.ttf, Noto Sans CJK, PingFang). Refusing to render Chinese "
             "as tofu boxes; install one of the probed fonts and re-run.")


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


# ---------------------------------------------------------------------------
# 1. Hero dispatcher SVG (light + dark)
# ---------------------------------------------------------------------------
# (subcommand token, where it goes). Command-surface tokens only: no prose,
# so the same pair serves zh / en / es / pt / hi.
ROWS = [
    ("dsh-dev new", "dsh-plugin-start"),
    ("dsh-dev check", "dsh-plugin-ready"),
    ("dsh-dev tools", "dsh-plugin-tools"),
    ("dsh-dev test", "temp DSH_HOME · add → dump-config → remove"),
    ("dsh-dev submit", "entry-validate · compat subset"),
    ("dsh-dev upgrade", "dsh-codemod"),
]
MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    w, h = 1200, 600
    hub_x, hub_y, hub_w, hub_h = 60, 150, 210, 362
    card_x, card_w, card_h, step = 430, 710, 52, 62
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="dsh-dev dispatch flow">',
        '<title>dsh-plugin-dev dispatch flow</title>',
        f'<rect width="{w}" height="{h}" rx="18" fill="{s["bg"]}"/>',
        f'<text x="60" y="64" fill="{s["text"]}" '
        f'font-family="ui-sans-serif,system-ui,sans-serif" '
        f'font-size="32" font-weight="700">dsh-plugin-dev</text>',
        f'<text x="60" y="97" fill="{s["sub"]}" font-family="{MONO}" '
        f'font-size="15">dsh-dev new · check · tools · test · submit · '
        f'upgrade</text>',
        f'<line x1="60" y1="118" x2="1140" y2="118" stroke="{s["border"]}"/>',
    ]

    # hub: one executable at the centre
    parts.append(
        f'<rect x="{hub_x}" y="{hub_y}" width="{hub_w}" height="{hub_h}" '
        f'rx="16" fill="{s["box"]}" stroke="{FAMILY}" stroke-width="2"/>')
    parts.append(
        f'<text x="{hub_x + hub_w // 2}" y="{hub_y + 168}" '
        f'fill="{s["text"]}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="26" font-weight="700">dsh-dev</text>')
    parts.append(
        f'<text x="{hub_x + hub_w // 2}" y="{hub_y + 196}" '
        f'fill="{s["sub"]}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="12">bin/dsh-dev.js</text>')

    for i, (token, target) in enumerate(ROWS):
        y = hub_y + i * step
        cy = y + card_h // 2
        in_repo = i in (3, 4)  # test / submit are orchestrated in this repo
        parts.append(
            f'<path d="M{hub_x + hub_w} {cy}h{card_x - hub_x - hub_w - 14}" '
            f'stroke="{s["sub"]}" stroke-width="2"/>')
        parts.append(
            f'<path d="M{card_x} {cy}l-11 -6v12z" fill="{s["sub"]}"/>')
        parts.append(
            f'<rect x="{card_x}" y="{y}" width="{card_w}" '
            f'height="{card_h}" rx="12" fill="{s["box"]}" '
            f'stroke="{FAMILY if in_repo else s["border"]}" '
            f'stroke-width="2"/>')
        parts.append(
            f'<text x="{card_x + 24}" y="{cy + 6}" fill="{FAMILY}" '
            f'font-family="{MONO}" font-size="17" font-weight="700">'
            f'{token}</text>')
        parts.append(
            f'<text x="{card_x + 260}" y="{cy + 5}" fill="{s["sub"]}" '
            f'font-family="{MONO}" font-size="13">{target}</text>')

    parts.append(
        f'<text x="60" y="570" fill="{s["sub"]}" font-family="{MONO}" '
        f'font-size="13">exit 0 pass · 2 fail · 3 blocked</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    # Guard: the probed font must load, so a future text-bearing asset in
    # this repo can never fall back to tofu boxes.
    font(13).getbbox("dsh-dev")
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        with open(os.path.join(OUT, f"dsh-plugin-dev-flow-{skin}.svg"),
                  "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
    print("wrote 2 SVG assets to docs/assets/ "
          "(dsh-plugin-dev-flow-{light,dark}.svg)")


if __name__ == "__main__":
    main()
