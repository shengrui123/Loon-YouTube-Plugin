# 抖音去开屏广告

插件文件：[Douyin.Splash.Loon.plugin](./Douyin.Splash.Loon.plugin)

## 功能

- 拦截抖音 `/aweme/v*/splash/`、`/aweme/v*/ad/` 开屏配置。
- 拦截 `/luna/launch` 与 `/luna/advert` 启动广告。
- 拦截已知开屏服务器的 6443 直连请求。
- 不修改首页频道、侧栏、底栏、信息流、评论或账号数据。

## 安装

在 Loon 的“配置 → 插件”中添加：

```text
https://raw.githubusercontent.com/shengrui123/Loon-YouTube-Plugin/main/Douyin.Splash.Loon.plugin
```

先删除旧的“抖音去广告与 TikTok 风格净化”插件，再使用上面的新地址添加。安装并信任 MitM 证书，开启“复写”和“MitM”。随后完全退出抖音、清除抖音缓存，再冷启动；已经下载到本地的开屏素材不会因安装插件自动消失。

## 兼容性

插件使用 Loon 3.5.1 (978) 起的 Rewrite V2 条件语法，无 JavaScript 依赖。规则基于 2026 年公开规则中的开屏路径和直连目标；固定服务器地址发生变化后需要更新。

## 参考

- [Loon 插件官方文档](https://nsloon.app/docs/Plugin/)
- [Loon Rewrite V2 官方文档](https://nsloon.app/docs/Rewrite/rewrite_v2/)
- [BOBOLAOSHIV587/Rules 的 2026 抖音规则](https://github.com/BOBOLAOSHIV587/Rules/blob/main/JS/Douyin_HK/Douyin_HK.plugin)
- [VME98/jinx-rules 的启动广告路径](https://github.com/VME98/jinx-rules)
