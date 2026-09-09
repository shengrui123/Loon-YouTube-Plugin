"""Offline checks; does not replace Loon/iOS integration testing."""
import json
from pathlib import Path
import re
import subprocess
import unittest

PLUGIN = Path(__file__).resolve().parents[1] / 'Xianyu.Clean.Loon.plugin'
TEXT = PLUGIN.read_text()
FILTERS = re.findall(r'response\.json\.jq\(`([^`]+)`\)', TEXT)
PATTERNS = [re.compile(p.replace(r'\/', '/')) for p in re.findall(r'\$\{url\} ~= /(.+?)(?<!\\)/', TEXT)]


def run(index, value):
    result = subprocess.run(['jq', '-c', FILTERS[index]], input=json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


class XianyuTests(unittest.TestCase):
    def test_home(self):
        value = {'data': {'sections': [{'data': {'bizType': 'item'}}, {'data': {'bizType': 'banner'}}, None, {'data': 42}], 'feedsCount': 4, 'cursor': 'keep'}}
        result = run(0, value)
        self.assertEqual(result['data']['sections'], [value['data']['sections'][i] for i in (0, 2, 3)])
        self.assertEqual(result['data']['feedsCount'], 3)
        self.assertEqual(result['data']['cursor'], 'keep')

    def test_search(self):
        def card(kind):
            return {'data': {'item': {'main': {'clickParam': {'args': {'item_type': kind}}}}}}
        value = {'data': {'resultList': [card('goods'), card('ad'), card(''), {}, 3], 'total': 100, 'nextPage': 2}}
        result = run(1, value)
        self.assertEqual(result['data']['resultList'], [value['data']['resultList'][i] for i in (0, 2, 3, 4)])
        self.assertEqual(result['data']['total'], 100)
        self.assertEqual(result['data']['nextPage'], 2)

    def test_unknown_structures(self):
        for value in [None, [], 3, 'text', {}, {'data': None}, {'data': []}, {'data': {'sections': {}, 'resultList': 'text'}}, {'data': {'sections': [None, {}, 2], 'feedsCount': 100}}]:
            for index in range(2):
                self.assertEqual(run(index, value), value)

    def test_url_boundaries(self):
        urls = ['https://acs.m.taobao.com/gw/mtop.taobao.idle.home.welcome/1.0/?x=1', 'https://acs.m.goofish.com/gw/mtop.taobao.idle.user.strategy.get/1.0/', 'https://g-acs.m.goofish.com/gw/mtop.taobao.idlehome.home.nextfresh/1.0/', 'https://g-acs.m.goofish.com/gw/mtop.taobao.idlemtopsearch.search/1.0/']
        self.assertEqual(len(PATTERNS), 4)
        for index, url in enumerate(urls):
            self.assertEqual([bool(p.search(url)) for p in PATTERNS], [i == index for i in range(4)])
            for bad in [url.replace('/1.0/', 'extra/1.0/'), url.replace('.com/', '.com.evil/'), url.replace('/gw/', '/h5/'), url.replace('https:', 'http:')]:
                self.assertFalse(any(p.search(bad) for p in PATTERNS))


if __name__ == '__main__':
    unittest.main()
