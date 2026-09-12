// 抖音 Loon 信息流广告过滤。异常或非 JSON 响应直接放行。
// 首页、侧栏和底栏由插件内的 Loon 原生 JSON Rewrite 处理。
const options = Object.assign({
  feed_ads: true
}, typeof $argument === 'object' && $argument ? $argument : {});

const url = String($request && $request.url || '');
let changed = 0;

function objectHasContent(value) {
  return value && typeof value === 'object' && Object.keys(value).length > 0;
}

function isAd(item) {
  if (!item || typeof item !== 'object') return false;
  const target = item.aweme && typeof item.aweme === 'object' ? item.aweme : item;
  return target.is_ads === true || target.is_ads === 1 || target.is_ad === true ||
    target.is_ad === 1 || objectHasContent(target.ad_info) ||
    (typeof target.raw_ad_data === 'string' && target.raw_ad_data.length > 2) ||
    objectHasContent(target.raw_ad_data);
}

function filterKnownLists(value, depth = 0) {
  if (!value || typeof value !== 'object' || depth > 18) return;
  if (Array.isArray(value)) {
    value.forEach(item => filterKnownLists(item, depth + 1));
    return;
  }
  for (const key of ['aweme_list', 'item_list']) {
    if (!Array.isArray(value[key])) continue;
    const before = value[key].length;
    value[key] = value[key].filter(item => !isAd(item));
    changed += before - value[key].length;
  }
  if (Array.isArray(value.data) && value.data.some(item => item && item.aweme)) {
    const before = value.data.length;
    value.data = value.data.filter(item => !isAd(item));
    changed += before - value.data.length;
  }
  Object.keys(value).forEach(key => filterKnownLists(value[key], depth + 1));
}

try {
  const body = JSON.parse($response.body);
  if (options.feed_ads && /\/aweme\/v\d+\/(?:feed|follow\/feed|nearby\/feed|search\/item|general\/search\/single)\//i.test(url)) {
    filterKnownLists(body);
  }
  if (changed) {
    console.log(`[DouyinClean] changed=${changed}`);
    $done({body: JSON.stringify(body)});
  } else $done({});
} catch (error) {
  console.log(`[DouyinClean] skipped: ${error}`);
  $done({});
}
