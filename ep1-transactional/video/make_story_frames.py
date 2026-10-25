"""Beginner opening pictures for episode 1 (v2 re-cut, 24 Oct 2026): the everyday stakes before any Spring word.
- frames/story-1-both.png        what must happen: save the order AND charge the card, both or neither
- frames/story-2-wrong.png       what the real trap run did: card declined, the order stayed (count read from the log)
- frames/story-3-transaction.png the name for "both, or neither": a transaction
All 1600x1000 (the intro slide's right half, split layout). Only the count line is evidence; it is read from
evidence/replays/ep1-trap/run.jsonl, never typed.
Run (no host installs): docker run --rm -v "<lab>:/lab" tsu-thumbs:0.1 python3 /lab/ep1-transactional/video/make_story_frames.py
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

EP = '/lab/ep1-transactional'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
INK, MUTED, RED, GREEN, BLUE, LINE = '#1a2230', '#5b6678', '#c62828', '#1b7f3b', '#1d4ed8', '#d8dde5'
W, H = 1600, 1000

run = [json.loads(l)['text'] for l in open(os.path.join(EP, 'evidence/replays/ep1-trap/run.jsonl'), encoding='utf-8')]
COUNT = next(t for t in run if t.startswith('LAB: orders after failure = '))
assert COUNT == 'LAB: orders after failure = 1', COUNT
assert any(t.startswith('LAB: placeOrder threw PaymentDeclinedException') for t in run)


def font(path, size):
    return ImageFont.truetype(path, size)


def base(title):
    im = Image.new('RGB', (W, H), '#f6f7f9')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, W - 40, H - 40), 28, fill='#ffffff', outline=LINE, width=4)
    f = font(SANS_B, 60)
    d.text(((W - d.textlength(title, font=f)) / 2, 80), title, font=f, fill=INK)
    return im, d


def receipt(d, x, y, col):
    d.rounded_rectangle((x, y, x + 120, y + 150), 10, fill='#ffffff', outline=col, width=6)
    for k in range(4):
        d.line((x + 22, y + 32 + k * 28, x + 98 - (30 if k == 3 else 0), y + 32 + k * 28), fill=col, width=6)


def card_icon(d, x, y, col):
    d.rounded_rectangle((x, y + 15, x + 170, y + 125), 14, fill='#ffffff', outline=col, width=6)
    d.rectangle((x + 3, y + 40, x + 167, y + 62), fill=col)
    d.rounded_rectangle((x + 20, y + 85, x + 70, y + 105), 4, fill=col)


def check(d, x, y, col=GREEN):
    d.line((x, y + 30, x + 25, y + 58, x + 70, y), fill=col, width=14, joint='curve')


def cross(d, x, y, col=RED):
    d.line((x, y, x + 60, y + 60), fill=col, width=14)
    d.line((x + 60, y, x, y + 60), fill=col, width=14)


def step(d, x, y, w, num, text, icon, col, outline=LINE, width=4, mark=None, note=None, note_col=MUTED):
    d.rounded_rectangle((x, y, x + w, y + 400), 24, fill='#fbfcfe', outline=outline, width=width)
    icon(d, x + (w - (170 if icon is card_icon else 120)) / 2, y + 40, col)
    f = font(SANS_B, 54)
    for k, line in enumerate(text):
        d.text((x + (w - d.textlength(line, font=f)) / 2, y + 220 + k * 66), line, font=f, fill=INK)
    fn = font(SANS_B, 30)
    d.ellipse((x + 22, y + 22, x + 82, y + 82), fill=col)
    d.text((x + 52 - d.textlength(num, font=fn) / 2, y + 34), num, font=fn, fill='#ffffff')
    if mark == 'check':
        check(d, x + w - 110, y + 40)
    elif mark == 'cross':
        cross(d, x + w - 100, y + 40)
    if note:
        fb = font(SANS_B, 46)
        d.text((x + (w - d.textlength(note, font=fb)) / 2, y + 420), note, font=fb, fill=note_col)


def centered(d, y, text, f, col):
    assert d.textlength(text, font=f) <= W - 140, text
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=col)


out = os.path.join(EP, 'video', 'frames')
os.makedirs(out, exist_ok=True)
X1, X2, SW = 120, 860, 620

# 1. the stakes
im, d = base('You pay for an order online')
step(d, X1, 190, SW, '1', ['Save', 'your order'], receipt, BLUE)
step(d, X2, 190, SW, '2', ['Charge', 'your card'], card_icon, BLUE)
centered(d, 360, '+', font(SANS_B, 90), MUTED)
centered(d, 680, 'Both, or neither.', font(SANS_B, 84), INK)
im.save(os.path.join(out, 'story-1-both.png'))

# 2. what the real trap run did (the decline is the lab's stand-in: saveAndCharge always throws PaymentDeclinedException)
im, d = base('Our test shop app, a real run')
step(d, X1, 160, SW, '1', ['Save', 'your order'], receipt, GREEN, outline=GREEN, width=6, mark='check', note='saved', note_col=GREEN)
step(d, X2, 160, SW, '2', ['Charge', 'your card'], card_icon, RED, outline=RED, width=6, mark='cross', note='declined (test)', note_col=RED)
centered(d, 655, 'The order stayed saved:', font(SANS_B, 60), INK)
centered(d, 728, 'an order nobody paid for', font(SANS_B, 60), RED)
centered(d, 818, 'Our test app printed its own check:', font(SANS_B, 40), INK)
centered(d, 870, COUNT, font(MONO, 44), INK)
im.save(os.path.join(out, 'story-2-wrong.png'))

# 3. the name. Accuracy (24 Oct): a database transaction covers the database changes only (the saved order), never the
# card charge; the declined charge is what should trigger undoing the save.
im, d = base('The tool for this: a transaction')
d.rounded_rectangle((90, 185, 760, 620), 30, outline=BLUE, width=8)
fl = font(SANS_B, 40)
lab = 'a transaction'
lw = d.textlength(lab, font=fl)
d.rectangle((425 - lw / 2 - 20, 162, 425 + lw / 2 + 20, 210), fill='#ffffff')
d.text((425 - lw / 2, 163), lab, font=fl, fill=BLUE)
d.rounded_rectangle((130, 235, 720, 590), 24, fill='#fbfcfe', outline=LINE, width=4)
receipt(d, 365, 255, BLUE)
f = font(SANS_B, 52)
for k, line in enumerate(['Save', 'your order']):
    d.text((425 - d.textlength(line, font=f) / 2, 430 + k * 62), line, font=f, fill=INK)
step(d, 860, 200, 620, '2', ['Charge', 'your card'], card_icon, RED, outline=RED, width=6, mark='cross')
d.line((860, 470, 790, 470), fill=RED, width=10)
d.polygon(((768, 470), (800, 450), (800, 490)), fill=RED)
fb = font(SANS_B, 44)
centered(d, 650, 'Declined? Then undo the save.', font(SANS_B, 60), RED)
centered(d, 750, 'Database changes: kept together,', font(SANS_B, 56), INK)
centered(d, 822, 'or undone together', font(SANS_B, 56), INK)
im.save(os.path.join(out, 'story-3-transaction.png'))
print('story frames written:', COUNT)
