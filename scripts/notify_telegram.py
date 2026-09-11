"""Announce changed plugins using repository metadata and commit messages."""
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, urlsplit, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def affected_plugins(before, after, repo):
    changed = set(git('diff', '--name-only', before, after).splitlines())
    result = []
    for name in git('ls-tree', '-r', '--name-only', after).splitlines():
        if not name.endswith('.plugin'):
            continue
        content = git('show', f'{after}:{name}')
        dependencies = {name}
        # Track scripts hosted by this repository, including cache-busting URLs.
        for url in re.findall(r'https://raw\.githubusercontent\.com/[^\s"\)]+', content):
            path = unquote(urlsplit(url).path)
            prefix = f'/{repo}/main/'
            if path.startswith(prefix):
                dependencies.add(path[len(prefix):])
        if not dependencies & changed:
            continue
        def meta(key, fallback):
            match = re.search(r'^#!' + key + r'\s*=\s*(.*)$', content, re.M)
            return match.group(1).strip() if match else fallback
        exists = subprocess.run(['git', 'cat-file', '-e', f'{before}:{name}'], capture_output=True).returncode == 0
        notes = git('log', '--format=%s', f'{before}..{after}', '--', *sorted(dependencies))
        result.append((name, meta('name', name), meta('desc', 'Loon 插件'), exists, notes))
    return result


def message(entry, repo, sha):
    name, title, desc, exists, notes = entry
    esc = html.escape
    raw = f'https://raw.githubusercontent.com/{repo}/main/{quote(name)}'
    commit = f'https://github.com/{repo}/commit/{sha}'
    # Bound each section well below Telegram's 4096-character limit.
    return (f'<b>{"🔄 插件更新" if exists else "🆕 新插件上线"}｜{esc(title[:150])}</b>\n\n'
            f'{esc(desc[:700])}\n\n<b>更新内容</b>\n{esc(notes[:1400] or "插件配置或配套脚本已更新，详见提交记录。")}\n\n'
            f'<a href="{esc(raw, quote=True)}">插件订阅地址</a> · '
            f'<a href="{esc(commit, quote=True)}">查看更新详情</a>\n\n@Atlas_Corner')


def send(text, token):
    data = json.dumps({'chat_id': os.environ.get('TELEGRAM_CHAT_ID', '@Atlas_Corner'),
                       'text': text, 'parse_mode': 'HTML',
                       'link_preview_options': {'is_disabled': True}}).encode()
    req = Request(f'https://api.telegram.org/bot{token}/sendMessage', data=data,
                  headers={'Content-Type': 'application/json'})
    try:
        with urlopen(req, timeout=30) as response:
            result = json.load(response)
        if not result.get('ok'):
            raise RuntimeError('Telegram rejected the message')
    except (HTTPError, URLError):
        # Never print an exception URL: the bot token is embedded in it.
        raise RuntimeError('Telegram 发送失败，请检查 Token、频道管理员发消息权限和网络。') from None


def main():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    repo = os.environ['GITHUB_REPOSITORY']
    after = os.environ['GITHUB_SHA']
    if os.environ.get('GITHUB_EVENT_NAME') == 'workflow_dispatch':
        messages = ['✅ Loon 插件通知已连接 @Atlas_Corner。后续仓库 main 分支新增或更新插件时，将自动发布简介、更新内容与订阅链接。']
    else:
        before = event.get('before', '')
        if not before or set(before) == {'0'}:
            before = git('hash-object', '-t', 'tree', '/dev/null')
        messages = [message(entry, repo, after) for entry in affected_plugins(before, after, repo)]
    if not messages:
        print('没有插件或配套脚本变更，无需通知。')
        return
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    if not token:
        raise RuntimeError('缺少 TELEGRAM_BOT_TOKEN：请在仓库 Actions secrets 中添加。')
    for text in messages:
        send(text, token)
    print(f'已发送 {len(messages)} 条频道通知。')


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
