#!/bin/bash

# Docker容器启动脚本
# 处理初始化、模型下载和服务启动

set -e

echo "🐳 启动动漫图片高清修复API Docker容器..."

# 创建必要的目录
mkdir -p /app/uploads /app/outputs /app/Real-ESRGAN/weights

# 设置权限
chmod 755 /app/uploads /app/outputs /app/Real-ESRGAN/weights

# 检查并安装运行时依赖
echo "📦 检查运行时依赖..."
if [ -f "/app/install_runtime_deps.sh" ]; then
    echo "🔧 运行依赖检查脚本..."
    /app/install_runtime_deps.sh
fi

# 检查关键Python包
echo "🐍 验证Python依赖..."
python3 -c "
import sys
missing_packages = []

try:
    import torch
    print('✅ PyTorch:', torch.__version__)
except ImportError:
    missing_packages.append('torch')

try:
    import basicsr
    print('✅ BasicSR:', basicsr.__version__)
except ImportError:
    print('⚠️ BasicSR 未安装，尝试安装...')
    import subprocess
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'basicsr>=1.4.2', '--index-url', 'https://pypi.org/simple'])
        print('✅ BasicSR 安装成功')
    except:
        print('❌ BasicSR 安装失败，可能影响某些功能')

try:
    import realesrgan
    print('✅ Real-ESRGAN 可用')
except ImportError:
    missing_packages.append('realesrgan')

if missing_packages:
    print('❌ 缺少关键依赖:', ', '.join(missing_packages))
    print('💡 尝试重新构建Docker镜像')
else:
    print('✅ 所有关键依赖已就绪')
"

# 检查GPU是否可用
echo "🎮 检查GPU状态..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU 驱动已安装"
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits || echo "⚠️ GPU信息获取失败"
else
    echo "⚠️ 未检测到NVIDIA GPU驱动，将使用CPU模式"
fi

# 检查Python环境
echo "🐍 检查Python环境..."
python3 --version
pip3 list | grep -E "(torch|torchvision|fastapi)" || echo "⚠️ 某些关键依赖可能未正确安装"

# 检查模型文件
echo "🤖 检查AI模型文件..."
MODEL_PATH="/app/Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth"
if [ ! -f "$MODEL_PATH" ]; then
    echo "📥 模型文件不存在，正在下载..."
    cd /app
    python3 scripts/install_dependencies.py || {
        echo "❌ 模型下载失败，请检查网络连接"
        echo "💡 您也可以手动下载模型文件到 Real-ESRGAN/weights/ 目录"
        exit 1
    }
else
    echo "✅ 模型文件已存在: $MODEL_PATH"
    ls -lh "$MODEL_PATH"
fi

# 验证配置文件
echo "⚙️ 验证配置文件..."
if [ -f "/app/config.env" ]; then
    echo "✅ 配置文件存在"
    # 显示关键配置（隐藏敏感信息）
    grep -E "^(APP_NAME|PORT|MODEL_NAME|GPU_ID)" /app/config.env || echo "使用默认配置"
else
    echo "⚠️ 配置文件不存在，使用默认配置"
fi

# 运行配置验证
echo "🔍 运行配置验证..."
python3 config_manager.py validate || echo "⚠️ 配置验证出现警告"

# 等待一下，确保所有初始化完成
sleep 2

echo "🚀 启动服务..."
echo "=" * 60
echo "📍 API服务将在端口 7999 启动"
echo "🌐 访问地址: http://localhost:7999"
echo "📖 API文档: http://localhost:7999/docs"
echo "=" * 60

# 执行传入的命令
exec "$@" 