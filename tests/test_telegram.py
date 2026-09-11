import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('notify', Path(__file__).parents[1] / 'scripts/notify_telegram.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)

class Notifications(unittest.TestCase):
    def test_real_update(self):
        entries = n.affected_plugins('4a943ef', '16808c8', 'shengrui123/Loon-YouTube-Plugin')
        self.assertEqual([e[0] for e in entries], ['Umetrip.Clean.Loon.plugin'])
        self.assertTrue(entries[0][3])

    def test_new_plugin(self):
        entries = n.affected_plugins('770b1f2', 'fd7301b', 'shengrui123/Loon-YouTube-Plugin')
        self.assertEqual(len(entries), 1)
        self.assertFalse(entries[0][3])

    def test_no_change(self):
        self.assertEqual(n.affected_plugins('HEAD', 'HEAD', 'shengrui123/Loon-YouTube-Plugin'), [])

    def test_escape(self):
        text = n.message(('test.plugin', '<Title>', '&desc', True, '<script>'), 'owner/repo', 'abc')
        self.assertNotIn('<script>', text)
        self.assertIn('&lt;Title&gt;', text)

    def test_transport(self):
        import json
        import io
        with patch.object(n, 'urlopen', return_value=io.BytesIO(b'{"ok":true}')) as mock:
            n.send('test', 'dummy')
            payload = json.loads(mock.call_args.args[0].data)
            self.assertEqual(payload['chat_id'], '@Atlas_Corner')
            self.assertEqual(payload['text'], 'test')

if __name__ == '__main__':
    unittest.main()
