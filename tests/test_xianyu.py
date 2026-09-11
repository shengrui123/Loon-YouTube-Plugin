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
            for index in range(6):
                if index == 5 and isinstance(value, dict) and isinstance(value.get("data"), dict) and isinstance(value["data"].get("sections"), list):
                    continue  # Known feed array is intentionally emptied.
                self.assertEqual(run(index, value), value)

    def test_profile(self):
        def section(name, **item):
            return {'template': {'name': name}, 'item': item}
        account = section('my_fy25_user_info', level={'banner': 'x'}, nickname='keep')
        trade = section('trade', orders=4)
        unknown = section('new_unknown')
        value = {'data': {'container': {'sections': [account, trade, unknown, None, section('my_fy25_slider'), section('xianyu_home_fish_my_banner_card_2023'), section('my_fy25_community'), section('my_fy25_tools')]}}}
        clean = run(2, value)
        sections = clean['data']['container']['sections']
        self.assertEqual(len(sections), 5)
        self.assertEqual(sections[0]['item'], {'nickname': 'keep'})
        self.assertEqual(sections[1:4], [trade, unknown, None])
        self.assertEqual(len(run(3, clean)['data']['container']['sections']), 4)
        self.assertEqual(len(run(3, value)['data']['container']['sections']), 7)
        for bad in [None, [], 3, {}, {'sections': None}, {'sections': {}}, {'sections': [None, 3, {}, {'item': None}]}]:
            obj = {'data': {'container': bad}}
            self.assertEqual(run(2, obj), obj)
            self.assertEqual(run(3, obj), obj)

    def test_profile_urls(self):
        for host in ['acs.m.goofish.com', 'g-acs.m.goofish.com']:
            url = 'https://' + host + '/gw/mtop.idle.user.page.my.adapter/1.0/'
            for pattern in PATTERNS[4:6]:
                self.assertTrue(pattern.search(url))
                self.assertFalse(pattern.search(url.replace('adapter/', 'adapter.extra/')))
                self.assertFalse(pattern.search(url.replace(host, host + '.evil')))

    def test_profile_business_and_feed(self):
        cards = [{'sectionBizCode': name} for name in ['head', 'user_info', 'trade', 'marketing', 'recycle', '']]+[{}, None, 3]
        value = {'data': {'ability': [1], 'container': {'sections': cards}, 'other': 'keep'}}
        result = run(4, value)
        self.assertEqual(result['data']['container']['sections'], cards[:3]+cards[5:])
        self.assertEqual(result['data']['ability'], [])
        self.assertEqual(result['data']['other'], 'keep')
        self.assertEqual(run(5, {'data': {'sections': [1], 'cursor': 'keep'}}), {'data': {'sections': [], 'cursor': 'keep'}})

    def test_new_endpoints(self):
        urls = ['https://acs.m.goofish.com/gw/mtop.idle.splash.ads/1.0/', 'https://iyes.youku.com/uts/v1/start/?x=1', 'https://g-acs.m.goofish.com/gw/mtop.idle.user.page.my.adapter/1.0/', 'https://acs.m.goofish.com/gw/mtop.taobao.idle.item.buy.feeds/1.0/']
        for pattern, url in zip(PATTERNS[7:], urls):
            self.assertTrue(pattern.search(url))
            self.assertFalse(pattern.search(url.replace('.com/', '.com.evil/')))
        self.assertFalse(PATTERNS[7].search('https://acs.m.goofish.com/gw/mtop.idle.splash.ads.extra/1.0/'))
        self.assertFalse(PATTERNS[8].search('https://iyes.youku.com/video/'))

    def test_url_boundaries(self):
        urls = ['https://acs.m.taobao.com/gw/mtop.taobao.idle.home.welcome/1.0/?x=1', 'https://acs.m.goofish.com/gw/mtop.taobao.idle.user.strategy.get/1.0/', 'https://g-acs.m.goofish.com/gw/mtop.taobao.idlehome.home.nextfresh/1.0/', 'https://g-acs.m.goofish.com/gw/mtop.taobao.idlemtopsearch.search/1.0/']
        self.assertEqual(len(PATTERNS), 11)
        for index, url in enumerate(urls):
            self.assertEqual([bool(p.search(url)) for p in PATTERNS[:4]], [i == index for i in range(4)])
            for bad in [url.replace('/1.0/', 'extra/1.0/'), url.replace('.com/', '.com.evil/'), url.replace('/gw/', '/h5/'), url.replace('https:', 'http:')]:
                self.assertFalse(any(p.search(bad) for p in PATTERNS))


if __name__ == '__main__':
    unittest.main()
