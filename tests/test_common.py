"""Checks every episode shares (PLAN rev 2, section 4.5): every overlaid tag/caption sits on a line that exists verbatim in
the captured log, and nothing private leaves the lab. Run in Docker: bash tests/run-tests.sh
"""
import glob
import json
import os
import re
import subprocess
import unittest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def P(*p):
    return os.path.join(LAB, *p)


def run_lines(run_jsonl):
    with open(run_jsonl, encoding='utf-8') as f:
        return [json.loads(ln)['text'] for ln in f if ln.strip()]


def js_regex(pattern):
    # the annotations use JS regexes; the subset used here (escapes, groups, lookahead, $) means the same in Python
    return re.compile(pattern)


def matches(lines, ref):
    rx = js_regex(ref['match'])
    hits = [i for i, t in enumerate(lines) if rx.search(t)]
    return hits


class TagsSitOnRealLines(unittest.TestCase):
    """T-tag: every event (tag or caption) and every `through` matches exactly one captured line (or its `nth`), the
    clause regex matches inside that line, and the same line is in the raw `docker logs --timestamps` output."""

    def annotations(self):
        found = sorted(glob.glob(P('ep*', 'evidence', 'replays', '*', '*.replay.json')))
        return found

    def test_every_tag_is_on_a_captured_line(self):
        anns = self.annotations()
        self.assertTrue(anns, 'no replay annotations yet')
        for ann_path in anns:
            with open(ann_path, encoding='utf-8') as f:
                ann = json.load(f)
            run = os.path.join(os.path.dirname(ann_path), ann['run'])
            lines = run_lines(run)
            raw = os.path.join(os.path.dirname(ann_path), 'raw', 'stdout.txt')
            raw_text = None
            if os.path.exists(raw):
                with open(raw, encoding='utf-8') as f:
                    raw_text = f.read()
            for ev in ann['events']:
                for key in ('at', 'through'):
                    ref = ev.get(key)
                    if not ref or 'match' not in ref:
                        continue
                    hits = matches(lines, ref)
                    if 'nth' in ref:
                        self.assertGreater(len(hits), ref['nth'], (ann_path, ev['id'], key))
                        hit = hits[ref['nth'] - 1]   # nth is 1-based (mcp-canvas compileReplay)
                    else:
                        self.assertEqual(len(hits), 1, (ann_path, ev['id'], key, hits))
                        hit = hits[0]
                    if key == 'at' and 'clause' in ref:
                        self.assertTrue(js_regex(ref['clause']).search(lines[hit]), (ann_path, ev['id']))
                    if raw_text is not None:
                        self.assertIn(lines[hit], raw_text, (ann_path, ev['id'], 'not in raw docker logs'))
                text = ev.get('tag') or ev.get('caption')
                self.assertTrue(text, (ann_path, ev['id'], 'event without a message'))
                if 'tag' in ev:
                    self.assertLessEqual(len(ev['tag'].split()), 6, (ann_path, ev['id'], ev['tag']))


# Host paths (they carry the account name) and tokens. Extra private words come from LAB_PRIVATE_WORDS
# (comma-separated), so this public file never spells them out. The patterns are written so they do not match themselves.
_EXTRA = [re.escape(w.strip()) for w in os.environ.get('LAB_PRIVATE_WORDS', '').split(',') if w.strip()]
PRIVATE = re.compile('|'.join([r'[A-Za-z]:[/\\]+Users', r'/[c]/Users', r'/home/[a-z]', r'sk-[a]nt-', r'Bearer [A-Za-z0-9]',
                               r'@gmail\.com'] + _EXTRA), re.I)


class NothingPrivate(unittest.TestCase):
    def test_no_host_paths_names_or_tokens_in_any_file(self):
        bad = []
        for path in glob.glob(P('**', '*'), recursive=True):
            rel = os.path.relpath(path, LAB).replace('\\', '/')
            if os.path.isdir(path) or '/target/' in '/' + rel or '/raw/' in '/' + rel or rel.startswith('.git/'):
                continue
            if rel.endswith(('.png', '.jpg', '.jar')):
                continue
            with open(path, encoding='utf-8', errors='replace') as f:
                if PRIVATE.search(f.read()):
                    bad.append(rel)
        self.assertFalse(bad, bad)

    def test_the_extra_words_are_really_checked(self):
        if not _EXTRA:
            self.skipTest('LAB_PRIVATE_WORDS not set')
        self.assertTrue(PRIVATE.search(os.environ['LAB_PRIVATE_WORDS'].split(',')[0].strip()))


if __name__ == '__main__':
    unittest.main()
