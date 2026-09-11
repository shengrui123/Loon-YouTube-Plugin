# Telegram 频道通知

目标频道：https://t.me/Atlas_Corner

## 一次性启用

1. 在 Telegram 的 @BotFather 创建机器人，取得 Bot Token。
2. 将机器人添加为 @Atlas_Corner 的管理员，授予发布消息权限。
3. 在 GitHub 仓库 Settings → Secrets and variables → Actions 添加 `TELEGRAM_BOT_TOKEN`，值为 Token。不要将 Token 写进代码或提交记录。
4. 在 Actions → Telegram plugin updates → Run workflow 手动运行，向频道发送连接测试通知。

Secret 页面：https://github.com/shengrui123/Loon-YouTube-Plugin/settings/secrets/actions

也可在本机终端运行 `gh secret set TELEGRAM_BOT_TOKEN --repo shengrui123/Loon-YouTube-Plugin`，在隐藏输入提示中粘贴 Token。

## 通知规则

- main 分支 push 后对比本次推送前后版本，新增或修改 `.plugin` 时发布通知。
- 插件引用的本仓库 main 分支远程脚本变更，也会通知对应插件；每个插件每次推送一条。
- 简介读取 `#!desc`，标题读取 `#!name`，更新内容读取本次推送中涉及该插件及其脚本的 Git 提交标题。以后请使用具体的中文提交标题，或在发布前整理提交说明。
- 消息包含插件订阅链接与提交详情；没有相关变更时保持安静。
- 删除插件不通知。第三方上游脚本自行更新但本仓库没有提交时，不会触发。
- 手动运行只发送连接测试，不重发全部历史插件。手动重跑已成功的推送工作流会重复通知。
- 发送失败会让 Actions 标记失败；为避免网络结果不确定时重复发布，不自动重试。

测试：`python3 -m unittest discover -s tests -p test_telegram.py`。
