#!/usr/bin/env python3
"""README visuals for dsh-plugin-dev — v5 (1440x576 hero + 1100x660 flow).

Both figures come from the code, not from a template:

  bin/dsh-dev.js    main(process.argv.slice(2)) -> process.exitCode
  src/dev.js        token compare: new|start, check|ready and tools call the
                    bundled npm deps' main() in-process; upgrade probes
                    where/which dsh-codemod; test -> src/host-test.js and
                    submit -> src/submit.js are the two commands this repo
                    really orchestrates
  src/host-test.js  package.json gate -> dsh/pnpm gate -> mkdtemp DSH_HOME
                    (refuses the real ~/.dsh) -> add -> dump-config ->
                    [--boot URL] -> remove -> finally rm; blocked / fail /
                    pass-with-warnings / pass; dsh-evidence/1
  src/submit.js     findStandards: --standards | $DSH_STANDARDS_DIR | sibling
                    dsh-plugin-spec|dsh-standard|dsh-standards checkouts at
                    four depths -> vendored entry-validate.mjs -> compat C1-C8

  hero  (Pillow, zh/en x light/dark) — the dispatch board. A prompt bar
        ($ dsh-dev, argv.slice(2)) sits above a six-row route table: one row
        per verb, each with the target it reaches and its route class
        (import / local / probe). Every row collapses into the four exit lamps
        the whole CLI is reduced to.

  flow  (hand-written SVG, light/dark) — an *unbalanced dispatch tree*, not a
        row of boxes: argv root, one bus, then a shallow 2x2 hand-off subtree
        (four leaves that leave this repository, 70px tall) beside a deep
        orchestration subtree (test's six-step temp-DSH_HOME chain and
        submit's five-rung checker ladder, 330px tall). The depth difference is
        the point: the repo barely implements the left half. Both halves return
        one number into the process.exitCode rail.

Labels are command tokens plus short Chinese notes, so the light/dark SVG pair
is shared by all five README languages; only the hero carries prose (zh / en).

Outputs (idempotent overwrite):
  docs/assets/dsh-plugin-dev-hero-{zh,en}-{light,dark}.webp
  docs/assets/dsh-plugin-dev-flow-v5-{light,dark}.svg

Run:  python scripts/gen-readme-assets.py
Needs: Pillow, plus msyh.ttc / msyhbd.ttc / consola.ttf (a CJK font is
       mandatory: Chinese must never render as tofu boxes).
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'assets')

FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_CJK_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
FONT_MONO = r'C:\Windows\Fonts\consola.ttf'
FONT_EN = r'C:\Windows\Fonts\segoeui.ttf'
FONT_EN_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_EN, FONT_EN_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f'FATAL: font missing: {_p}  (CJK must never render '
                         f'as tofu boxes; install the font and re-run)')

KIND = {'cjk': FONT_CJK, 'cjk_bold': FONT_CJK_BOLD, 'mono': FONT_MONO,
        'en': FONT_EN, 'en_bold': FONT_EN_BOLD}

# --- palette: family accent + the two mandated page gradients ---------------
SKIN = {
    'light': dict(bg_from='#f9f6fd', bg_to='#e4eaf8', card='#ffffff',
                  card_edge='#e4e1ee', zone='#f7f5fc', text='#141419',
                  sub='#4d5261', faint='#8f94a4', accent='#4B67B4',
                  accent2='#6d80c4', ok='#16a34a', warn='#bc4c00',
                  fail='#cf222e', pill='#ece7f9', grid='#e7e4f0',
                  shadow=(32, 26, 64)),
    'dark': dict(bg_from='#131a2a', bg_to='#0c1016', card='#1b2231',
                 card_edge='#2e374b', zone='#202839', text='#f0f3f9',
                 sub='#a8b1c4', faint='#737b8d', accent='#8496f5',
                 accent2='#a9b7f8', ok='#3fb950', warn='#d29922',
                 fail='#f85149', pill='#242d42', grid='#2a3348',
                 shadow=(0, 0, 0)),
}


def font(size: float, kind: str = 'cjk_bold') -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(KIND[kind], int(round(size)))


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    img = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = 0.2 * (y / h) + 0.8 * (y / h) ** 1.5
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(hx(c1), hx(c2))))
    return img


def glow(img: Image.Image, cx: int, cy: int, r: int, color, alpha: int = 30):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(9, 0, -1):
        rr = r * i / 9
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (1 - i / 10)),))
    return Image.alpha_composite(img.convert('RGBA'),
                                 layer).convert('RGB')


def card(img, box, skin, radius=20, shadow=16, fill=None, edge=None, width=2):
    """Rounded card with a soft, offset shadow."""
    x0, y0, x1, y1 = box
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle([x0 - i // 5, y0 + i // 2, x1 + i // 5, y1 + i],
                             radius=radius + i // 4,
                             fill=skin['shadow'] + (int(7 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert('RGBA'),
                                 sh.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or skin['card']),
                        outline=hx(edge or skin['card_edge']), width=width)
    return base.convert('RGB')


def pill(img, xy, text, skin, size=17, fg=None, bg=None, kind='cjk_bold'):
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    tw = d.textlength(text, font=f)
    x, y = xy
    h = size + 16
    d.rounded_rectangle([x, y, x + tw + 28, y + h], radius=h // 2,
                        fill=hx(bg or skin['pill']))
    d.text((x + 14, y + 7), text, font=f, fill=hx(fg or skin['accent']))


def wrap(d, text, f, maxw):
    if ' ' in text:
        words, lines, cur = text.split(' '), [], ''
        for wd in words:
            cand = f'{cur} {wd}' if cur else wd
            if d.textlength(cand, font=f) <= maxw or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines
    lines, cur = [], ''
    for ch in text:
        if d.textlength(cur + ch, font=f) <= maxw or not cur:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# hero copy — only prose is localised; every right-hand label is a token
# ---------------------------------------------------------------------------
HERO = {
    'zh': dict(
        kicker='DeepSeek Harness · 插件开发入口',
        title='dsh-plugin-dev',
        value=['六个动作，一条命令', '四条转交，两条真编排'],
        sub=['new / check / tools / upgrade 交给家族工具；',
             'test 在临时 DSH_HOME 里跑三步；',
             'submit 顺着检查器阶梯找 entry-validate。'],
        meta='零配置 · 不挂 profile · 不常驻 · Node ≥24.9.0 · exit 0/1/2/3',
        foot='Apache-2.0 · 社区命令行工具，与 DeepSeek 官方无关',
        table='分发台 · 六个动词',
        table_note='一个可执行文件 · 六条路由',
        exit_label='exit',
    ),
    'en': dict(
        kicker='DeepSeek Harness · plugin dev entry',
        title='dsh-plugin-dev',
        value=['Six actions, one command', 'Four hand-offs, two real runs'],
        sub=['Four verbs hand off to the family tools;',
             'test runs three steps in a temp DSH_HOME;',
             'submit walks the checker ladder to entry-validate.'],
        meta='no config · no profile · Node >=24.9.0 · exit 0/1/2/3',
        foot='Apache-2.0 · community CLI, not affiliated with DeepSeek',
        table='route table · 6 verbs',
        table_note='one binary · six routes',
        exit_label='exit',
    ),
}

# (verb, target it reaches, route class). Straight from src/dev.js.
ROUTES = [
    ('new', 'dsh-plugin-start', 'import'),
    ('check', 'dsh-plugin-ready', 'import'),
    ('tools', 'dsh-plugin-tools', 'import'),
    ('test', 'temp DSH_HOME', 'local'),
    ('submit', 'entry-validate / compat', 'local'),
    ('upgrade', 'where dsh-codemod', 'probe'),
]
CLASS_COLOR = {'import': 'accent2', 'local': 'accent', 'probe': 'faint'}
EXITS = [('0', 'ok'), ('1', 'faint'), ('2', 'fail'), ('3', 'warn')]


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    H_ = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s['bg_from'], s['bg_to'])
    img = glow(img, 1230, 60, 360, hx(s['accent']),
               24 if skin == 'light' else 38)
    img = glow(img, 110, 560, 240, hx(s['accent']),
               8 if skin == 'light' else 14)
    m = 60

    pill(img, (m, 52), H_['kicker'], s, size=17)
    d = ImageDraw.Draw(img)

    # title: mono wordmark, auto-shrunk only if it would cross the panel
    tsize = 80
    while tsize > 62 and d.textlength(H_['title'],
                                      font=font(tsize, 'mono')) > 690:
        tsize -= 2
    d.text((m - 2, 102), H_['title'], font=font(tsize, 'mono'),
           fill=hx(s['text']))

    vkind = 'en_bold' if lang == 'en' else 'cjk_bold'
    vy = 238
    for line in H_['value']:
        d.text((m, vy), line, font=font(38, vkind), fill=hx(s['text']))
        vy += 54

    skind = 'en' if lang == 'en' else 'cjk'
    lines, fsub = [], None
    for size in (25, 23, 21):
        fsub = font(size, skind)
        lines = []
        for para in H_['sub']:
            lines += wrap(d, para, fsub, 700)
        if len(lines) <= 3:
            break
    for i, ln in enumerate(lines):
        d.text((m + 1, 358 + i * 34), ln, font=fsub, fill=hx(s['sub']))

    meta_y = 358 + len(lines) * 34 + 18
    d.text((m + 1, meta_y), H_['meta'],
           font=font(20, 'mono' if lang == 'en' else 'cjk'),
           fill=hx(s['faint']))
    d.line([m + 1, meta_y + 36, m + 566, meta_y + 36],
           fill=hx(s['grid']), width=2)
    d.text((m + 1, meta_y + 52), H_['foot'], font=font(17, skind),
           fill=hx(s['faint']))

    # ---------------- right: prompt bar -> route table -> exit lamps ------
    img = card(img, (772, 84, 1390, 124), s, radius=18)
    d = ImageDraw.Draw(img)
    fm_prompt = font(17, 'mono')
    d.text((792, 93), '$ dsh-dev', font=fm_prompt, fill=hx(s['text']))
    caret_x = 792 + int(d.textlength('$ dsh-dev', font=fm_prompt)) + 5
    d.rounded_rectangle([caret_x, 96, caret_x + 4, 111], radius=2,
                        fill=hx(s['accent']))
    d.text((1364, 93), 'argv.slice(2)', font=font(12, 'mono'),
           anchor='ra', fill=hx(s['faint']))

    # arrow from the prompt into the table
    d.line([1081, 124, 1081, 134], fill=hx(s['accent']), width=2)
    d.polygon([(1081, 138), (1076, 130), (1086, 130)], fill=hx(s['accent']))

    img = card(img, (772, 138, 1390, 470), s, radius=20)
    d = ImageDraw.Draw(img)
    d.text((796, 157), H_['table'], font=font(13, skind), fill=hx(s['accent']))
    d.text((1364, 157), H_['table_note'], font=font(12, skind), anchor='ra',
           fill=hx(s['faint']))
    d.line([796, 178, 1364, 178], fill=hx(s['grid']), width=2)

    fm_token = font(18, 'mono')
    fm_target = font(14, 'mono')
    fm_tag = font(12, 'mono')
    for i, (token, target, cls) in enumerate(ROUTES):
        y = 190 + i * 40
        d.rounded_rectangle([796, y, 1364, y + 34], radius=10,
                            fill=hx(s['zone']))
        # route class is encoded twice: by colour and by the shape of the mark
        if cls == 'local':                    # double bar: orchestrated here
            d.rounded_rectangle([796, y + 8, 798, y + 26], radius=1,
                                fill=hx(s['accent']))
            d.rounded_rectangle([801, y + 8, 803, y + 26], radius=1,
                                fill=hx(s['accent']))
        elif cls == 'probe':                  # three dots: probed on PATH
            for k in range(3):
                d.rounded_rectangle([796, y + 9 + k * 6, 800, y + 12 + k * 6],
                                    radius=1.5, fill=hx(s['faint']))
        else:                                 # solid bar: imported in-process
            d.rounded_rectangle([796, y + 8, 800, y + 26], radius=2,
                                fill=hx(s['accent2']))
        d.text((812, y + 7), token, font=fm_token, fill=hx(s['text']))
        d.text((908, y + 8), '→', font=font(13, 'mono'), fill=hx(s['faint']))
        d.text((944, y + 10), target, font=fm_target, fill=hx(s['sub']))
        d.text((1356, y + 11), cls, font=fm_tag, anchor='ra',
               fill=hx(s[CLASS_COLOR[cls]]))

    # exit lamps: every route returns into the same code
    d.text((796, 450), 'process.exitCode', font=font(12, 'mono'),
           anchor='lm', fill=hx(s['accent']))
    d.text((1108, 450), H_['exit_label'], font=font(12, 'mono'), anchor='rm',
           fill=hx(s['faint']))
    for i, (code, ckey) in enumerate(EXITS):
        x = 1120 + i * 42
        d.rounded_rectangle([x, 438, x + 34, 462], radius=9,
                            fill=hx(s['bg_from']), outline=hx(s[ckey]),
                            width=2)
        d.text((x + 17, 450), code, font=font(13, 'mono'), anchor='mm',
               fill=hx(s[ckey]))

    img.save(os.path.join(OUT, f'dsh-plugin-dev-hero-{lang}-{skin}.webp'),
             'WEBP', quality=92, method=6)
    print(f'dsh-plugin-dev-hero-{lang}-{skin}.webp')


# ---------------------------------------------------------------------------
# flow (hand-written SVG): the unbalanced dispatch tree
# ---------------------------------------------------------------------------
FLOW = {
    'light': dict(bg='#f9f6fd', bg2='#e4eaf8', dots='#ece7f7', card='#ffffff',
                  zone='#f5f1fb', edge='#e4e1ee', grid='#eae6f3',
                  text='#141419', sub='#4d5261', faint='#8f94a4',
                  accent='#4B67B4', accent2='#6d80c4', ok='#16a34a',
                  warn='#bc4c00', fail='#cf222e', solid='0.10'),
    'dark': dict(bg='#131a2a', bg2='#0c1016', dots='#1b2231', card='#161b26',
                 zone='#1c2333', edge='#2a3142', grid='#222a3b',
                 text='#f0f3f9', sub='#a8b1c4', faint='#737b8d',
                 accent='#8496f5', accent2='#a9b7f8', ok='#3fb950',
                 warn='#d29922', fail='#f85149', solid='0.55'),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"

LEAVES = [
    # x, y, verb, target, class tag, exit note
    (44, 222, 'new', 'dsh-plugin-start', 'import', '别名 start'),
    (254, 222, 'check', 'dsh-plugin-ready', 'import', '别名 ready'),
    (44, 300, 'tools', 'dsh-plugin-tools', 'import', 'list · doctor · install'),
    (254, 300, 'upgrade', 'dsh-codemod', 'probe', '缺命令 → exit 3'),
]

CHAIN = [
    ('① 闸门：package.json 可解析', 'edge'),
    ('② 闸门：PATH 上有 dsh 与 pnpm', 'edge'),
    ('③ mkdtemp 建临时 DSH_HOME', 'edge'),
    ('④ add → dump-config → remove', 'accent'),
    ('⑤ --boot 抓一次 127.0.0.1 URL', 'edge'),
    ('⑥ finally 删掉整个临时目录', 'edge'),
]

LADDER = [
    ('① --standards &lt;checkout&gt;', 'grid'),
    ('② $DSH_STANDARDS_DIR', 'grid'),
    ('③ 邻近 standards checkout ×4 深度', 'grid'),
    ('④ 内置 vendor/entry-validate.mjs', 'grid'),
    ('⑤ 兜底 compat C1-C8', 'warn'),
]

LEFT_NOTES = [
    'start / ready / tools 是 package.json 里的普通依赖',
    '调用方式是进程内 import main，不是 spawn',
    'upgrade 例外：where/which 探测 dsh-codemod',
    '没有配置文件、没有 cordis.patch.yml、不挂 profile',
    '不安装插件、不跑 UI、不给结论 → 输出自带 notClaimed',
    '依赖锁定 start 0.2.1 · ready 0.2.2 · tools 0.2.2',
]

TEST_NOTES = [
    'add 失败才停 · remove 非零仅告警',
    '--boot 抓不到 URL → 告警，不算坏',
    'finally 必删 · 证据 dsh-evidence/1',
]

SUBMIT_NOTES = [
    'vendor 缺失才走 compat 子集',
    'C3 无宿主证据 → not-applicable',
    'pass / 告警 / incomplete / fail',
    'args --meta · --host-evidence',
    '不评分 · 不排名 · 不认证',
]


def t(x, y, txt, size, fill, fam=MONO, weight=None, anchor=None,
      spacing=None, opacity=None):
    a = [f'<text x="{x}" y="{y}" fill="{fill}" font-family="{fam}"',
         f'font-size="{size}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    if opacity:
        a.append(f'opacity="{opacity}"')
    if spacing:
        a.append(f'letter-spacing="{spacing}"')
    a.append(f'>{txt}</text>')
    return ' '.join(a)


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    W, H = 1100, 660
    p = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="dsh-plugin-dev dispatch tree: one argv root, a shallow hand-off subtree of four verbs that leave this repository, and a deep orchestration subtree for test (six steps in a temp DSH_HOME) and submit (a five-rung checker ladder); every branch returns one process.exitCode among 0, 1, 2, 3">
<title>dsh-plugin-dev — unbalanced dispatch tree</title>
<defs>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="200%">
    <feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#241d4a" flood-opacity="{s['solid']}"/>
  </filter>
  <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
    <circle cx="1.3" cy="1.3" r="1.3" fill="{s['dots']}"/>
  </pattern>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 z" fill="{s['accent']}"/>
  </marker>
  <marker id="arrFaint" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 z" fill="{s['faint']}"/>
  </marker>
  <linearGradient id="page" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{s['bg']}"/>
    <stop offset="1" stop-color="{s['bg2']}"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#page)"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".6"/>
''']

    # ---- header ----------------------------------------------------------
    p.append(t(44, 50, 'dsh-plugin-dev', 30, s['text'], weight='700'))
    p.append(t(44, 79, 'argv → 动词 → 两类落点：转交 4 条 / 本仓编排 2 条 · '
                       '每个分支只返回一个 process.exitCode', 15, s['sub'],
               fam=SANS))

    # ---- root: argv ------------------------------------------------------
    p.append(f'<rect x="330" y="96" width="440" height="68" rx="16" '
             f'fill="{s["card"]}" stroke="{s["accent"]}" stroke-width="1.6" '
             f'filter="url(#soft)"/>')
    p.append(t(348, 117, 'S0 · argv', 11, s['accent'], weight='700',
               spacing='0.6'))
    p.append(t(348, 142, 'dsh-dev &lt;verb&gt; [flags]', 17, s['text'],
               weight='700'))
    p.append(t(348, 158, '--help / -h 短路 → exit 0 · 未知命令 → exit 1', 11,
               s['faint'], fam=SANS))

    # ---- stem + bus + two drops -----------------------------------------
    p.append(f'<path d="M550 164V178" stroke="{s["accent"]}" stroke-width="2"/>')
    p.append(f'<path d="M248 178H763" stroke="{s["accent"]}" stroke-width="2" '
             f'fill="none"/>')
    p.append(f'<path d="M248 178V195" stroke="{s["accent"]}" stroke-width="2" '
             f'marker-end="url(#arr)"/>')
    p.append(f'<path d="M763 178V195" stroke="{s["accent"]}" stroke-width="2" '
             f'marker-end="url(#arr)"/>')

    # ---- branch labels ---------------------------------------------------
    p.append(t(248, 211, '转交 · 4 条（不在本仓实现）', 12.5, s['accent'],
               fam=SANS, weight='700', anchor='middle'))
    p.append(t(763, 211, '本仓编排 · 2 条（src/host-test.js · src/submit.js）',
               12.5, s['accent'], fam=SANS, weight='700', anchor='middle'))

    # ---- shallow subtree: four leaves that leave the repo ---------------
    for x, y, verb, target, tag, note in LEAVES:
        p.append(f'<rect x="{x}" y="{y}" width="194" height="70" rx="14" '
                 f'fill="{s["card"]}" stroke="{s["edge"]}" '
                 f'filter="url(#soft)"/>')
        p.append(t(x + 16, y + 26, verb, 16, s['text'], weight='700'))
        p.append(t(x + 16, y + 47, target, 11, s['sub']))
        p.append(t(x + 178, y + 22, tag, 11, s['accent2'], anchor='end',
                   spacing='0.4'))
        p.append(t(x + 16, y + 63, note, 11, s['faint'], fam=SANS))

    # ---- left annotation: what this repository does NOT implement -------
    p.append(f'<rect x="44" y="382" width="404" height="170" rx="16" '
             f'fill="{s["zone"]}" stroke="{s["edge"]}" stroke-width="1.4" '
             f'stroke-dasharray="7 5"/>')
    p.append(t(62, 406, '转交侧 · 这个仓库不实现这些', 12, s['accent'],
               fam=SANS, weight='700'))
    for i, note in enumerate(LEFT_NOTES):
        p.append(t(62, 431 + i * 21, note, 11, s['sub'], fam=SANS))

    # ---- deep subtree A: test's temp-DSH_HOME chain ---------------------
    p.append(f'<rect x="470" y="222" width="294" height="330" rx="16" '
             f'fill="{s["card"]}" stroke="{s["edge"]}" filter="url(#soft)"/>')
    p.append(t(488, 247, 'test', 16, s['text'], weight='700'))
    p.append(t(746, 246, 'src/host-test.js', 11, s['faint'], anchor='end'))
    p.append(t(488, 266, 'temp DSH_HOME · 不过闸门 → blocked', 11, s['sub'],
               fam=SANS))
    p.append(f'<line x1="500" y1="294" x2="500" y2="454" '
             f'stroke="{s["edge"]}" stroke-width="2"/>')
    for i, (label, ckey) in enumerate(CHAIN):
        y = 280 + i * 32
        p.append(f'<circle cx="500" cy="{y + 14}" r="3.4" fill="{s[ckey]}"/>')
        p.append(f'<rect x="512" y="{y}" width="234" height="28" rx="9" '
                 f'fill="{s["zone"]}" stroke="{s["grid"]}"/>')
        p.append(t(524, y + 19, label, 11, s['text'], fam=SANS))
    for i, note in enumerate(TEST_NOTES):
        p.append(t(488, 494 + i * 21, note, 11, s['faint'], fam=SANS))

    # ---- deep subtree B: submit's checker ladder ------------------------
    p.append(f'<rect x="780" y="222" width="276" height="330" rx="16" '
             f'fill="{s["card"]}" stroke="{s["edge"]}" filter="url(#soft)"/>')
    p.append(t(798, 247, 'submit', 16, s['text'], weight='700'))
    p.append(t(1038, 246, 'src/submit.js', 11, s['faint'], anchor='end'))
    p.append(t(798, 266, '找 checker：5 级阶梯，找到即停', 11, s['sub'],
               fam=SANS))
    p.append(f'<line x1="812" y1="294" x2="812" y2="422" '
             f'stroke="{s["accent"]}" stroke-width="1.6"/>')
    for i, (label, ckey) in enumerate(LADDER):
        y = 280 + i * 32
        p.append(f'<path d="M812 {y + 14}H818" stroke="{s["accent"]}" '
                 f'stroke-width="1.6"/>')
        p.append(f'<rect x="818" y="{y}" width="220" height="28" rx="9" '
                 f'fill="{s["zone"]}" stroke="{s[ckey]}"/>')
        p.append(t(830, y + 19, label, 11, s['text'], fam=SANS))
    for i, note in enumerate(SUBMIT_NOTES):
        p.append(t(798, 458 + i * 20, note, 11, s['faint'], fam=SANS))

    # ---- exit-code rail: both halves return one number ------------------
    p.append(f'<path d="M617 552V566" stroke="{s["faint"]}" stroke-width="1.6" '
             f'stroke-dasharray="4 4" marker-end="url(#arrFaint)"/>')
    p.append(f'<path d="M918 552V566" stroke="{s["faint"]}" stroke-width="1.6" '
             f'stroke-dasharray="4 4" marker-end="url(#arrFaint)"/>')
    p.append(f'<rect x="44" y="566" width="1012" height="64" rx="14" '
             f'fill="{s["zone"]}" stroke="{s["edge"]}" stroke-width="1.4"/>')
    p.append(t(64, 589, 'process.exitCode', 12, s['accent'], weight='700'))
    p.append(t(64, 607, 'bin/dsh-dev.js 统一设置 · 六个分支共用', 11,
               s['faint'], fam=SANS))
    codes = [('0', '通过 / 正常结束', 'ok'),
             ('1', '未知命令 / 参数错', 'faint'),
             ('2', '检查失败', 'fail'),
             ('3', 'blocked / 未完成', 'warn')]
    for i, (code, caption, ckey) in enumerate(codes):
        x = 352 + i * 172
        p.append(f'<rect x="{x}" y="576" width="160" height="42" rx="10" '
                 f'fill="{s["card"]}" stroke="{s[ckey]}"/>')
        p.append(t(x + 16, 601, code, 15, s[ckey], weight='700'))
        p.append(t(x + 40, 599, caption, 11, s['sub'], fam=SANS))

    # ---- footer ----------------------------------------------------------
    p.append(t(44, 648, '只返回数字 · 不安装插件、不跑 UI、不认证', 11,
               s['faint'], fam=SANS))
    p.append(t(1056, 648, 'schema dsh-dev-test/1 · dsh-dev-submit/1', 11,
               s['faint'], anchor='end'))
    p.append('</svg>')

    path = os.path.join(OUT, f'dsh-plugin-dev-flow-v5-{skin}.svg')
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(p) + '\n')
    print(f'dsh-plugin-dev-flow-v5-{skin}.svg')


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ('light', 'dark'):
        for lang in ('zh', 'en'):
            hero(lang, skin)
    for skin in ('light', 'dark'):
        flow_svg(skin)


if __name__ == '__main__':
    main()
