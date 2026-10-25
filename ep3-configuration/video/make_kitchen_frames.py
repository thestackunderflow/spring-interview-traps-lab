"""Pictures for episode 3 (v2 re-cut, 25 Oct 2026): a real-life opening, then ONE analogy, Spring's kitchen, reused as
a memory peg through the trap and the fix. Same style as ep1's make_story_frames.py / make_desk_frames.py.
- frames/story-1-one-log.png      the stakes: a shop keeps ONE audit log; the order part writes, the checker reads
- frames/story-2-two-logs.png     our real run: two AuditLogs; the order part holds #2 (lines as the lab printed them)
- frames/kitchen-1-shelf.png      the recipe book (AppBeans), two recipes with their @Bean labels, Spring follows each
                                  recipe once and keeps the result on the shelf (the container): one of each = singleton
- frames/kitchen-2-as-written.png the trap: cover label @Component, the book is used as written: the orderService
                                  recipe runs the auditLog recipe again, AuditLog #2 is made and never goes on the shelf
- frames/kitchen-3-edited.png     the fix: cover label @Configuration, Spring's edited book (the subclass): every recipe
                                  checks the shelf first, AuditLog #1 is handed back
Mapping (1:1, the only one used in the video): recipe = @Bean method, label above a recipe = @Bean, recipe book =
the class AppBeans, shelf = Spring's container, one of each = singleton, label on the cover = @Component /
@Configuration, the book as written = lite mode, Spring's edited book = the CGLIB subclass.
All 1600x1000 (the slide's right half, split layout). Lines quoted from the lab are copied from
evidence/replays/ep3-trap/raw/stdout.txt; nothing else here is evidence.
Run (no host installs): docker run --rm -v "<lab>:/lab" tsu-thumbs:0.1 python3 /lab/ep3-configuration/video/make_kitchen_frames.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

EP = '/lab/ep3-configuration'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
MONO_B = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
INK, MUTED, RED, GREEN, BLUE, ORANGE, LINE = '#1a2230', '#5b6678', '#c62828', '#1b7f3b', '#1d4ed8', '#b45309', '#d8dde5'
W, H = 1600, 1000


def font(path, size):
    return ImageFont.truetype(path, size)


def base(title):
    im = Image.new('RGB', (W, H), '#f6f7f9')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, W - 40, H - 40), 28, fill='#ffffff', outline=LINE, width=4)
    f = font(SANS_B, 58)
    assert d.textlength(title, font=f) <= W - 140, title
    d.text(((W - d.textlength(title, font=f)) / 2, 72), title, font=f, fill=INK)
    return im, d


def ctext(d, cx, y, text, f, col):
    assert d.textlength(text, font=f) <= W - 120, text
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=col)


def arrow(d, pts, col, width=10, dashed=False):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if not dashed:
            d.line((xa, ya, xb, yb), fill=col, width=width)
            continue
        n = max(1, int((abs(xb - xa) + abs(yb - ya)) / 26))
        for k in range(0, n, 2):
            t0, t1 = k / n, min(1, (k + 1) / n)
            d.line((xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1), fill=col, width=width)
    (xa, ya), (xb, yb) = pts[-2], pts[-1]
    a = math.atan2(yb - ya, xb - xa)
    s = 30
    d.polygon(((xb, yb), (xb - s * math.cos(a - 0.45), yb - s * math.sin(a - 0.45)),
               (xb - s * math.cos(a + 0.45), yb - s * math.sin(a + 0.45))), fill=col)


def tag(d, cx, y, text, col, size=32, fill='#ffffff', mono=False):
    f = font(MONO_B if mono else SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((cx - tw / 2 - 14, y - 6, cx + tw / 2 + 14, y + size + 12), 10, fill=fill, outline=col, width=4)
    d.text((cx - tw / 2, y), text, font=f, fill=col)


def notebook(d, x, y, w, h, title, rows, col):
    """An audit log drawn as a notebook: rings on the left, one row per order."""
    d.rounded_rectangle((x, y, x + w, y + h), 16, fill='#ffffff', outline=col, width=6)
    for k in range(4):
        cy = y + 40 + k * (h - 80) / 3
        d.ellipse((x - 14, cy - 10, x + 14, cy + 10), outline=col, width=5)
    ctext(d, x + w / 2, y + 18, title, font(SANS_B, 38), col)
    f = font(SANS_B, 32)
    for k, r in enumerate(rows):
        d.line((x + 40, y + 120 + k * 56, x + w - 30, y + 120 + k * 56), fill=LINE, width=3)
        d.text((x + 44, y + 78 + k * 56), r, font=f, fill=INK)


def box(d, b, text, col, size=38, fill='#ffffff', width=6):
    d.rounded_rectangle(b, 18, fill=fill, outline=col, width=width)
    f = font(SANS_B, size)
    lines = text.split('\n')
    y0 = (b[1] + b[3]) / 2 - len(lines) * (size + 8) / 2
    for k, ln in enumerate(lines):
        d.text(((b[0] + b[2]) / 2 - d.textlength(ln, font=f) / 2, y0 + k * (size + 8)), ln, font=f, fill=col)


def recipe(d, x, y, name, step, col=INK, first=None):
    """A recipe card = a @Bean method: the @Bean label on top, its name, what it says."""
    w, h = 470, 230 if first is None else 214
    d.rounded_rectangle((x, y, x + w, y + h), 16, fill='#fffdf7', outline=col, width=5)
    tag(d, x + 90, y + 16, '@Bean', ORANGE, size=32, fill='#fff4e5', mono=True)
    d.text((x + 170, y + 18), name, font=font(SANS_B, 36), fill=INK)
    yy = y + 84
    if first:
        d.text((x + 24, yy), first, font=font(SANS_B, 32), fill=GREEN)
        yy += 52
    for ln in step.split('\n'):
        d.text((x + 24, yy), ln, font=font(SANS_B, 32), fill=INK)
        yy += 46
    return (x, y, x + w, y + h)


def book(d, x, y, w, h, cover, cover_col, title='AppBeans = the recipe book', back=False):
    if back:
        d.rounded_rectangle((x + 22, y + 22, x + w + 22, y + h + 22), 22, fill='#eef1f6', outline=LINE, width=4)
    d.rounded_rectangle((x, y, x + w, y + h), 22, fill='#f3f6fd', outline=BLUE, width=8)
    f = font(SANS_B, 34)
    tw = d.textlength(title, font=f)
    d.rounded_rectangle((x + 24, y - 26, x + 24 + tw + 36, y + 26), 14, fill=BLUE)
    d.text((x + 42, y - 21), title, font=f, fill='#ffffff')
    if cover:
        tag(d, x + w / 2, y + h - 26, 'cover label: ' + cover, cover_col, size=32, fill='#fff4e5', mono=True)   # on the book's bottom edge


def shelf(d, x, y, w, items, caption='Shelf = Spring\'s container'):
    """The shelf = the container: a plank with the beans standing on it."""
    for k, (label, col) in enumerate(items):
        bx = x + 20 + k * 250
        box(d, (bx, y - 150, bx + 230, y - 10), label, col, size=34)
    d.rounded_rectangle((x, y, x + w, y + 26), 8, fill='#8a5a2b')
    d.line((x + 30, y + 26, x + 30, y + 90), fill='#8a5a2b', width=12)
    d.line((x + w - 30, y + 26, x + w - 30, y + 90), fill='#8a5a2b', width=12)
    ctext(d, x + w / 2, y + 100, caption, font(SANS_B, 36), INK)


out = os.path.join(EP, 'video', 'frames')
os.makedirs(out, exist_ok=True)

# 1. the stakes: one audit log, everyone writes to it, the checker reads it
im, d = base('A shop keeps one audit log')
box(d, (110, 330, 430, 470), 'Takes\norders', INK)
notebook(d, 600, 210, 420, 400, 'Audit log', ['Order 1: book', 'Order 2: pen', 'Order 3: lamp', '...'], BLUE)
box(d, (1190, 330, 1490, 470), 'The\nchecker', INK)
arrow(d, [(436, 400), (582, 400)], GREEN)
ctext(d, 509, 340, 'writes', font(SANS_B, 32), GREEN)
arrow(d, [(1040, 400), (1184, 400)], GREEN)
ctext(d, 1112, 340, 'reads', font(SANS_B, 32), GREEN)
ctext(d, W / 2, 680, 'Every order, in one place.', font(SANS_B, 56), INK)
ctext(d, W / 2, 760, 'Exactly one audit log.', font(SANS_B, 56), BLUE)
im.save(os.path.join(out, 'story-1-one-log.png'))

# 2. the real run: two AuditLogs; the order part holds #2 (LAB lines copied from the trap run)
im, d = base('Our test shop app, a real run')
notebook(d, 170, 190, 440, 330, 'Audit log #1', ['handed out', 'by Spring'], BLUE)
notebook(d, 990, 190, 440, 330, 'Audit log #2', ['held by the', 'order part'], RED)
ctext(d, 800, 300, 'two?', font(SANS_B, 64), RED)
ctext(d, W / 2, 575, 'In a real app, orders kept in #2 would never', font(SANS_B, 44), INK)
ctext(d, W / 2, 635, 'whoever checks #1.', font(SANS_B, 46), RED)
ctext(d, W / 2, 735, 'Our test app printed its own check:', font(SANS_B, 40), INK)
ctext(d, W / 2, 795, 'LAB: AuditLog constructor ran, #2', font(MONO, 42), INK)
ctext(d, W / 2, 855, 'LAB: same object? false', font(MONO, 42), INK)
im.save(os.path.join(out, 'story-2-two-logs.png'))

# 3. the kitchen: recipe book, two recipes, Spring follows each once, the shelf
im, d = base("Spring's kitchen")
book(d, 90, 200, 560, 620, None, None)
recipe(d, 135, 250, 'auditLog', 'make a new\nAuditLog')
recipe(d, 135, 520, 'orderService', 'needs an AuditLog:\nrun the auditLog recipe')
arrow(d, [(670, 490), (880, 490)], GREEN)
ctext(d, 775, 390, 'Spring follows', font(SANS_B, 30), GREEN)
ctext(d, 775, 426, 'each recipe once', font(SANS_B, 30), GREEN)
shelf(d, 905, 560, 560, [('AuditLog', INK), ('Order\nService', INK)])
ctext(d, W / 2, 860, 'One of each on the shelf: a singleton.', font(SANS_B, 46), BLUE)
im.save(os.path.join(out, 'kitchen-1-shelf.png'))

# 4. the trap: @Component, the book as written
im, d = base('The trap: the book as written')
book(d, 90, 200, 560, 620, '@Component', ORANGE)
recipe(d, 135, 250, 'auditLog', 'make a new\nAuditLog')
recipe(d, 135, 520, 'orderService', 'needs an AuditLog:\nrun the auditLog recipe')
shelf(d, 905, 420, 560, [('AuditLog\n#1', INK)])
box(d, (960, 650, 1360, 790), 'AuditLog #2\nnot on the shelf', RED, size=34)
arrow(d, [(610, 640), (950, 720)], RED, width=9, dashed=True)
ctext(d, 790, 760, 'a new one', font(SANS_B, 32), RED)
ctext(d, W / 2, 870, 'Nobody checks the shelf: a second AuditLog.', font(SANS_B, 44), RED)
im.save(os.path.join(out, 'kitchen-2-as-written.png'))

# 5. the fix: @Configuration, Spring's edited book: check the shelf first
im, d = base("The fix: Spring's edited book")
book(d, 90, 200, 560, 620, '@Configuration', ORANGE, title="Spring's edited book", back=True)
recipe(d, 135, 245, 'auditLog', '2. If empty: make one', first='1. Check the shelf first')
recipe(d, 135, 490, 'orderService', '2. Run auditLog recipe', first='1. Check the shelf first')
shelf(d, 905, 560, 560, [('AuditLog\n#1', GREEN), ('Order\nService', INK)])
arrow(d, [(612, 600), (760, 600), (760, 470), (920, 470)], GREEN)
ctext(d, 1185, 300, 'found: AuditLog #1', font(SANS_B, 34), GREEN)
ctext(d, 1185, 345, 'handed back', font(SANS_B, 34), GREEN)
ctext(d, W / 2, 870, 'Every recipe checks the shelf first: one AuditLog.', font(SANS_B, 42), GREEN)
im.save(os.path.join(out, 'kitchen-3-edited.png'))
print('kitchen frames written')
