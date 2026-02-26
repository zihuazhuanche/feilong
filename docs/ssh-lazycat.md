# SSH 连接懒猫服务器

## 当前配置

```
本机私钥                        懒猫服务器
~/.ssh/id_ed25519_bili   →   ~/.ssh/authorized_keys
（私钥，留在本机）               （存了两个公钥）
```

`~/.ssh/config` 中的别名：

```
Host lazycat
    HostName lazycat1012.heiyu.space
    User root
    IdentityFile ~/.ssh/id_ed25519_bili
```

登录命令：

```bash
ssh lazycat
```

---

## authorized_keys 中的公钥

| 公钥备注 | 对应私钥位置 | 是否在用 |
|----------|------------|---------|
| `claude@bili` | 本机 `~/.ssh/id_ed25519_bili` | ✅ 有效，`add-link.py` 通过此密钥 SSH 进懒猫 |
| `deploy-pipeline` | 未知（不在本机） | ❌ 私钥不在本机，暂时无用 |

> `deploy-pipeline` 公钥若要启用，需要把对应私钥存入 GitHub Actions Secrets，
> 并在 workflow 里配置 `SSH_PRIVATE_KEY`，可实现 CI 直接 SSH 操懒猫。

---

## 懒猫 PocketBase 路径

| 项目 | 路径 |
|------|------|
| 数据库 | `/lzcsys/data/appvar/com.lucasay.pocketbase/pocketbase/pb_data/data.db` |
| Hooks 脚本 | `/lzcsys/data/appvar/com.lucasay.pocketbase/pocketbase/pb_hooks/` |
| API 地址 | `http://lazycat1012.heiyu.space:8090`（端口转发，绕过懒猫登录墙） |
| 后台管理 | `https://pocketbase.lazycat1012.heiyu.space/_/`（需懒猫账号登录） |
