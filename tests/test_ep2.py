"""Episode 2 (prototype bean injected into a singleton): what the two captured runs must show (PLAN rev 2 #2).
Written before any capture. Framework evidence: TRACE "Creating instance of bean 'ticket'" from the bean factory,
switched on by the lab after startup (acc M4), so the replay is not flooded with startup lines.
"""
import json
import os
import re
import unittest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(LAB, 'ep2-prototype', 'evidence', 'replays')
TRACE_ON = 'LAB: bean-factory TRACE logging on from here'
MADE = re.compile(r'^LAB: Ticket #\d+ constructed$')
SERVED = re.compile(r'^LAB: call (\d) served by Ticket #(\d+), identityHashCode ([0-9a-f]+)$')


def lines(scenario):
    with open(os.path.join(EV, scenario, 'run.jsonl'), encoding='utf-8') as f:
        return [json.loads(ln)['text'] for ln in f if ln.strip()]


def meta(scenario):
    with open(os.path.join(EV, scenario, 'run.meta.json'), encoding='utf-8') as f:
        return json.load(f)


def after_trace_on(ls):
    return ls[ls.index(TRACE_ON) + 1:]


class Common(unittest.TestCase):
    def test_boot_4_1_2_exit_0(self):
        for s in ('ep2-trap', 'ep2-fix'):
            self.assertEqual(meta(s)['versions']['springBoot'], '4.1.2')
            self.assertEqual(meta(s)['exitCode'], 0)


class Trap(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep2-trap')

    def test_one_ticket_built_at_startup_before_the_calls(self):
        made = [t for t in self.l if MADE.match(t)]
        self.assertEqual(made, ['LAB: Ticket #1 constructed'])
        self.assertLess(self.l.index(made[0]), self.l.index(TRACE_ON))

    def test_three_calls_one_ticket_same_identity(self):
        calls = [SERVED.match(t) for t in self.l if SERVED.match(t)]
        self.assertEqual([m.group(1) for m in calls], ['1', '2', '3'])
        self.assertEqual({m.group(2) for m in calls}, {'1'})
        self.assertEqual(len({m.group(3) for m in calls}), 1)

    def test_the_container_creates_no_ticket_during_the_calls(self):
        self.assertFalse([t for t in after_trace_on(self.l) if "Creating instance of bean 'ticket'" in t])


class Fix(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep2-fix')

    def test_no_ticket_at_startup_three_during_the_calls(self):
        made = [t for t in self.l if MADE.match(t)]
        self.assertEqual(made, ['LAB: Ticket #1 constructed', 'LAB: Ticket #2 constructed', 'LAB: Ticket #3 constructed'])
        self.assertGreater(self.l.index(made[0]), self.l.index(TRACE_ON))

    def test_three_calls_three_tickets(self):
        calls = [SERVED.match(t) for t in self.l if SERVED.match(t)]
        self.assertEqual([m.group(2) for m in calls], ['1', '2', '3'])
        self.assertEqual(len({m.group(3) for m in calls}), 3)

    def test_the_container_logs_each_creation(self):
        created = [t for t in after_trace_on(self.l) if "Creating instance of bean 'ticket'" in t]
        self.assertEqual(len(created), 3)


class Panels(unittest.TestCase):
    def test_before_after_rows_are_captured_lines(self):
        path = os.path.join(LAB, 'ep2-prototype', 'video', 'before-after-panel.txt')
        with open(path, encoding='utf-8') as f:
            rows = [r.rstrip('\n') for r in f]
        trap, fix = lines('ep2-trap'), lines('ep2-fix')
        for r in rows:   # '# ...' rows are our labels; a trailing ' …' marks a cut line
            body = r[6:][:-2] if r.endswith(' …') else r[6:]
            if r.startswith('trap: '):
                self.assertTrue(any(body in t for t in trap), r)
            elif r.startswith('fix:  '):
                self.assertTrue(any(body in t for t in fix), r)
            else:
                self.assertTrue(r.startswith('# '), r)
            self.assertLessEqual(len(r), 60, r)


if __name__ == '__main__':
    unittest.main()
