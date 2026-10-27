"""Meaningful read-only, content-coverage and offline packaging checks."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from build_reader import DEFAULT_SOURCE, collect_library, embedded_json


class ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = collect_library()

    def test_every_distributable_file_is_available(self):
        inventory = DEFAULT_SOURCE / '10_Progress_Tracking/file_inventory.csv'
        import csv
        with inventory.open(encoding='utf-8-sig') as file:
            expected = {row['Relative path'] for row in csv.DictReader(file)}
        expected.add('10_Progress_Tracking/file_inventory.csv')
        actual = {file['path'] for file in self.library['files']}
        self.assertTrue(expected <= actual, expected - actual)
        self.assertFalse(any('/build/' in path or '/~$' in path for path in actual))

    def test_original_files_are_unchanged(self):
        baseline = json.loads((APP/'original_files.sha256.json').read_text(encoding='utf-8'))
        changed = []
        for relative, expected in baseline.items():
            file = APP.parent / relative
            if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != expected:
                changed.append(relative)
        self.assertEqual(changed, [], 'Existing files changed during implementation')

    def test_question_bank_and_tables_keep_full_content(self):
        self.assertEqual(len(self.library['questions']), 200)
        self.assertEqual({q['ID'] for q in self.library['questions']}, {f'Q{i:03}' for i in range(1,201)})
        roadmap = next(f for f in self.library['files'] if f['path'].endswith('roadmap_64_weeks.csv'))
        self.assertEqual(len(roadmap['rows']),64)
        self.assertIn('Objective exit test',roadmap['columns'])
        self.assertIn('Objects, arrays and pointers',roadmap['rows'][1])
        self.assertEqual(self.library['stats']['implementedProjects'],1)

    def test_word_editions_are_readable_without_word(self):
        words = [f for f in self.library['files'] if f['kind'] == 'word']
        self.assertEqual(len(words),4)
        self.assertTrue(all(len(f['text']) > 1000 and not f['error'] for f in words))
        bank = next(f for f in words if 'Interview_Bank' in f['path'])
        self.assertIn('Q001',bank['text'])
        self.assertIn('Q200',bank['text'])

    def test_answers_are_classified_for_gated_access(self):
        by_path = {f['path']:f for f in self.library['files']}
        self.assertTrue(by_path['04_Skill_Assessments/answer_keys/D01_Key.md']['answer'])
        self.assertFalse(by_path['04_Skill_Assessments/questions/D01_Initial_Diagnostic.md']['answer'])
        self.assertTrue(by_path['03_JD_JR_Skills_and_Learning_Content/solutions/M01_Solutions.md']['answer'])

    def test_json_embedding_cannot_close_its_script_element(self):
        attack = {'text':'</script><img src=x onerror=alert(1)> & \u2028'}
        encoded = embedded_json(attack)
        self.assertNotIn('<',encoded)
        self.assertEqual(json.loads(encoded),attack)

    def test_index_is_offline_and_has_no_unfilled_tokens(self):
        import re
        html = (APP/'index.html').read_text(encoding='utf-8')
        self.assertNotRegex(html,r'<script[^>]+src=')
        self.assertNotRegex(html,r'<link[^>]+href=["\']https?://')
        self.assertNotIn('/* LIBRARY_JSON */',html)
        self.assertNotIn('/* READER_SCRIPT */',html)
        embedded = re.search(r'<script id="library-data" type="application/json">(.*?)</script>',html,re.S)
        self.assertIsNotNone(embedded)
        self.assertEqual(len(json.loads(embedded[1])['files']),len(self.library['files']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
