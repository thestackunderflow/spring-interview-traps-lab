"""Frame-0 cards (light look) for episode 2, built from the lab's own files, never retyped:
- frames/hook-landscape.png (1600x1000): the intro slide's right half and the long video's hook overlay
- frames/short-frame0.png (1080x1440): the Short's frame-0 overlay (above the caption band)
- frames/thumb-base.png (1280x720): the thumbnail's evidence crop
Sources: src/main/java/lab/Ticket.java L10-11, lab/trap/TicketCounter.java L13, evidence/replays/ep2-trap/run.jsonl.
Run (no host installs): docker run --rm -v "<lab>:/lab" tsu-thumbs:0.1 python3 /lab/ep2-prototype/video/make_frames.py
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

EP = '/lab/ep2-prototype'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
INK, RED, MUTED, BLUE, VIOLET = '#1a2230', '#c62828', '#5b6678', '#1d4ed8', '#6d28d9'

ticket = open(os.path.join(EP, 'src/main/java/lab/Ticket.java'), encoding='utf-8').read().splitlines()
counter = open(os.path.join(EP, 'src/main/java/lab/trap/TicketCounter.java'), encoding='utf-8').read().splitlines()
SCOPE, TCLASS, FIELD = ticket[9], ticket[10], counter[12].strip()
assert SCOPE.startswith('@Scope(') and 'PROTOTYPE' in SCOPE and FIELD == 'private final Ticket ticket;', (SCOPE, FIELD)
run = [json.loads(l)['text'] for l in open(os.path.join(EP, 'evidence/replays/ep2-trap/run.jsonl'), encoding='utf-8')]
CALLS = [t for t in run if t.startswith('LAB: call ')]
assert len(CALLS) == 3 and all('Ticket #1,' in c for c in CALLS), CALLS
SHORT = [c[:c.index(',')] + ' …' for c in CALLS]


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
card(os.path.join(out, 'hook-landscape.png'), 1600, 1000, 36, 'Ticket.java + TicketCounter.java · Spring Boot 4.1.2',
     'Real lab run, 22 Oct 2026 · code from the lab files · LAB lines as captured',
     [(SCOPE, VIOLET, False), (TCLASS, INK, False), ('', INK, False), ('// in TicketCounter, a singleton:', MUTED, False),
      (FIELD, RED, True), ('', INK, False)] + [(c, RED if i == 2 else INK, i == 2) for i, c in enumerate(CALLS)])
card(os.path.join(out, 'short-frame0.png'), 1080, 1440, 36, 'Spring Boot 4.1.2 · real run',
     'Real lab run, 22 Oct 2026, as captured',
     [(SCOPE[:SCOPE.index('(')] + '(...PROTOTYPE)', VIOLET, False), ('', INK, False)] + [(c, INK, False) for c in SHORT[:2]]
     + [(SHORT[2], RED, True), ('', INK, False), ('Prototype. Same object', INK, False), ('every call. Why?', INK, False)])
print('frames written')
