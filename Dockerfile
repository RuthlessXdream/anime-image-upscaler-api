# GPU版本 Dockerfile - 基于NVIDIA CUDA
# 使用方法：docker build -t anime-upscaler-api .
FROM nvidia/cuda:11.8-runtime-ubuntu22.04

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai \
    PORT=3005

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 创建python3的软链接
RUN ln -sf /usr/bin/python3 /usr/bin/python

# 创建工作目录
WORKDIR /app

# 升级pip
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# 安装PyTorch GPU版本
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 复制并安装Python依赖
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app/

# 创建必要的目录
RUN mkdir -p /app/uploads /app/outputs /app/Real-ESRGAN/weights

# 设置权限
RUN chmod +x /app/docker-entrypoint.sh

# 下载模型文件
RUN python3 scripts/install_dependencies.py || echo "模型下载可能失败，将在运行时重试"

# 暴露端口
EXPOSE 3005

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# 设置启动脚本
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python3", "start_modern.py"] 