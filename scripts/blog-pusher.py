#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINKS_JSON = REPO_ROOT / 'src' / 'data' / 'links.json'
POSTS_DIR = REPO_ROOT / 'src' / 'content' / 'posts'


def run(cmd, check=True):
    return subprocess.run(cmd, cwd=REPO_ROOT, check=check, text=True)


def fetch_meta(url: str) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        content = r.read(300_000).decode(r.headers.get_content_charset() or 'utf-8', errors='replace')

    def find(pattern: str) -> str:
        m = re.search(pattern, content, re.I | re.S)
        return unescape(m.group(1).strip()) if m else ''

    title = find(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']') or \
            find(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']') or \
            find(r'<title[^>]*>(.*?)</title>')
    description = find(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']') or \
                  find(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:description["\']') or \
                  find(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']')
    image = find(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']') or \
            find(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']')
    return {'title': title, 'description': description, 'image': image}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text or 'post'


def load_links() -> list:
    return json.loads(LINKS_JSON.read_text(encoding='utf-8'))


def save_links(data: list) -> None:
    LINKS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def ensure_link(url: str, title: str, description: str, image: str, link_type: str) -> bool:
    data = load_links()
    for item in data:
        if item.get('url') == url:
            return False
    record = {
        'title': title,
        'url': url,
        'type': [link_type],
        'description': f'<p>{description}</p>' if description else '',
        'image': image or '',
        'created': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.000Z'),
    }
    data.insert(0, record)
    save_links(data)
    return True


def ensure_post(date_str: str, slug: str, title: str, description: str, tags: list[str], url: str) -> Path | None:
    filename = f'{date_str}-{slug}.md'
    path = POSTS_DIR / filename
    if path.exists():
        return None
    frontmatter_tags = ', '.join(tags)
    body = f'''---
title: {title}
date: {date_str}
tags: [{frontmatter_tags}]
description: {description}
---

已收录链接：{url}

本次发布包含：

- 站点链接已加入 links 数据
- 新增一篇记录文章

如需补充说明，可继续编辑本文。
'''
    path.write_text(body, encoding='utf-8')
    return path


def git_has_changes() -> bool:
    res = subprocess.run(['git', 'status', '--porcelain'], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return bool(res.stdout.strip())


def push_with_token(token: str) -> None:
    original = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.strip()
    remote = f'https://x-access-token:{token}@github.com/zihuazhuanche/feilong.git'
    try:
        run(['git', 'remote', 'set-url', 'origin', remote])
        run(['git', 'push', 'origin', 'main'])
    finally:
        run(['git', 'remote', 'set-url', 'origin', original], check=False)


def main():
    parser = argparse.ArgumentParser(description='One-shot link + post publisher for feilong.')
    parser.add_argument('url')
    parser.add_argument('--title')
    parser.add_argument('--description')
    parser.add_argument('--image', default='')
    parser.add_argument('--link-type', default='link', choices=['link', 'article'])
    parser.add_argument('--post-title')
    parser.add_argument('--slug')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--tags', default='链接,站点')
    parser.add_argument('--skip-link', action='store_true')
    parser.add_argument('--skip-post', action='store_true')
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--commit', action='store_true')
    parser.add_argument('--push', action='store_true')
    args = parser.parse_args()

    meta = fetch_meta(args.url)
    title = args.title or meta['title'] or args.url
    description = args.description or meta['description'] or args.url
    image = args.image or meta['image'] or ''
    post_title = args.post_title or f'{title} 链接已收录'
    slug = args.slug or slugify(post_title)
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]

    changed = False

    if not args.skip_link:
        link_added = ensure_link(args.url, title, description, image, args.link_type)
        print(f'link_added={link_added}')
        changed = changed or link_added

    if not args.skip_post:
        post_path = ensure_post(args.date, slug, post_title, description, tags, args.url)
        print(f'post_created={str(post_path) if post_path else False}')
        changed = changed or bool(post_path)

    if args.build:
        run(['npm', 'run', 'build'])
        print('build_ok=true')

    if args.commit and git_has_changes():
        run(['git', 'add', 'src/data/links.json', 'src/content/posts', 'scripts/blog-pusher.py'])
        run(['git', 'commit', '-m', f'content: publish {title[:40]}'])
        print('commit_ok=true')
    elif args.commit:
        print('commit_ok=false')

    if args.push:
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if not token:
            print('push_ok=false')
            print('reason=missing GITHUB_TOKEN/GH_TOKEN')
            sys.exit(2)
        push_with_token(token)
        print('push_ok=true')

    if not changed:
        print('changed=false')


if __name__ == '__main__':
    main()
