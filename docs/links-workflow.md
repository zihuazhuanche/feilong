# Links 页面使用指南

## 第一步：设置环境变量（只做一次）

把 GitHub Token 加到 `~/.zshrc`，以后打开终端自动生效：

```bash
echo 'export GH_TOKEN=<你的_GitHub_PAT>' >> ~/.zshrc
source ~/.zshrc
```

---

## 第二步：添加链接

```bash
cd ~/feilong
python3 scripts/add-link.py <url>
```

### 示例

```bash
# 添加一篇文章（默认类型）
python3 scripts/add-link.py https://example.com/some-post

# 指定类型为 link（工具/网站）
python3 scripts/add-link.py https://some-tool.app link

# 不需要确认，直接写入（-y）
python3 scripts/add-link.py https://example.com -y
```

### 脚本会做什么

1. 自动抓取网页的 `og:title`、`og:description`、`og:image`
2. 展示预览，按 **Enter** 确认（或加 `-y` 跳过）
3. 写入懒猫上的 PocketBase 数据库
4. 把最新数据导出为 `src/data/links.json`
5. `git commit` + `git push`，GitHub Actions 自动部署

**2-3 分钟后** [www.feilong.eu.org/links](https://www.feilong.eu.org/links) 即可看到新链接。

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<url>` | 必填，链接地址 | — |
| `article` \| `link` | 类型：文章 / 工具网站 | `article` |
| `-y` / `--yes` | 跳过确认直接写入 | 否 |

---

## 常见问题

**抓取失败怎么办？**
脚本会提示手动输入标题，其余字段留空，后续可在 PocketBase 后台补充。

**PocketBase 后台在哪？**
`https://pocketbase.lazycat1012.heiyu.space/_/`（需先登录懒猫账号）

**链接字段说明：**

| 字段 | 说明 |
|------|------|
| `title` | 标题 |
| `url` | 链接地址 |
| `type` | `article`（文章）或 `link`（网站/工具） |
| `description` | 简介，支持 HTML |
| `image` | 封面图 URL（可留空） |

