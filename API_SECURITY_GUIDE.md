# API和Token安全指南

## 重要原则
- **绝不推送敏感信息**: API密钥、Token、密码等敏感信息绝对不能推送到任何公共仓库
- **GitHub保护**: GitHub会自动检测并阻止包含敏感信息的推送
- **环境变量管理**: 敏感信息应存储在.env文件中，并通过.gitignore排除

## 安全措施

### 1. Git配置
- 确保.env文件在.gitignore中
- 提交前检查是否有敏感信息
- 使用`git diff --cached`检查即将提交的内容

### 2. Token管理
- GitHub Personal Access Token应存储在.env文件中
- 不要在代码中硬编码任何API密钥
- 定期轮换Token

### 3. 推送前检查
```bash
# 检查是否有敏感文件被意外添加
git status

# 检查即将提交的内容
git diff --cached

# 检查敏感信息
git log --oneline --all | grep -i "token\|api\|secret\|key"
```

### 4. 错误处理
如果推送被GitHub阻止：
1. 立即重置包含敏感信息的提交
2. 从.gitignore中排除敏感文件
3. 重新提交不包含敏感信息的代码
4. 将敏感信息存储在安全的位置

## 最佳实践
- 使用环境变量管理敏感信息
- 定期检查仓库安全性
- 遵循最小权限原则分配Token权限
- 及时撤销不再需要的Token

## 联系方式
如有安全问题，立即联系相关负责人并采取补救措施。