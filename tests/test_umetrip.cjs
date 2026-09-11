const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync(require('node:path').join(__dirname, '../Umetrip.Clean.Loon.js'), 'utf8');
const ctx = {Uint8Array, TextDecoder, console: {log() {}}, $request: {headers: {}}, $response: {}, $done() {}};
vm.createContext(ctx);
vm.runInContext(code, ctx);
const enc = n => [...ctx.encodeVarint(n)];
const field = (n, b) => Uint8Array.from([...enc(n*8+2), ...enc(b.length), ...b]);
const str = (n, s) => field(n, Buffer.from(s));
const join = (...b) => ctx.concatBytes(b);
function run(payload, rpid) {
  const results = [];
  const original = join(str(5, rpid), field(7, payload));
  vm.runInNewContext(code, {...ctx, $request: {headers: {rpid}}, $response: {body: original}, $done: x => results.push(x)});
  assert.equal(results.length, 1);
  return ctx.parseMessage(results[0].body || original).find(f => f.field === 7).data;
}
function jsonRun(object, rpid) {
  return JSON.parse(ctx.bytesToUtf8(ctx.parseMessage(run(str(1, JSON.stringify(object)), rpid))[0].data));
}
const mine = {children: ['礼金中心','票券权益','特价专区','全部订单','礼金余额','我的钱包'].map((title, i) => ({title, cardId:i})), childrenIndex: {}};
let result = jsonRun(mine, '1100001');
assert.deepEqual(result.children.map(x=>x.title), ['全部订单','礼金余额','我的钱包']);
assert.deepEqual(result.childrenIndex, {'3':0,'4':1,'5':2});
assert.equal(jsonRun(mine, 'unknown').children.length, 6);
result = jsonRun({cards: [{title:'广告横幅',cardType:'ADVERT'}, {title:'订单'}]}, '1100001');
assert.equal(result.cards.length,1);
result = jsonRun({tabs:['首页','行程','经验','动态','我'].map(title=>({title})), content:[{title:'经验',text:'普通文章'}], ranks:[{title:'风景榜'},{title:'延误榜'},{title:'航班查询'}]}, 'unknown');
assert.equal(result.tabs.length,4);
assert.equal(result.content.length,1);
assert.deepEqual(result.ranks,[{title:'航班查询'}]);
const proto = join(...['首页','行程','经验','动态','我'].map(label=>field(3,str(1,label))));
assert.equal(ctx.parseMessage(run(proto,'unknown')).length,4);
const single = field(3,str(1,'经验'));
assert.deepEqual([...run(single,'unknown')],[...single]);
assert.deepEqual([...run(Uint8Array.from([255]),'unknown')],[255]);
assert.deepEqual([...run(str(1,'ad'),'1000019')],[10,0,16,0,32,0]);
console.log('PASS: mine scope, ads, indexes, tabs, rankings, protobuf navigation, single-node preservation, malformed input, splash.');
// 回归：删除内容后应移除嵌套 SECTION 外壳，并保留钱包与混合内容。
const shells = {children: [
 {cardId:1, cardType:'SECTION', children:[{cardId:2, children:[{title:'礼金中心'}], backgroundColor:'#fff', showArrow:true}]},
 {cardId:3, children:[{title:'票券权益'},{title:'我的钱包'}]},
 {cardId:4, children:[]},
 {cardId:5, title:'正常说明', children:[{title:'特价专区'}]}
], childrenIndex:{'1':0,'3':1,'4':2,'5':3}};
const cleanedShells = jsonRun(shells, '1100001');
assert.deepEqual(cleanedShells.children.map(x=>x.cardId),[3,4,5]);
assert.deepEqual(cleanedShells.childrenIndex,{'3':0,'4':1,'5':2});
assert.deepEqual(cleanedShells.children[0].children,[{title:'我的钱包'}]);
assert.deepEqual(jsonRun(shells,'unknown'),shells);
const onlyRemoved = field(6,join(field(3,str(1,'礼金中心')),field(3,str(1,'票券权益'))));
const normalSibling = str(9,'normal');
assert.deepEqual([...run(join(onlyRemoved,normalSibling),'1100001')],[...normalSibling]);
console.log('PASS: nested empty containers, mixed cards, pre-existing placeholders, indexes, mine-only scope, empty protobuf wrappers.');
