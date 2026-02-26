#!/usr/bin/env python3
"""
add-link: 给 URL，自动抓元信息写入 PocketBase 并同步 links.json 触发部署
用法: python3 scripts/add-link.py <url> [article|link] [-y]
"""

import sys, re, html, json, random, string, time, subprocess, os
import urllib.request, urllib.error

PB_DB    = os.environ.get("PB_DB", "/lzcsys/data/appvar/com.lucasay.pocketbase/pocketbase/pb_data/data.db")
SSH_HOST = os.environ.get("SSH_HOST", "lazycat")
GH_TOKEN = os.environ.get("GH_TOKEN", "")
GH_REPO  = os.environ.get("GH_REPO", "zihuazhuanche/feilong")

REPO_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINKS_JSON = os.path.join(REPO_ROOT, "src", "data", "links.json")


def fetch_meta(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read(300_000)
            content = raw.decode(r.headers.get_content_charset() or "utf-8", errors="replace")
    except Exception as e:
        print(f"⚠️  抓取失败: {e}")
        return {}

    def og(prop):
        m = re.search(rf'<meta[^>]+property=["\']og:{prop}["\'][^>]+content=["\']([^"\']+)["\']', content, re.I)
        if not m:
            m = re.search(rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:{prop}["\']', content, re.I)
        return html.unescape(m.group(1).strip()) if m else ""

    title = og("title")
    if not title:
        m = re.search(r"<title[^>]*>([^<]+)</title>", content, re.I)
        title = html.unescape(m.group(1).strip()) if m else ""

    desc = og("description")
    if not desc:
        m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', content, re.I)
        desc = html.unescape(m.group(1).strip()) if m else ""

    return {"title": title, "description": desc, "image": og("image")}


def insert_and_export(title, url, link_type, description, image):
    payload = {
        "db": PB_DB, "title": title, "url": url, "type": link_type,
        "description": "<p>" + description + "</p>" if description else "",
        "image": image,
    }
    script = (
        "import sqlite3,random,string,time,json,os\n"
        "p=json.loads(os.environ['PB_PAYLOAD'])\n"
        "conn=sqlite3.connect(p['db'])\n"
        "conn.row_factory=sqlite3.Row\n"
        "cur=conn.cursor()\n"
        "rid=''.join(random.choices(string.ascii_lowercase+string.digits,k=15))\n"
        "now=time.strftime('%Y-%m-%d %H:%M:%S.000Z',time.gmtime())\n"
        "cur.execute('INSERT INTO links(id,created,updated,title,url,type,description,image)VALUES(?,?,?,?,?,?,?,?)',"
        "(rid,now,now,p['title'],p['url'],json.dumps([p['type']]),p['description'],p['image']))\n"
        "conn.commit()\n"
        "cur.execute('SELECT id,title,url,type,description,image,created FROM links ORDER BY created DESC')\n"
        "rows=[]\n"
        "for r in cur.fetchall():\n"
        "    row=dict(r)\n"
        "    try: row['type']=json.loads(row['type'])\n"
        "    except: row['type']=[row['type']]\n"
        "    rows.append(row)\n"
        "print(json.dumps(rows,ensure_ascii=False))\n"
        "conn.close()\n"
    )
    env_val = json.dumps(payload)
    result = subprocess.run(
        ["ssh", SSH_HOST, f"export PB_PAYLOAD={json.dumps(env_val)}; python3"],
        input=script, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("❌ SSH 失败:", result.stderr[:500])
        sys.exit(1)
    return json.loads(result.stdout.strip())


def save_json(data):
    with open(LINKS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已更新 src/data/links.json（共 {len(data)} 条）")


def git_push(title):
    os.chdir(REPO_ROOT)
    subprocess.run(["git", "add", "src/data/links.json"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode == 0:
        print("ℹ️  无变化，跳过提交")
        return
    subprocess.run(["git", "commit", "-m", f"content: 新增链接「{title[:30]}」"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 已推送，GitHub Actions 自动部署中...")
    print("🌐 https://www.feilong.eu.org/links  (2-3 分钟后生效)")


def tty_input(prompt):
    try:
        with open("/dev/tty") as tty:
            sys.stdout.write(prompt); sys.stdout.flush()
            return tty.readline().strip()
    except Exception:
        return input(prompt).strip()


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/add-link.py <url> [article|link] [-y]")
        sys.exit(1)

    if not GH_TOKEN:
        print("❌ 请先设置: export GH_TOKEN=<your_github_pat>")
        sys.exit(1)

    url = sys.argv[1]
    link_type, auto_yes = "article", False
    for arg in sys.argv[2:]:
        if arg in ("-y", "--yes"):   auto_yes = True
        elif not arg.startswith("-"): link_type = arg

    print(f"🔍 抓取: {url}")
    meta  = fetch_meta(url)
    title = meta.get("title", "")
    desc  = meta.get("description", "")
    image = meta.get("image", "")

    if not title:
        title = tty_input("未能提取标题，请手动输入: ")

    print(f"\n📝 标题: {title}\n🔗 URL:  {url}\n🏷️  类型: {link_type}")
    print(f"🖼️  图片: {image or '（无）'}\n📄 描述: {desc[:100]}{'...' if len(desc)>100 else ''}\n")

    if not auto_yes:
        confirm = tty_input("确认写入？[Y/n] ") or "Y"
        if confirm.lower() != "y":
            print("已取消"); return

    all_links = insert_and_export(title, url, link_type, desc, image)
    print(f"✅ 已插入 PocketBase（共 {len(all_links)} 条）")
    save_json(all_links)
    git_push(title)


if __name__ == "__main__":
    main()
