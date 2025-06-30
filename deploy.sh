#!/bin/bash

# 动漫图片高清修复API - 一键部署脚本
# 支持GPU和CPU模式自动选择

set -e

echo "🚀 动漫图片高清修复API - Docker一键部署"
echo "================================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    echo "💡 安装指南: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    echo "💡 安装指南: https://docs.docker.com/compose/install/"
    exit 1
fi

# 检查是否有GPU支持
GPU_AVAILABLE=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        GPU_AVAILABLE=true
        echo "✅ 检测到NVIDIA GPU支持"
        nvidia-smi --query-gpu=name --format=csv,noheader | head -1
    else
        echo "⚠️ 检测到nvidia-smi但GPU不可用"
    fi
else
    echo "ℹ️ 未检测到NVIDIA GPU，将使用CPU模式"
fi

# 检查Docker的GPU支持
if [ "$GPU_AVAILABLE" = true ]; then
    if docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi &> /dev/null; then
        echo "✅ Docker GPU支持正常"
        USE_GPU=true
    else
        echo "⚠️ Docker GPU支持不可用，将使用CPU模式"
        echo "💡 请安装nvidia-docker2: https://github.com/NVIDIA/nvidia-docker"
        USE_GPU=false
    fi
else
    USE_GPU=false
fi

# 选择部署模式
if [ "$USE_GPU" = true ]; then
    echo "🎮 使用GPU模式部署"
    COMPOSE_FILE="docker-compose.yml"
    DOCKERFILE="Dockerfile"
else
    echo "🖥️ 使用CPU模式部署"
    COMPOSE_FILE="docker-compose.cpu.yml"
    DOCKERFILE="Dockerfile.cpu"
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p uploads outputs Real-ESRGAN/weights

# 创建.gitkeep文件
touch uploads/.gitkeep outputs/.gitkeep

# 检查配置文件
if [ ! -f "config.env" ]; then
    echo "⚠️ 配置文件不存在，将使用默认配置"
fi

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose -f "$COMPOSE_FILE" build

echo "🚀 启动服务..."
docker-compose -f "$COMPOSE_FILE" up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "🌐 访问地址:"
    echo "   - API服务: http://localhost:7999"
    echo "   - API文档: http://localhost:7999/docs"
    echo "   - 交互式文档: http://localhost:7999/redoc"
    echo ""
    echo "📋 常用命令:"
    echo "   - 查看日志: docker-compose -f $COMPOSE_FILE logs -f"
    echo "   - 停止服务: docker-compose -f $COMPOSE_FILE down"
    echo "   - 重启服务: docker-compose -f $COMPOSE_FILE restart"
    echo ""
    echo "📁 数据目录:"
    echo "   - 上传目录: ./uploads"
    echo "   - 输出目录: ./outputs"
    echo "   - 模型目录: ./Real-ESRGAN/weights"
else
    echo "❌ 服务启动失败"
    echo "📝 查看日志:"
    docker-compose -f "$COMPOSE_FILE" logs
    exit 1
fi 