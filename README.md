# Loon 应用净化插件

## 抖音

- [抖音去广告与 TikTok 风格净化](./Douyin.README.md)：去开屏、过滤信息流广告，首页默认仅保留关注与推荐。

## YouTube 与 YouTube Music

插件文件：[YouTube.Enhance.Loon.plugin](./YouTube.Enhance.Loon.plugin)

## 功能

- 移除 YouTube 视频贴片广告、瀑布流广告、搜索广告及 Shorts 广告。
- 移除 YouTube 底栏 Shorts 与上传按钮。
- 开启 YouTube 画中画、后台播放和字幕翻译。
- 移除 YouTube Music 底栏上传、选段（Samples）与升级入口。
- 开启 YouTube Music 后台播放与双语歌词翻译。

## 安装

1. 将 `YouTube.Enhance.Loon.plugin` 放入 iCloud Drive 的 `Loon/Plugins` 目录，或把它托管到可直接访问的 HTTPS 地址。
2. 在 Loon 中打开“配置 → 插件”，添加该文件或远程 URL。
3. 在 Loon 中安装并信任 MitM 证书，同时开启“复写”“脚本”和“MitM”。
4. 完全退出并重新打开 YouTube 与 YouTube Music。

建议只启用这一份 YouTube 增强插件。Loon 的 Request/Response Script 采用首条匹配机制，其他 YouTube 去广告、字幕或歌词插件可能抢先匹配同一接口。

## 参数

- 字幕与歌词翻译默认使用简体中文/Google，可在插件设置中修改。
- `off` 可关闭 YouTube 字幕翻译。
- 关闭“歌词翻译”开关可完全停用 DualSubs 歌词请求和响应脚本。
- 画中画和后台播放能力由响应脚本注入；仍可在 YouTube App 自身设置中关闭。

## 兼容性与限制

- 需要 Loon `3.5.1 (983)` 或更高版本，使用新版 Script/Rewrite 语法。
- 仅适用于 iOS/iPadOS/macOS；YouTube 接口变化后可能需要更新上游脚本。
- 字幕翻译要求视频本身存在字幕轨道；歌词翻译要求 YouTube Music 提供歌词页面。
- 插件引用的脚本会从 GitHub 下载，因此首次启用或更新时需能访问 GitHub。

## 上游与致谢

- [Maasea/sgmodule](https://github.com/Maasea/sgmodule)：广告净化、界面精简、画中画、后台播放、字幕功能。
- [DualSubs/YouTube](https://github.com/DualSubs/YouTube)：YouTube Music 歌词翻译请求处理。
- [DualSubs/Universal](https://github.com/DualSubs/Universal)：歌词翻译响应处理。
- [Loon 官方文档](https://nsloon.app/docs/Plugin/)：插件、Rewrite 与 Script 语法。

本仓库只包含 Loon 配置，不复制上游脚本。上游代码分别受其各自许可证约束。
