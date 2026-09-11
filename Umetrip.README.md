# 航旅纵横去广告与净化

配套文件：`Umetrip.Clean.Loon.plugin` 和 `Umetrip.Clean.Loon.js`。需要 Loon 3.5.1 (983) 或以上。

## 安装

1. 在 Loon「配置 → 插件」中添加以下订阅地址：
   `https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Umetrip.Clean.Loon.plugin`
2. 插件会自动下载本仓库的配套脚本，无需单独导入 JS；首次安装及更新需能访问 GitHub Raw。
3. 开启脚本、MitM，安装并在系统中信任 Loon 的 MitM 证书。
4. 停用其他航旅纵横净化规则，完全退出航旅纵横后重新打开。已缓存的开屏素材可能需要在 App 内清理缓存后再次启动。

如需完全本地使用，把 JS 导入 Loon 本地脚本目录，并将插件的远程脚本 URL 改为 `Umetrip.Clean.Loon.js`。

## 净化范围

- 采用上游开屏及推广载荷清空逻辑。
- 首页广告卡片、营销礼包和部分推广入口。
- 首页瀑布流特价机票、酒店、租车、权益及攻略推广卡片。
- 行程横幅、历史行程、航班详情和家人守护中的会员推广。
- 我的页面会员卡片、商品及返现推广。

隐藏会员推广不改变服务端权限。算法按已知 RPID 和 Protobuf 字段处理，其余响应放行。未添加整域名拦截；上游列出的 `oss.umetrip.com` 没有对应处理规则，因此未加入 MitM。

## 适配与验证

原配置为 Quantumult X 规则，脚本读取/返回 `bodyBytes`。本版本保存上游算法快照，将输入和输出改为 Loon 的 `Uint8Array body`，并将不修改或异常时的结束调用改为 `$done({})`。配置启用 `requires_body=true` 和 `binary_body_mode=true`，使用新版 `response if … then script(…) with …` 语法。

已通过 JavaScript 语法检查及合成二进制响应测试：载荷替换、RPID 回退读取、未知 RPID、损坏载荷与非二进制输入放行，以及单次完成调用。尚未在 iPhone 的 Loon 和航旅纵横中实测；不保证新版 App 的全部广告均被覆盖。

## 来源

- 原作者：ddgksf2013（墨鱼）。[原规则](https://ddgksf2013.top/rewrite/UmetripAds.conf)，V1.0.1，2026-08-29。
- [原脚本](https://ddgksf2013.top/scripts/umetrip.ads.js)，获取于 2026-09-11。获取时使用 `Quantumult X` User-Agent，普通浏览器请求可能返回导航页。
- [Loon 新版 Script 文档](https://nsloon.app/docs/Script/script_v2/)。
- [Loon Script API](https://nsloon.app/docs/Script/script_api/)。

本版本保留原作者署名和来源。脚本为适配快照，后续上游更新需重新适配，不能直接用原 QX 脚本覆盖。
