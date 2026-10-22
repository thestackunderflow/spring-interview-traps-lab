"""Frame-0 cards (light look) for episode 1, built from the lab's own files, never retyped:
- frames/hook-landscape.png (1600x1000): the intro slide's right half and the long video's hook overlay
- frames/short-frame0.png (1080x1440): the Short's frame-0 overlay (above the caption band)
- frames/thumb-base.png (1280x720): the thumbnail's evidence crop
Sources: src/main/java/lab/trap/Checkout.java L21-26, evidence/replays/ep1-trap/run.jsonl (LAB: lines).
Run (no host installs): docker run --rm -v "<lab>:/lab" tsu-thumbs:0.1 python3 /lab/ep1-transactional/video/make_frames.py
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

EP = '/lab/ep1-transactional'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK, RED, MUTED, BLUE, VIOLET = '#1a2230', '#c62828', '#5b6678', '#1d4ed8', '#6d28d9'

src = open(os.path.join(EP, 'src/main/java/lab/trap/Checkout.java'), encoding='utf-8').read().splitlines()
CODE = [src[i - 1][4:] for i in range(21, 27)]   # placeOrder + the annotated method's first lines, one indent level off
assert CODE[1].strip() == 'this.saveAndCharge(item);' and CODE[4].strip() == '@Transactional', CODE
run = [json.loads(l)['text'] for l in open(os.path.join(EP, 'evidence/replays/ep1-trap/run.jsonl'), encoding='utf-8')]
THREW = next(t for t in run if t.startswith('LAB: placeOrder threw '))
COUNT = next(t for t in run if t.startswith('LAB: orders after failure = '))
assert COUNT == 'LAB: orders after failure = 1', COUNT


def card(path, W, H, size, title, note, rows):
    im = Image.new('RGB', (W, H), '#f6f7f9')
    d = ImageDraw.Draw(im)
    m = int(W * 0.04)
    top = int(H * 0.06) if W > H else int(H * 0.08)
    d.rounded_rectangle((m, top, W - m, H - top - 60), 24, fill='#ffffff', outline='#d8dde5', width=4)
    d.rectangle((m + 2, top + 2, W - m - 2, top + 70), fill='#e3e7ee')
    for i, c in enumerate(('#e5534b', '#d9a400', '#2da44e')):
        d.ellipse((m + 30 + i * 42, top + 22, m + 56 + i * 42, top + 48), fill=c)
    d.text((m + 180, top + 18), title, font=ImageFont.truetype(BOLD, int(size * 0.75)), fill=INK)
    f, fb = ImageFont.truetype(MONO, size), ImageFont.truetype(BOLD, size)
    y = top + 110
    for text, col, box in rows:
        font = fb if col in (RED, BLUE, VIOLET) else f
        w = d.textlength(text, font=font)
        assert w <= W - 2 * m - 80, (path, text)
        if box:
            d.rounded_rectangle((m + 28, y - 8, m + 52 + w, y + size + 12), 10, fill='#fdecec' if col == RED else '#e8efff',
                                outline=col, width=3)
        d.text((m + 40, y), text, font=font, fill=col)
        y += int(size * 1.5)
    assert y < H - top - 60, (path, 'rows overflow the card')
    fn = ImageFont.truetype(MONO, int(size * 0.6))
    assert d.textlength(note, font=fn) <= W - 2 * m, (path, 'footer too wide')
    d.text((m + 6, H - top - 40), note, font=fn, fill=MUTED)
    im.save(path)


out = os.path.join(EP, 'video', 'frames')
os.makedirs(out, exist_ok=True)
code_rows = [(CODE[0], INK, False), (CODE[1], RED, True), (CODE[2], INK, False), ('', INK, False),
             (CODE[4], VIOLET, False), (CODE[5], INK, False)]
card(os.path.join(out, 'hook-landscape.png'), 1600, 1000, 40, 'Checkout.java · Spring Boot 4.1.2',
     'Real lab run, 22 Oct 2026 · lines as captured',
     code_rows + [('  ...throws PaymentDeclinedException', MUTED, False), ('', INK, False), (COUNT, RED, True)])
card(os.path.join(out, 'short-frame0.png'), 1080, 1440, 36, 'Spring Boot 4.1.2 · real run',
     'Real lab run, 22 Oct 2026, as captured',
     code_rows + [('', INK, False), ('...it threw. Then:', MUTED, False), (COUNT, RED, True), ('', INK, False),
                  ('The row stayed. Why?', INK, False)])
# thumbnail base: the outcome line only, big
im = Image.new('RGB', (1280, 720), '#ffffff')
d = ImageDraw.Draw(im)
d.text((70, 430), COUNT, font=ImageFont.truetype(BOLD, 46), fill=RED)
d.text((70, 510), '@Transactional · this.saveAndCharge(item)', font=ImageFont.truetype(MONO, 34), fill=MUTED)
im.save(os.path.join(out, 'thumb-base.png'))
print('frames written', THREW)
