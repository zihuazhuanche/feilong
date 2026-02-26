#!/usr/bin/env python3
"""
add-link: 给 URL，自动抓元信息写入 PocketBase 并触发部署
用法: python3 scripts/add-link.py <url> [article|link]
"""

import sys
import re
import html
import json
import random
import string
import time
import subprocess
import urllib.request
import urllib.error

import os as _os

PB_DB = _os.environ.get("PB_DB", "/lzcsys/data/appvar/com.lucasay.pocketbase/pocketbase/pb_data/data.db")
SSH_HOST = _os.environ.get("SSH_HOST", "lazycat")
GH_TOKEN = _os.environ.get("GH_TOKEN", "")
GH_REPO = _os.environ.get("GH_REPO", "zihuazhuanche/feilong")


def fetch_meta(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read(300_000)
            charset = r.headers.get_content_charset() or "utf-8"
            content = raw.decode(charset, errors="replace")
    except Exception as e:
        print(f"⚠️  抓取失败: {e}")
        return {}, ""

    def og(prop):
        m = re.search(
            rf'<meta[^>]+property=["\']og:{prop}["\'][^>]+content=["\']([^"\']+)["\']',
            content, re.I,
        )
        if not m:
            m = re.search(
                rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:{prop}["\']',
                content, re.I,
            )
        return html.unescape(m.group(1).strip()) if m else ""

    def meta_name(name):
        m = re.search(
            rf'<meta[^>]+name=["\'](?:description)["\'][^>]+content=["\']([^"\']+)["\']',
            content, re.I,
        )
        return html.unescape(m.group(1).strip()) if m else ""

    title = og("title")
    if not title:
        m = re.search(r"<title[^>]*>([^<]+)</title>", content, re.I)
        title = html.unescape(m.group(1).strip()) if m else ""

    desc = og("description") or meta_name("description")
    image = og("image")

    return {"title": title, "description": desc, "image": image}, content


def insert_via_ssh(title, url, link_type, description, image):
    payload = {
        "db": PB_DB,
        "title": title,
        "url": url,
        "type": link_type,
        "description": "<p>" + description + "</p>" if description else "",
        "image": image,
    }
    # 把 Python 脚本通过 stdin 传给 ssh，payload 用 env var
    script = (
        "import sqlite3,random,string,time,json,os\n"
        "p=json.loads(os.environ['PB_PAYLOAD'])\n"
        "conn=sqlite3.connect(p['db'])\n"
        "cur=conn.cursor()\n"
        "rid=''.join(random.choices(string.ascii_lowercase+string.digits,k=15))\n"
        "now=time.strftime('%Y-%m-%d %H:%M:%S.000Z',time.gmtime())\n"
        "cur.execute('INSERT INTO links(id,created,updated,title,url,type,description,image)VALUES(?,?,?,?,?,?,?,?)',"
        "(rid,now,now,p['title'],p['url'],json.dumps([p['type']]),p['description'],p['image']))\n"
        "conn.commit()\n"
        "print('inserted:',rid)\n"
        "conn.close()\n"
    )
    env_val = json.dumps(payload)
    result = subprocess.run(
        ["ssh", SSH_HOST, "python3"],
        input=script,
        capture_output=True, text=True,
        env={**__import__("os").environ, "PB_PAYLOAD": env_val},
    )
    # env var 不会自动透传 ssh，改用 inline export
    if result.returncode != 0:
        # fallback: 用 env 命令传递
        cmd = f"PB_PAYLOAD={json.dumps(env_val)} python3"
        result = subprocess.run(
            ["ssh", SSH_HOST, f"export PB_PAYLOAD={json.dumps(env_val)}; python3"],
            input=script,
            capture_output=True, text=True,
        )
    if result.returncode != 0:
        print("❌ SSH 插入失败:", result.stderr[:500])
        sys.exit(1)
    print("✅", result.stdout.strip())


def trigger_deploy():
    import urllib.request
    data = json.dumps({"ref": "main"}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{GH_REPO}/actions/workflows/deploy.yml/dispatches",
        data=data,
        headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"🚀 部署已触发 (HTTP {r.status})")
    except urllib.error.HTTPError as e:
        print(f"⚠️  部署触发失败: HTTP {e.code}")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/add-link.py <url> [article|link]")
        print("环境变量: GH_TOKEN=<github_pat>  (必填)")
        sys.exit(1)

    if not GH_TOKEN:
        print("❌ 请先设置环境变量: export GH_TOKEN=<your_github_pat>")
        sys.exit(1)

    url = sys.argv[1]
    link_type = sys.argv[2] if len(sys.argv) > 2 else "article"

    print(f"🔍 抓取: {url}")
    meta, _ = fetch_meta(url)

    title = meta.get("title", "")
    desc  = meta.get("description", "")
    image = meta.get("image", "")

    if not title:
        title = input("未能提取标题，请手动输入: ").strip()

    print()
    print(f"📝 标题: {title}")
    print(f"🔗 URL:  {url}")
    print(f"🏷️  类型: {link_type}")
    print(f"🖼️  图片: {image or '（无）'}")
    print(f"📄 描述: {desc[:100]}{'...' if len(desc) > 100 else ''}")
    print()

    confirm = input("确认写入？[Y/n] ").strip() or "Y"
    if confirm.lower() != "y":
        print("已取消")
        return

    insert_via_ssh(title, url, link_type, desc, image)
    trigger_deploy()
    print("🌐 https://www.feilong.eu.org/links  (2-3 分钟后生效)")


if __name__ == "__main__":
    main()
