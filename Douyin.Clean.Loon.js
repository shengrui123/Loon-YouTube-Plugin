// 抖音 Loon 响应净化脚本。异常或非 JSON 响应直接放行。
// 2026-09-12：适配 feed、homepage/render、sidebar_data 与 request_combine。
const options = Object.assign({
  feed_ads: true,
  minimal_tabs: true,
  keep_live: false,
  clean_sidebar: true,
  clean_tabbar: true
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

function tabId(tab) {
  if (!tab || typeof tab !== 'object') return '';
  return String(tab.tab_id || tab.channel_id || tab.channelID || tab.id || '');
}

function cleanHomepage(root) {
  const data = root && root.data;
  if (!data || typeof data !== 'object') return;

  if (options.clean_tabbar && Object.prototype.hasOwnProperty.call(data, 'tab_config')) {
    delete data.tab_config;
    changed++;
  }

  const allowed = new Set(['homepage_follow', 'homepage_hot_container']);
  if (options.keep_live) allowed.add('homepage_tablive');
  if (!Array.isArray(data.tab_list)) return;

  for (const group of data.tab_list) {
    const extra = group && group.extra;
    if (!extra || typeof extra !== 'object') continue;
    if (options.minimal_tabs && Array.isArray(extra.tab_list)) {
      const before = extra.tab_list.length;
      extra.tab_list = extra.tab_list.filter(tab => allowed.has(tabId(tab)));
      changed += before - extra.tab_list.length;
    }
    if (options.clean_sidebar && extra.side_bar && Array.isArray(extra.side_bar.modules)) {
      const before = extra.side_bar.modules.length;
      extra.side_bar.modules = extra.side_bar.modules.filter(module => {
        const title = String(module && (module.module_title || module.title) || '');
        if (title === '常用功能') return false;
        const items = module && module.items;
        return !Array.isArray(items) || !items.some(item =>
          String(item && item.data && item.data.first_page_module && item.data.first_page_module.module_title || '') === '常用功能');
      });
      changed += before - extra.side_bar.modules.length;
    }
  }
  if (options.minimal_tabs) {
    const before = data.tab_list.length;
    data.tab_list = data.tab_list.filter(group => !group || !group.extra ||
      !Array.isArray(group.extra.tab_list) || group.extra.tab_list.length > 0);
    changed += before - data.tab_list.length;
  }
}

function cleanSidebar(root) {
  const map = root && root.data_map;
  if (!map || typeof map !== 'object') return;
  for (const key of ['recently_apps', 'recently_users']) {
    if (Object.prototype.hasOwnProperty.call(map, key)) {
      delete map[key];
      changed++;
    }
  }
}

function cleanSettings(value, depth = 0) {
  if (!value || typeof value !== 'object' || depth > 20) return;
  if (Array.isArray(value)) {
    value.forEach(item => cleanSettings(item, depth + 1));
    return;
  }
  for (const key of ['homepage_two_session_tab_skin_2025', 'homepage_tab_skin_enable']) {
    if (Object.prototype.hasOwnProperty.call(value, key) && value[key] !== false) {
      value[key] = false;
      changed++;
    }
  }
  for (const key of ['tab_bar_background_use_server_time', 'dynamic_plus_icon_config']) {
    if (Object.prototype.hasOwnProperty.call(value, key)) {
      delete value[key];
      changed++;
    }
  }
  Object.keys(value).forEach(key => cleanSettings(value[key], depth + 1));
}

try {
  const body = JSON.parse($response.body);
  if (options.feed_ads && /\/aweme\/v\d+\/(?:feed|follow\/feed|nearby\/feed|search\/item|general\/search\/single)\//i.test(url)) {
    filterKnownLists(body);
  }
  if (/\/aweme\/homepage\/render\//i.test(url)) cleanHomepage(body);
  if (options.clean_sidebar && /\/aweme\/homepage\/sidebar_data\//i.test(url)) cleanSidebar(body);
  if (options.clean_tabbar && /\/tfe\/api\/request_combine\/v1\//i.test(url)) cleanSettings(body);
  if (changed) {
    console.log(`[DouyinClean] changed=${changed}`);
    $done({body: JSON.stringify(body)});
  } else $done({});
} catch (error) {
  console.log(`[DouyinClean] skipped: ${error}`);
  $done({});
}
