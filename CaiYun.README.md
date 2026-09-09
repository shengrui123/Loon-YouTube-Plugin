# 彩云天气 Loon 插件

文件：`CaiYun.Clean.Loon.plugin`，要求 Loon 3.5.1（983）或更新版本。

## 安装

1. 将插件文件传到 iPhone，在 Loon 的插件管理中导入；如果该版本只支持 URL 导入，请先将文件放到你自己的可访问 HTTPS 地址，再添加该地址。
2. 开启插件、复写、脚本和 MitM，安装并在 iOS 设置中完全信任 Loon CA 证书。
3. 停用重复的彩云天气规则，彻底退出彩云天气后重新打开。
4. 首次使用需要能够下载 GitHub raw 上的原作者脚本。

## 功能与限制

- 按原规则转换了 11 条响应脚本规则和 1 条广告拒绝规则，补充会员接口域名 `biz.cyapi.cn` 的 MitM。
- AI：原脚本在 activity 请求包含 `type_id=A03` 时下发 `aichat` 标签关闭配置。这不代表关闭所有 AI 功能；新版 Pro 是否沿用该接口需实机验证。
- 广告：保留原作者的活动、首页推广、消息推广、发现页过滤及通用广告处理。原脚本仍保留部分天气文章横幅和驾驶天气入口，并非完全清空发现页。
- SVIP：保留原作者的本地会员响应伪装。作者限定已登录、旧版 ≤ 7.20.2；不产生真实订阅，也不能保证服务端付费功能可用。原脚本的常规 user 分支仅识别 `/v2/user`，其他版本接口不能据此认为有效。
- 原脚本缺少异常保护，接口结构变化可能导致脚本报错。出现异常时可停用插件恢复。
- 未在 iPhone / 彩云天气 Pro 实机验证。已核对规则数量、域名覆盖及 Loon 文档语法。

## 来源

- 原规则：https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/CaiYunAds.conf
- 原脚本：https://raw.githubusercontent.com/ddgksf2013/Scripts/refs/heads/master/caiyun_json.js
- Loon 语法：https://nsloon.app/docs/Script/script_v2/

原作者：ddgksf2013。插件直接引用上游远程脚本，后续更新会改变运行逻辑。

## Stash 规则补充（2026-09-09）

参考用户提供的 https://clashios.app/static/stoverride/chxm1023_rewrite/caiyun.stoverride ，增加 `biz.cyapi.cn` / `biz.caiyunapp.com` 的 `/p/v数字/vip_info` 响应处理，仅调整响应中已存在的 VIP / SVIP 对象的到期字段。该逻辑在插件内使用 JQ 实现，不引入第二份远程脚本。

该 Stash 引用的 chxm1023 脚本标注支持 7.11.0（2024-02-07），并非新版 Pro 兼容证明。未采用其增加 AI 配额、插入频道入口、修改注册天数或硬编码设备令牌的行为。地图和 48 小时预报的请求认证未改动，不能承诺解锁。此补充仍需实机验证。
