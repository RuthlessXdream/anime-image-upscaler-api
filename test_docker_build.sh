#!/bin/bash

# Docker构建测试脚本
# 测试不同Dockerfile的构建时间和镜像大小

echo "🚀 开始测试Docker构建..."

# 清理旧镜像
echo "清理旧镜像..."
docker rmi anime-upscaler-api:python-gpu 2>/dev/null || true
docker rmi anime-upscaler-api:cuda-alternative 2>/dev/null || true

# 测试轻量级Python版本
echo ""
echo "📦 测试1: 轻量级Python版本 (Dockerfile.python-gpu)"
echo "基础镜像: python:3.10-slim"
echo "预估大小: ~2GB"
echo "----------------------------------------"
start_time=$(date +%s)
docker build -f Dockerfile.python-gpu -t anime-upscaler-api:python-gpu . 2>&1 | tee build_python.log
end_time=$(date +%s)
python_build_time=$((end_time - start_time))

# 测试CUDA备用版本
echo ""
echo "📦 测试2: CUDA备用版本 (Dockerfile.gpu-alternative)"
echo "基础镜像: nvidia/cuda:11.8-runtime-ubuntu22.04"
echo "预估大小: ~6GB"
echo "----------------------------------------"
start_time=$(date +%s)
docker build -f Dockerfile.gpu-alternative -t anime-upscaler-api:cuda-alternative . 2>&1 | tee build_cuda.log
end_time=$(date +%s)
cuda_build_time=$((end_time - start_time))

# 显示结果
echo ""
echo "📊 构建结果对比:"
echo "=============================================="
printf "%-20s %-15s %-15s\n" "版本" "构建时间" "镜像大小"
echo "----------------------------------------------"

# 获取镜像大小
python_size=$(docker images anime-upscaler-api:python-gpu --format "{{.Size}}" 2>/dev/null || echo "构建失败")
cuda_size=$(docker images anime-upscaler-api:cuda-alternative --format "{{.Size}}" 2>/dev/null || echo "构建失败")

printf "%-20s %-15s %-15s\n" "Python轻量级" "${python_build_time}秒" "$python_size"
printf "%-20s %-15s %-15s\n" "CUDA备用版" "${cuda_build_time}秒" "$cuda_size"

echo ""
echo "🎯 推荐使用: Python轻量级版本"
echo "原因: 镜像更小，构建更快，网络友好"

# 测试运行
echo ""
echo "🧪 测试运行Python轻量级版本..."
if docker run --rm -d --name test-python-gpu -p 3006:3005 anime-upscaler-api:python-gpu; then
    sleep 10
    if curl -s http://localhost:3006/health > /dev/null; then
        echo "✅ Python轻量级版本运行正常"
    else
        echo "❌ Python轻量级版本运行异常"
    fi
    docker stop test-python-gpu 2>/dev/null || true
else
    echo "❌ Python轻量级版本启动失败"
fi

echo ""
echo "🎉 测试完成！"
echo "使用以下命令启动服务:"
echo "docker-compose -f docker-compose.python-gpu.yml up -d" 