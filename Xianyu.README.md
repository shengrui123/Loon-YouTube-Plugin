# 闲鱼净化 · Loon

文件：[Xianyu.Clean.Loon.plugin](./Xianyu.Clean.Loon.plugin)。单文件，无远程 JavaScript 依赖。

## 版本与安装

采用截至 2026-09-09 核对的 [Loon 新版 Rewrite 语法](https://nsloon.app/docs/Rewrite/rewrite_v2/)，最低版本为 **3.5.1 (978)**。本插件不使用 Script，所以无需 983 才引入的新版 Script 语法。

1. 将插件导入 Loon 的“配置 → 插件”。远程安装时，需要先将本文件托管到可直接读取内容的 HTTPS 地址，再添加该 URL；此交付没有发布远程地址。
2. 开启“复写”和“MitM”，安装 Loon 生成的 CA 证书，并在 iOS“设置 → 通用 → 关于本机 → 证书信任设置”中启用完全信任。
3. 启用插件，按需调整插件参数，彻底退出闲鱼后重新打开。首次排查时关闭其他匹配闲鱼接口的净化插件。

## 功能

| 开关 | 默认 | 处理范围 |
| --- | --- | --- |
| 屏蔽已知开屏请求 | 开 | 淘宝域名下 `mtop.taobao.idle.home.welcome` |
| 首页仅保留商品类型 | 开 | `home.nextfresh` 的 `data.sections`，保留 `bizType=item` |
| 搜索仅保留商品类型 | 开 | `idlemtopsearch.search` 的 `data.resultList`，保留 `item_type=goods` |
| 隐藏发布浮层 | 关 | 实验性屏蔽 `idle.user.strategy.get`；可能同时影响其他策略入口 |

首页和搜索的处理属于“非商品卡片精简”，不是精确的广告标签识别，也会移除部分正常活动入口；商品类型的广告仍可能保留。缺失类型、空类型或类型异常的卡片保留。只有实际删掉首页卡片且原 feedsCount 为数字时才同步数量，不修改搜索分页和总数。

未加入底栏、直播、热搜等缺少可靠响应样本的修改。不拦截整个淘宝或闲鱼域名，不修改登录、聊天、订单、支付接口。1.2.0 增加优酷共用开屏的精确路径拦截，可独立关闭。

## 验证与限制

本地用 jq 验证过滤逻辑及异常结构，用 URL 正反例检查匹配范围；这不等同于 Loon 原生解析器和闲鱼实机验证。尚无当前闲鱼版本的抓包样本，不能保证全部广告或入口都被移除。

仅处理指定 HTTPS `/gw/` 接口的 JSON 响应；其他域名、接口、JSONP、加密载荷、客户端内置和缓存内容不在覆盖范围。MitM 证书不受 App 接受时不能处理响应。若首页或搜索异常，先关闭对应开关；若发生连接问题，停用插件并检查 MitM 设置。

排查时在 Loon 请求记录中确认接口是否命中、状态是否为 200。后续适配需要 App 版本、实际接口路径及去除 Cookie、Token、用户信息后的响应样本。

## 来源

- [Loon 插件规范](https://nsloon.app/docs/Plugin/) 与 [新版 Rewrite](https://nsloon.app/docs/Rewrite/rewrite_v2/)：配置语法。
- [androidcn/userscripts](https://github.com/androidcn/userscripts/blob/main/goofish.plugin)：首页和搜索端点；同仓库 goofish.js、goofishSearch.js 提供字段路径参考。这里使用自行编写、含结构检查的 JQ 实现。
- [BlueGrave/Surge](https://github.com/BlueGrave/Surge/blob/master/Module/WhiteList.sgmodule)：开屏及发布浮层端点参考。

这些是社区实现资料，并非闲鱼官方稳定 API 承诺。

## 1.1.0：我的页面净化

新增两个默认开启的开关：

- **净化我的页面推广**：处理 `mtop.idle.user.page.my.adapter` 的 `data.container.sections`，移除已知滚动提示、横幅、底部推广模板，并删除用户信息中的 `item.level`。另屏蔽已知 `idle.topic.banner` 横幅请求。
- **隐藏我的工具箱**：移除整个 `my_fy25_tools` 模块，因此同组借钱、小法庭、公约等入口都会隐藏；需要这些入口时关闭此开关。

规则保留未知模板与账号、交易模块，不按全文关键词递归删除。字段依据为 [公开保存的 2024 年实现](https://github.com/zmjde/loon/blob/main/Script/Goofish/Goofish.js) 及 [对应插件](https://github.com/zmjde/loon/blob/main/Plugin/Goofish.plugin)，不是当前闲鱼版本的响应样本。

截图中会员 X7、鱼小铺、回收、游戏签到和猜你喜欢可能使用新的模板，**本次不能保证全部隐藏**。若更新插件并重启 App 后仍显示，请提供打开“我的”时该接口的脱敏 JSON 响应及闲鱼版本，用真实模板继续适配。不要提供 Cookie、Token 或未脱敏的账户数据。

## 1.2.0：修复覆盖缺口（2026-09-11）

前版未覆盖闲鱼 `mtop.*splash.ads`，本版补充该接口，并加入 `iyes.youku.com/uts/v1/start/` 的路径级拦截及 MitM 域名。共用开屏开关默认开启，可能影响其他 App 使用同一路径的开屏；不屏蔽整个优酷域名，也不按尺寸拦截商品图片。

新增默认开启的“按业务类型精简我的页面”：对于有非空字符串 `sectionBizCode` 的模块，仅保留包含 `head`、`user`、`trade` 的模块；缺失或异常编码保持原样。清空已知数组 `data.ability`。这一模式会隐藏其他正常业务入口，可独立关闭。仍无法移除保留模块内部结构未知的会员或营销卡片。

新增“移除我的推荐信息流”，清空 `mtop.taobao.idle.item.buy.feeds` 的 `data.sections` 数组。接口可能被其他页面复用，复用位置的推荐也会清空。

业务字段及 splash.ads 来源：[ddgksf2013 原始规则](https://github.com/ddgksf2013/Rewrite/blob/master/AdBlock/GoofishAds.conf)，标注 2025-09-06 / V1.0.11；不是 2026 年当前 App 的实机验证。优酷路径参考前述 BlueGrave 社区规则。

### 更新后仍无效果

1. 在 Loon 更新远程插件，打开源码确认版本为 1.2.0，并确认新增开关开启。
2. 确认复写、MitM 和证书信任已开启；彻底退出闲鱼再打开。缓存广告可能仍出现，可使用 App 自带清缓存功能（若提供），无需卸载。
3. 记录一次冷启动及进入“我的”的请求，查找 `splash`、`iyes.youku.com`、`my.adapter`、`buy.feeds`。只有域名、没有 HTTPS 路径时，尚不能确认请求被成功解密。
4. 提供闲鱼与 Loon 版本、相关请求 URL（删除查询参数中的身份信息）、规则命中/错误记录，以及 my.adapter 的脱敏响应 JSON。不要发送 Cookie、Token 或账户数据。通过记录区分下载缓存、未解密、接口变化或字段变化，避免盲目扩大拦截。
