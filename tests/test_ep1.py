"""Episode 1 (@Transactional self-invocation): what the two captured runs must show (PLAN rev 2 #1, section 4.3).
Written before any capture: red until scripts/ep1.sh has produced ep1-transactional/evidence/replays/.
Lines are matched on the message text, never on the abbreviated logger column (acc M1).
"""
import json
import os
import unittest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(LAB, 'ep1-transactional', 'evidence', 'replays')


def lines(scenario):
    with open(os.path.join(EV, scenario, 'run.jsonl'), encoding='utf-8') as f:
        return [json.loads(ln)['text'] for ln in f if ln.strip()]


def meta(scenario):
    with open(os.path.join(EV, scenario, 'run.meta.json'), encoding='utf-8') as f:
        return json.load(f)


def has(ls, text):
    return [t for t in ls if text in t]


class Trap(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep1-trap')

    def test_boot_4_1_2_and_exit_0(self):
        self.assertEqual(meta('ep1-trap')['versions']['springBoot'], '4.1.2')
        self.assertEqual(meta('ep1-trap')['exitCode'], 0)

    def test_the_insert_ran_without_a_transaction(self):
        self.assertEqual(len(has(self.l, 'Executing prepared SQL update')), 1)
        self.assertEqual(has(self.l, 'LAB: at the insert, transaction active = '),
                         ['LAB: at the insert, transaction active = false'])

    def test_no_transaction_was_created_or_rolled_back(self):
        self.assertFalse(has(self.l, 'Creating new transaction with name ['))
        self.assertFalse(has(self.l, 'Initiating transaction rollback'))
        self.assertFalse(has(self.l, 'Getting transaction for ['))

    def test_the_row_stayed(self):
        self.assertEqual(has(self.l, 'LAB: orders after failure = '), ['LAB: orders after failure = 1'])
        self.assertEqual(len(has(self.l, 'LAB: placeOrder threw PaymentDeclinedException')), 1)


class Fix(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep1-fix')

    def test_boot_4_1_2_and_exit_0(self):
        self.assertEqual(meta('ep1-fix')['versions']['springBoot'], '4.1.2')
        self.assertEqual(meta('ep1-fix')['exitCode'], 0)

    def test_a_transaction_was_created_then_rolled_back_in_that_order(self):
        order = ['Creating new transaction with name [lab.fix.OrderWriter.saveAndCharge]',
                 'Executing prepared SQL update',
                 'LAB: at the insert, transaction active = true',
                 'Initiating transaction rollback',
                 'Rolling back JDBC transaction on Connection']
        idx = []
        for text in order:
            hits = [i for i, t in enumerate(self.l) if text in t]
            self.assertEqual(len(hits), 1, (text, hits))
            idx.append(hits[0])
        self.assertEqual(idx, sorted(idx), 'order')

    def test_the_row_was_undone(self):
        self.assertEqual(has(self.l, 'LAB: orders after failure = '), ['LAB: orders after failure = 0'])


class BeforeAfterPanel(unittest.TestCase):
    """The two-row before/after terminal (PLAN 4.4) carries lines copied from the captures, never retyped."""

    def test_panel_rows_are_captured_lines(self):
        path = os.path.join(LAB, 'ep1-transactional', 'video', 'before-after-panel.txt')
        with open(path, encoding='utf-8') as f:
            rows = [r.rstrip('\n') for r in f]
        trap, fix = lines('ep1-trap'), lines('ep1-fix')
        for r in rows:   # '# ...' rows are our labels; a trailing ' …' marks a cut line (the rest is verbatim)
            body = r[6:][:-2] if r.endswith(' …') else r[6:]
            if r.startswith('trap: '):
                self.assertTrue(any(body in t for t in trap), r)
            elif r.startswith('fix:  '):
                self.assertTrue(any(body in t for t in fix), r)
            else:
                self.assertTrue(r.startswith('# '), r)
            self.assertLessEqual(len(r), 64, r)


if __name__ == '__main__':
    unittest.main()
