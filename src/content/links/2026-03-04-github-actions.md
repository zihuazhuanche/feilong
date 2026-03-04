---
title: "GitHub Actions 自动化部署指南"
url: "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site"
date: 2026-03-04
type: article
---

GitHub Actions 是一个强大的 CI/CD 平台，可以自动构建、测试和部署代码。对于静态网站（如 Astro 生成的博客），可以使用 GitHub Actions 实现自动化部署到 GitHub Pages。

配置时需要注意几点：
1. 工作流文件必须位于 `.github/workflows/` 目录
2. 默认分支（通常是 main）的 push 会自动触发部署
3. 需要设置正确的权限（contents: read, pages: write, id-token: write）

今天通过实际操作，我们发现了一个常见问题：推送时使用了错误的分支（master 而不是 main），导致工作流没有触发。切换到正确的分支后，部署立即成功。
