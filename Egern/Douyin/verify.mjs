import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const code = await readFile(new URL('./feed.js', import.meta.url), 'utf8');
const { default: filter } = await import('data:text/javascript;base64,' + Buffer.from(code).toString('base64'));
async function run(text, status = 200) {
  return filter({ response: { status, body: {}, text: async () => text } });
}
const input = '{"id":1234567890123456789,"aweme_list":[{"id":9876543210987654321},{"is_ads":true},{"is_ad":1},{"is_ads":"1"},{"is_ads":false,"desc":"a,]}\\\""}],"has_more":1}';
const output = await run(input);
assert.equal(output.body, '{"id":1234567890123456789,"aweme_list":[{"id":9876543210987654321},{"is_ads":false,"desc":"a,]}\\\""}],"has_more":1}');
assert.equal(await run('{"aweme_list":[{"is_ads":false}]}'), undefined);
assert.equal(await run('{"aweme_list":[{"is_ads":true}]}', 500), undefined);
assert.equal(await run('not json'), undefined);
assert.equal((await run('{"nested":{"aweme_list":[{"is_ads":1}]},"aweme_list":[{"is_ads":1}]}')).body, '{"nested":{"aweme_list":[{"is_ads":1}]},"aweme_list":[]}');
console.log('Response filter tests passed');
