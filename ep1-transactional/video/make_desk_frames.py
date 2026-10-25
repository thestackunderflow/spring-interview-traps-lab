"""Front-desk analogy pictures for episode 1 (v3 re-cut, 25 Oct 2026: owner asked for one analogy for the proxy,
reused as a memory peg through the trap and the fix). One picture, the same words, three moments:
- frames/desk-1-office.png  the office (the Checkout bean), its rooms (methods), the front desk (the proxy);
                            a call from outside comes in through the desk; saveAndCharge's door has the label
- frames/desk-2-hall.png    the trap: the Buy call passes the desk into placeOrder's room, then placeOrder walks
                            down the hall (this.saveAndCharge) to the next room: the desk never sees it
- frames/desk-3-fix.png     the fix: saveAndCharge in its own office (OrderWriter) with its own front desk;
                            placeOrder's call (writer.saveAndCharge) goes out and in through that desk
Mapping (1:1, the only one used in the video): office = bean, room = method, label on a door = @Transactional,
front desk = proxy (Spring puts it in front of the bean; the rest of the app is handed the desk), a call from
outside = through the desk, a call with this = a walk down the hall (this is the office itself, never the desk).
All 1600x1000 (the slide's right half, split layout). No evidence is drawn here (no counts, no log lines).
Run (no host installs): docker run --rm -v "<lab>:/lab" tsu-thumbs:0.1 python3 /lab/ep1-transactional/video/make_desk_frames.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

EP = '/lab/ep1-transactional'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
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
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=col)


def office(d, box, name):
    """An office = a bean: a building outline with its name on a tab at the top."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 26, fill='#f3f6fd', outline=BLUE, width=8)
    f = font(SANS_B, 38)
    tw = d.textlength(name, font=f)
    d.rounded_rectangle((x0 + 24, y0 - 26, x0 + 24 + tw + 36, y0 + 26), 14, fill=BLUE)
    d.text((x0 + 42, y0 - 21), name, font=f, fill='#ffffff')
    # the door (gap in the left wall) where the desk sits
    return (x0, (y0 + y1) / 2)


