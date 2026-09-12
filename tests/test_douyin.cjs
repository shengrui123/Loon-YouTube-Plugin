const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');

const code = fs.readFileSync(path.join(__dirname, '../Douyin.Clean.Loon.js'), 'utf8');

function run(url, body, argument = {}) {
  let output;
  vm.runInNewContext(code, {
    $request: {url},
    $response: {body: JSON.stringify(body)},
    $argument: argument,
    $done: value => { output = value; },
    console: {log() {}}
  });
  return output && output.body ? JSON.parse(output.body) : body;
}

const feed = run('https://aweme.snssdk.com/aweme/v1/feed/?x=1', {
  aweme_list: [
    {aweme_id: 'normal', desc: '普通视频'},
    {aweme_id: 'shop', commerce_config_data: {type: 1}},
    {aweme_id: 'ad1', is_ads: true},
    {aweme_id: 'ad2', ad_info: {creative_id: '2'}}
  ]
}, {feed_ads: true});
assert.deepEqual(feed.aweme_list.map(item => item.aweme_id), ['normal', 'shop']);

const homepage = run('https://api5-normal-m.amemv.com/aweme/homepage/render/?x=1', {
  data: {
    tab_config: {experiment: true},
    tab_list: [{extra: {
      tab_list: [
        {tab_id: 'homepage_follow'},
        {tab_id: 'homepage_mall'},
        {tab_id: 'homepage_hot_container'},
        {tab_id: 'homepage_tablive'}
      ],
      side_bar: {modules: [
        {module_title: '常用功能', items: []},
        {module_title: '设置', items: [{name: '设置'}]}
      ]}
    }}]
  }
}, {minimal_tabs: true, keep_live: false, clean_sidebar: true, clean_tabbar: true});
assert.deepEqual(homepage.data.tab_list[0].extra.tab_list.map(tab => tab.tab_id), [
  'homepage_follow', 'homepage_hot_container'
]);
assert.equal(homepage.data.tab_config, undefined);
assert.deepEqual(homepage.data.tab_list[0].extra.side_bar.modules.map(module => module.module_title), ['设置']);

const settings = run('https://aweme.snssdk.com/tfe/api/request_combine/v1/?need_personal_recommend=1', {
  data: {'/service/settings/v3/': {body: {data: {settings: {
    homepage_two_session_tab_skin_2025: true,
    homepage_tab_skin_enable: true,
    dynamic_plus_icon_config: {icon: 'promo'},
    unrelated: true
  }}}}}
}, {clean_tabbar: true});
const cleaned = settings.data['/service/settings/v3/'].body.data.settings;
assert.equal(cleaned.homepage_two_session_tab_skin_2025, false);
assert.equal(cleaned.homepage_tab_skin_enable, false);
assert.equal(cleaned.dynamic_plus_icon_config, undefined);
assert.equal(cleaned.unrelated, true);

const sidebar = run('https://api5-normal-m.amemv.com/aweme/homepage/sidebar_data/?x=1', {
  data_map: {recently_apps: [1], recently_users: [2], settings: [3]}
}, {clean_sidebar: true});
assert.deepEqual(sidebar.data_map, {settings: [3]});

console.log('PASS: feed ads, TikTok-style tabs, sidebar cleanup and tab-bar settings.');
