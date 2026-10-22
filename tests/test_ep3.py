"""Episode 3 (@Configuration vs @Component, lite mode): what the two captured runs must show (PLAN rev 2 #3).
Written before any capture. acc M3: the container logs ONE creation of the auditLog bean in both runs; the second
object in the trap is a plain `new` the container never sees; the fix's class is CGLIB-enhanced (TRACE line).
"""
import json
import os
import re
import unittest

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(LAB, 'ep3-configuration', 'evidence', 'replays')
BUILT = re.compile(r'^LAB: AuditLog constructor ran, #\d+$')


def lines(scenario):
    with open(os.path.join(EV, scenario, 'run.jsonl'), encoding='utf-8') as f:
        return [json.loads(ln)['text'] for ln in f if ln.strip()]


def meta(scenario):
    with open(os.path.join(EV, scenario, 'run.meta.json'), encoding='utf-8') as f:
        return json.load(f)


def count(ls, text):
    return len([t for t in ls if text in t])


class Common(unittest.TestCase):
    def test_boot_4_1_2_exit_0(self):
        for s in ('ep3-trap', 'ep3-fix'):
            self.assertEqual(meta(s)['versions']['springBoot'], '4.1.2')
            self.assertEqual(meta(s)['exitCode'], 0)

    def test_the_container_creates_the_auditlog_bean_once_in_both_runs(self):
        for s in ('ep3-trap', 'ep3-fix'):
            self.assertEqual(count(lines(s), "Creating shared instance of singleton bean 'auditLog'"), 1, s)


class Trap(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep3-trap')

    def test_the_constructor_ran_twice(self):
        self.assertEqual([t for t in self.l if BUILT.match(t)],
                         ['LAB: AuditLog constructor ran, #1', 'LAB: AuditLog constructor ran, #2'])

    def test_two_different_objects(self):
        self.assertEqual(count(self.l, 'LAB: same object? false'), 1)

    def test_no_enhanced_appbeans(self):
        self.assertEqual(count(self.l, 'Successfully enhanced lab.trap.AppBeans'), 0)


class Fix(unittest.TestCase):
    def setUp(self):
        self.l = lines('ep3-fix')

    def test_the_constructor_ran_once(self):
        self.assertEqual([t for t in self.l if BUILT.match(t)], ['LAB: AuditLog constructor ran, #1'])

    def test_one_object(self):
        self.assertEqual(count(self.l, 'LAB: same object? true'), 1)

    def test_appbeans_was_enhanced_with_cglib(self):
        hits = [t for t in self.l if 'Successfully enhanced lab.fix.AppBeans' in t]
        self.assertEqual(len(hits), 1)
        self.assertIn('lab.fix.AppBeans$$SpringCGLIB$$', hits[0])


class Panels(unittest.TestCase):
    def test_panel_rows_are_captured_lines(self):
        for name in ('before-after-panel.txt', 'outcome-panel.txt'):
            path = os.path.join(LAB, 'ep3-configuration', 'video', name)
            with open(path, encoding='utf-8') as f:
                rows = [r.rstrip('\n') for r in f]
            trap, fix = lines('ep3-trap'), lines('ep3-fix')
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
