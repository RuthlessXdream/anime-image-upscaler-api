@echo off
echo 🚀 初始化Git仓库并推送到GitHub
echo ================================================

:: 检查是否已经是Git仓库
if exist .git (
    echo ⚠️  检测到已存在的Git仓库
    echo 是否要重新初始化？这将删除现有的Git历史记录。
    choice /C YN /M "继续 (Y/N)"
    if errorlevel 2 goto :end
    rmdir /S /Q .git
)

echo.
echo 📦 初始化Git仓库...
git init

echo.
echo 📝 添加文件到暂存区...
git add .

echo.
echo 💾 创建初始提交...
git commit -m "feat: 初始化动漫图片高清修复API项目

✨ 主要功能:
- 基于Real-ESRGAN的AI图片放大
- FastAPI RESTful接口
- GPU加速和智能并发处理
- 局域网访问支持
- 完整的工具链和测试套件
- 批量处理功能

🔧 技术栈:
- Python 3.8+
- FastAPI + Pydantic
- Real-ESRGAN
- CUDA GPU加速
- 异步处理"

echo.
echo 🌐 添加GitHub远程仓库...
git remote add origin https://github.com/RuthlessXdream/anime-image-upscaler-api.git

echo.
echo 📤 推送到GitHub...
git branch -M main
git push -u origin main

if %errorlevel% == 0 (
    echo.
    echo ✅ 成功推送到GitHub！
    echo 🔗 仓库地址: https://github.com/RuthlessXdream/anime-image-upscaler-api
    echo 📖 查看项目: https://github.com/RuthlessXdream/anime-image-upscaler-api/blob/main/README.md
) else (
    echo.
    echo ❌ 推送失败，请检查：
    echo 1. 网络连接是否正常
    echo 2. GitHub仓库是否已创建
    echo 3. Git凭据是否配置正确
    echo.
    echo 💡 手动推送命令：
    echo git remote add origin https://github.com/RuthlessXdream/anime-image-upscaler-api.git
    echo git branch -M main
    echo git push -u origin main
)

:end
echo.
pause 