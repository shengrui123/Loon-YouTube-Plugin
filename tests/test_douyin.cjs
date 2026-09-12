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

console.log('PASS: explicit feed ads are removed and ordinary commerce posts are retained.');
