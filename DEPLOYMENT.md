# 🚀 部署指南

本指南将帮助您将项目部署到GitHub并设置完整的开发环境。

## 📋 部署前准备

### 1. 创建GitHub仓库
1. 登录GitHub账户
2. 创建新仓库：https://github.com/new
3. 仓库名：`anime-image-upscaler-api`
4. 设置为Public（推荐）或Private
5. **不要**初始化README、.gitignore或LICENSE（我们已经准备好了）

### 2. 配置Git
```bash
# 设置Git用户信息（如果还没设置）
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"

# 配置GitHub凭据（推荐使用Token）
git config --global credential.helper store
```

### 3. 获取GitHub Personal Access Token
1. 访问：https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 选择权限：
   - `repo` (完全控制私有仓库)
   - `workflow` (更新GitHub Actions工作流)
4. 复制生成的Token（只显示一次）

## 🚀 快速部署

### 方法一：使用自动化脚本（推荐）
```bash
# 在项目根目录运行
init_git_repo.bat
```

### 方法二：手动部署
```bash
# 1. 初始化Git仓库
git init

# 2. 添加所有文件
git add .

# 3. 创建初始提交
git commit -m "feat: 初始化动漫图片高清修复API项目"

# 4. 添加远程仓库
git remote add origin https://github.com/RuthlessXdream/anime-image-upscaler-api.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

## 📦 项目结构说明

部署到GitHub的文件结构：
```
anime-image-upscaler-api/
├── .github/                    # GitHub配置
│   ├── ISSUE_TEMPLATE/        # Issue模板
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── .gitignore                 # Git忽略文件
├── LICENSE                    # MIT许可证
├── README.md                  # 项目说明
├── CONTRIBUTING.md            # 贡献指南
├── DEPLOYMENT.md              # 部署指南（本文件）
├── requirements.txt           # Python依赖
├── main.py                    # 主API服务
├── start_server.py           # 启动脚本
├── setup_firewall.bat        # 防火墙配置
├── network_test.py           # 网络测试
├── test_client.py            # 基础测试客户端
├── enhanced_test_client.py   # 增强测试客户端
├── performance_test.py       # 性能测试
├── batch_processor.py        # 批量处理工具
└── init_git_repo.bat        # Git初始化脚本
```

## 🔧 部署后配置

### 1. 设置GitHub Pages（可选）
1. 进入仓库设置：`Settings` -> `Pages`
2. Source选择：`Deploy from a branch`
3. Branch选择：`main` / `(root)`
4. 保存后可通过 `https://ruthlessxdream.github.io/anime-image-upscaler-api/` 访问

### 2. 配置Issue和PR模板
GitHub会自动识别`.github`目录下的模板文件：
- Bug报告模板
- 功能请求模板
- Pull Request模板

### 3. 设置仓库描述和标签
在GitHub仓库页面：
1. 点击右上角的⚙️图标
2. 添加描述：`基于Real-ESRGAN的高性能动漫图片AI放大API服务`
3. 添加标签：`python`, `fastapi`, `real-esrgan`, `ai`, `image-processing`, `gpu`, `anime`, `upscaling`
4. 设置主页：`https://github.com/RuthlessXdream/anime-image-upscaler-api`

## 📈 GitHub功能配置

### 1. 启用Discussions（推荐）
1. 进入仓库设置：`Settings` -> `Features`
2. 勾选`Discussions`
3. 用于社区讨论和问答

### 2. 设置分支保护规则
1. 进入：`Settings` -> `Branches`
2. 添加规则保护`main`分支：
   - Require pull request reviews
   - Require status checks to pass
   - Restrict pushes

### 3. 配置安全设置
1. 进入：`Settings` -> `Security & analysis`
2. 启用：
   - Dependency graph
   - Dependabot alerts
   - Dependabot security updates

## 🔄 持续更新

### 日常开发流程
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 开发和提交
git add .
git commit -m "feat: 添加新功能"

# 4. 推送分支
git push origin feature/new-feature

# 5. 在GitHub创建Pull Request
```

### 版本发布
```bash
# 1. 更新版本号（在main.py中）
# 2. 创建标签
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 3. 在GitHub创建Release
```

## 🛠️ 故障排除

### 常见问题

#### 1. 推送失败：Authentication failed
```bash
# 解决方案：使用Personal Access Token
git remote set-url origin https://[TOKEN]@github.com/RuthlessXdream/anime-image-upscaler-api.git
```

#### 2. 文件过大无法推送
```bash
# 检查大文件
git ls-files -s | sort -k5 -nr | head -10

# 移除大文件
git rm --cached large-file.bin
git commit -m "remove large file"
```

#### 3. .gitignore不生效
```bash
# 清除缓存
git rm -r --cached .
git add .
git commit -m "fix: update .gitignore"
```

## 📞 获得帮助

如果部署过程中遇到问题：
1. 检查GitHub仓库是否已创建
2. 确认Git配置和凭据
3. 查看错误信息并搜索解决方案
4. 在项目Issues中提问

## 🎉 部署完成

部署成功后，您的项目将在以下地址可访问：
- **仓库主页**：https://github.com/RuthlessXdream/anime-image-upscaler-api
- **API文档**：在README中有详细说明
- **Issues**：https://github.com/RuthlessXdream/anime-image-upscaler-api/issues
- **Discussions**：https://github.com/RuthlessXdream/anime-image-upscaler-api/discussions

恭喜！您的动漫图片高清修复API项目现在已经在GitHub上线了！🎊 