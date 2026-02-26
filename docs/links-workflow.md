# Links 页面工作流

## 架构概览

```
你 → add-link.py → PocketBase (懒猫) → GitHub Actions → GitHub Pages
```

- **数据存储**：PocketBase，运行在懒猫微服 (`lazycat1012.heiyu.space:8090`)
- **静态构建**：Astro，build 时从 PocketBase API 拉取数据
- **部署**：GitHub Actions → GitHub Pages (`www.feilong.eu.org/links`)
- **触发方式**：新增链接时 → `add-link.py` 直接触发 workflow dispatch；兜底 cron 每 30 分钟自动 rebuild

---

## 一、添加链接（日常使用）

### 前置：设一次 token（加到 ~/.zshrc 之后就不用再管了）

```bash
echo 'export GH_TOKEN=<你的_GitHub_PAT>' >> ~/.zshrc
source ~/.zshrc
```

### 添加一条链接

```bash
cd ~/feilong
python3 scripts/add-link.py <url> [article|link]
```

**示例：**

```bash
# 添加一篇文章（默认类型就是 article，可省略）
python3 scripts/add-link.py https://example.com/some-article article

# 添加一个网站/工具
python3 scripts/add-link.py https://some-tool.app link
```

**脚本会自动：**
1. 抓取页面的 `og:title`、`og:description`、`og:image`
2. 展示预览，等你按 Enter 确认
3. 写入 PocketBase 数据库
4. 触发 GitHub Actions 重新部署

**2-3 分钟后**访问 [www.feilong.eu.org/links](https://www.feilong.eu.org/links) 即可看到新链接。

---

## 二、直接在 PocketBase 后台操作（备用）

1. 打开 `https://pocketbase.lazycat1012.heiyu.space/_/`（需要懒猫账号登录）
2. 左侧点 `links` 集合 → **New record**
3. 填写字段后 **Save**
4. pb_hooks 会自动触发 GitHub Actions 部署（约 2-3 分钟生效）

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | text | 标题 |
| `url` | url | 链接地址 |
| `type` | select | `article`（文章）或 `link`（网站/工具） |
| `description` | rich editor | 简介，支持 HTML |
| `image` | url | 封面图 URL（可留空） |

---

## 三、基础设施说明

### PocketBase API
- 公开地址：`http://lazycat1012.heiyu.space:8090`（走端口转发绕过懒猫登录墙）
- 后台管理：`https://pocketbase.lazycat1012.heiyu.space/_/`

### SSH 登录懒猫
```bash
ssh lazycat   # 免密，使用 ~/.ssh/id_ed25519_bili
```

### GitHub Actions 手动触发
```bash
curl -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  -d '{"ref":"main"}' \
  https://api.github.com/repos/zihuazhuanche/feilong/actions/workflows/deploy.yml/dispatches
```

### 自动部署触发逻辑
- `pb_hooks/github_deploy.pb.js`：links 集合任意增删改 → 立即触发
- `.github/workflows/deploy.yml` cron：每 30 分钟兜底 rebuild