def room(d, box, name, label=None):
    """A room = a method; an optional label on its door = the annotation."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 18, fill='#ffffff', outline=INK, width=5)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2 + 6, name, font(SANS_B, 38), INK)
    ctext(d, (x0 + x1) / 2, y1 - 58, 'room', font(SANS_B, 40), INK)
    if label:
        f = font(MONO_B, 34)
        tw = d.textlength(label, font=f)
        cx = (x0 + x1) / 2
        d.rounded_rectangle((cx - tw / 2 - 16, y0 + 22, cx + tw / 2 + 16, y0 + 74), 10, fill='#fff4e5', outline=ORANGE, width=4)
        d.text((cx - tw / 2, y0 + 28), label, font=f, fill=ORANGE)
        ctext(d, cx, y0 + 82, 'label on the door', font(SANS_B, 32), '#9a3412')


def desk(d, cx, cy, caption, col=INK):
    """The front desk = the proxy: a person behind a counter, in front of the office door."""
    d.ellipse((cx - 26, cy - 96, cx + 26, cy - 44), fill='#ffffff', outline=col, width=6)   # head
    d.arc((cx - 46, cy - 46, cx + 46, cy + 40), 180, 360, fill=col, width=6)              # shoulders
    d.rounded_rectangle((cx - 80, cy - 6, cx + 80, cy + 60), 10, fill='#e8edf6', outline=col, width=6)  # counter
    f = font(SANS_B, 36)
    for k, line in enumerate(caption.split('\n')):
        ctext(d, cx, cy + 74 + k * 42, line, f, col)


def visitor(d, cx, cy, caption):
    d.ellipse((cx - 24, cy - 90, cx + 24, cy - 42), outline=INK, width=6)
    d.line((cx, cy - 42, cx, cy + 20), fill=INK, width=6)
    d.line((cx - 34, cy - 20, cx + 34, cy - 20), fill=INK, width=6)
    d.line((cx, cy + 20, cx - 28, cy + 70), fill=INK, width=6)
    d.line((cx, cy + 20, cx + 28, cy + 70), fill=INK, width=6)
    f = font(SANS_B, 36)
    for k, line in enumerate(caption.split('\n')):
        ctext(d, cx, cy + 84 + k * 42, line, f, INK)


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
    import math
    a = math.atan2(yb - ya, xb - xa)
    s = 30
    d.polygon(((xb, yb), (xb - s * math.cos(a - 0.45), yb - s * math.sin(a - 0.45)),
               (xb - s * math.cos(a + 0.45), yb - s * math.sin(a + 0.45))), fill=col)


def tag(d, x, y, text, col, size=32):
    f = font(SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x - tw / 2 - 14, y - 6, x + tw / 2 + 14, y + size + 12), 10, fill='#ffffff', outline=col, width=4)
    d.text((x - tw / 2, y), text, font=f, fill=col)


def check(d, x, y, col=GREEN):
    d.line((x, y + 22, x + 18, y + 42, x + 52, y), fill=col, width=10, joint='curve')


out = os.path.join(EP, 'video', 'frames')
os.makedirs(out, exist_ok=True)

# shared layout for pictures 1 and 2: visitor, desk, one office with two rooms
VX, DX, OFF = 140, 410, (560, 230, 1510, 780)
RA, RB = (600, 330, 955, 700), (1115, 330, 1470, 700)
MID = 515


def office_scene(title):
    im, d = base(title)
    office(d, OFF, 'Office = the Checkout bean')
    room(d, RA, 'placeOrder')
    room(d, RB, 'saveAndCharge', label='@Transactional')
    return im, d


# 1. the office, its rooms, the front desk
im, d = office_scene('An office with a front desk')
visitor(d, VX, MID, 'a call from\noutside')
desk(d, DX, MID, 'Front desk\n= the proxy')
arrow(d, [(VX + 50, MID - 20), (DX - 92, MID - 20)], GREEN)
arrow(d, [(DX + 92, MID - 20), (RA[0] - 6, MID - 20)], GREEN)
ctext(d, W / 2, 830, 'Calls from outside always pass the front desk.', font(SANS_B, 46), INK)
ctext(d, W / 2, 892, 'The desk reads the label on the door.', font(SANS_B, 46), ORANGE)
im.save(os.path.join(out, 'desk-1-office.png'))

# 2. the trap: through the desk into placeOrder, then down the hall to saveAndCharge
im, d = office_scene('The trap: a walk down the hall')
visitor(d, VX, MID, 'the Buy\nclick')
desk(d, DX, MID, 'Front desk')
arrow(d, [(VX + 50, MID - 20), (DX - 92, MID - 20)], GREEN)
arrow(d, [(DX + 92, MID - 20), (RA[0] - 6, MID - 20)], GREEN)
arrow(d, [(RA[2] + 6, 580), (RB[0] - 6, 580)], RED, width=9, dashed=True)
tag(d, (RA[2] + RB[0]) / 2, 500, 'this.', RED, size=36)
ctext(d, (RA[2] + RB[0]) / 2, 714, 'down the hall: the desk never sees this walk', font(SANS_B, 30), RED)
ctext(d, W / 2, 830, 'this.saveAndCharge(): down the hall, inside the office', font(SANS_B, 40), RED)
ctext(d, W / 2, 892, 'No desk, so nobody reads the label: no transaction.', font(SANS_B, 44), INK)
im.save(os.path.join(out, 'desk-2-hall.png'))

# 3. the fix: saveAndCharge in its own office with its own front desk
im, d = base('The fix: its own office, its own desk')
office(d, (100, 250, 600, 740), 'Checkout bean')
room(d, (150, 350, 550, 680), 'placeOrder')
DX2 = 800
office(d, (1000, 250, 1500, 740), 'OrderWriter bean')
room(d, (1040, 350, 1460, 680), 'saveAndCharge', label='@Transactional')
desk(d, DX2, 500, "OrderWriter's\nfront desk\n= writer")
arrow(d, [(520, 470), (DX2 - 92, 470)], GREEN)
arrow(d, [(DX2 + 92, 470), (1034, 470)], GREEN)
tag(d, DX2, 714, 'starts a transaction', GREEN, size=28)
ctext(d, W / 2, 790, 'writer.saveAndCharge(): out of Checkout,', font(SANS_B, 44), INK)
ctext(d, W / 2, 852, "in through OrderWriter's front desk", font(SANS_B, 44), GREEN)
im.save(os.path.join(out, 'desk-3-fix.png'))
print('desk frames written')
