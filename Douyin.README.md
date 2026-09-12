# 抖音去广告与 TikTok 风格净化

插件文件：[Douyin.Clean.Loon.plugin](./Douyin.Clean.Loon.plugin)

## 功能

- 拦截已知开屏直连 IP、`/api/ad/`、`/aweme/v*/splash/` 与 `zlink.ugsdk.cn/ad/`。
- 从推荐、关注、附近和搜索响应中删除带明确广告字段的内容。
- 顶部默认只保留“关注”和“推荐”，形成接近 TikTok 的双频道首页；可以选择保留“直播”。
- 清理侧栏“常用功能”、常用小程序和常访问的人。
- 关闭服务端动态底栏皮肤并删除底栏切换配置，使用客户端基础布局。

## 安装

在 Loon 的“配置 → 插件”中添加：

```text
https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Douyin.Clean.Loon.plugin
```

安装并信任 MitM 证书，开启“复写”“脚本”和“MitM”，随后完全退出抖音并重新打开。若旧的开屏或频道配置仍在，清除抖音缓存后再冷启动一次。

## 参数

- “过滤信息流广告”：默认开启，只匹配 `is_ads`、`is_ad`、`ad_info` 或 `raw_ad_data` 等明确字段。
- “精简顶部频道”：默认开启，仅保留关注和推荐。
- “保留直播频道”：默认关闭。
- “净化侧栏”：默认开启。
- “净化底栏样式”：默认开启。

## 兼容性

插件使用 Loon 3.5.1 (983) 起的 Script V2 插件对象参数和 Rewrite V2 条件语法。规则基于 2026 年仍公开使用的 `aweme/homepage/render`、`sidebar_data`、`request_combine` 与 `aweme/v*/feed` 接口；抖音灰度版本可能使用不同主机或响应结构。

网络脚本只能修改服务端下发内容，不能像越狱 Hook 一样隐藏所有客户端写死控件。插件不会修改账号、会员、下载权限或地区。

## 参考

- [Loon Script V2 官方文档](https://nsloon.app/docs/Script/script_v2/)
- [Loon 插件官方文档](https://nsloon.app/docs/Plugin/)
- [BOBOLAOSHIV587/Rules 的 2026 抖音规则](https://github.com/BOBOLAOSHIV587/Rules/blob/main/JS/Douyin_HK/Douyin_HK.plugin)
- [huami1314/DYYY 的当前频道 ID](https://github.com/huami1314/DYYY)
