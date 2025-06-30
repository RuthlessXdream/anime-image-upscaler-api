# 🚀 部署指南

完整的动漫图像高清修复API部署指南，包含Docker容器化部署和传统部署方式。

## 📋 部署前准备

### 系统要求

**最低配置**
- CPU: 4核心
- 内存: 8GB RAM
- 存储: 10GB可用空间
- 操作系统: Ubuntu 18.04+, CentOS 7+, Windows 10+

**推荐配置**
- CPU: 8核心+
- 内存: 16GB+ RAM
- GPU: NVIDIA GPU (6GB+ VRAM)
- 存储: 20GB+ SSD
- 操作系统: Ubuntu 20.04+ LTS

### 必需软件

**Docker部署（推荐）**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose git

# CentOS/RHEL
sudo yum install docker docker-compose git
sudo systemctl start docker
sudo systemctl enable docker

# 添加用户到docker组
sudo usermod -aG docker $USER
# 重新登录或执行: newgrp docker
```

**GPU支持（可选但推荐）**
```bash
# 安装NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```

## 🐳 Docker部署（推荐）

### 快速开始

**1. 获取项目代码**
```bash
# 克隆项目（包含子模块）
git clone --recursive https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api

# 如果已克隆但缺少子模块
git submodule update --init --recursive
```

**2. 配置服务**
```bash
# 复制配置文件模板
cp config.env.example config.env

# 编辑配置（可选）
nano config.env
```

**3. 选择部署模式**

**GPU模式（推荐 - 适用于有独立显卡的用户）**

```bash
# 检查GPU可用性
nvidia-smi

# 方法1: 标准GPU版本（CUDA 11.8）
sudo docker-compose up --build -d

# 方法2: 如果CUDA 11.8镜像拉取失败，使用备用GPU版本（CUDA 12.1）
docker build -f Dockerfile.gpu-alternative -t anime-upscaler-api .
docker run -d --gpus all -p 3005:3005 --name anime-upscaler-api anime-upscaler-api

# 查看启动日志
sudo docker-compose logs -f app
```

**CPU模式（适用于无独立显卡的用户）**
```bash
# 适用于无GPU环境或集成显卡
sudo docker-compose -f docker-compose.cpu.yml up --build -d

# 查看启动日志
sudo docker-compose -f docker-compose.cpu.yml logs -f app
```

**⚠️ 重要提醒**: 
- 如果您有独立显卡（GTX/RTX系列），请务必使用GPU版本
- 不要在有GPU的机器上使用CPU版本，这会严重影响性能

**4. 验证部署**
```bash
# 检查服务状态
curl http://localhost:3005/health

# 查看容器状态
docker ps

# 访问API文档
# 浏览器打开: http://localhost:3005/docs
```

### Docker部署管理

**服务管理**
```bash
# 查看服务状态
sudo docker-compose ps

# 停止服务
sudo docker-compose down

# 重启服务
sudo docker-compose restart

# 查看日志
sudo docker-compose logs -f app

# 进入容器调试
sudo docker-compose exec app bash
```

**更新部署**
```bash
# 拉取最新代码
git pull origin main
git submodule update --recursive

# 重新构建并启动
sudo docker-compose down
sudo docker-compose up --build -d
```

**清理资源**
```bash
# 停止并删除容器
sudo docker-compose down -v

# 清理未使用的镜像
sudo docker system prune -a

# 清理所有Docker资源（谨慎使用）
sudo docker system prune -a --volumes
```

## 📦 传统部署方式

<details>
<summary>点击展开传统部署步骤</summary>

### 环境准备

**Python环境**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev python3-pip

# CentOS/RHEL
sudo yum install python38 python38-devel python38-pip

# 创建虚拟环境
python3.8 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

**系统依赖**
```bash
# Ubuntu/Debian
sudo apt install build-essential cmake libopencv-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install cmake opencv-devel
```

### 安装部署

```bash
# 1. 克隆项目
git clone --recursive https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 4. 配置环境
cp config.env.example config.env
# 编辑 config.env 文件

# 5. 启动服务
python start_modern.py
```

### 系统服务配置

**创建systemd服务**
```bash
sudo nano /etc/systemd/system/upscale-api.service
```

```ini
[Unit]
Description=Anime Image Upscaler API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/anime-image-upscaler-api
Environment=PATH=/home/ubuntu/anime-image-upscaler-api/venv/bin
ExecStart=/home/ubuntu/anime-image-upscaler-api/venv/bin/python start_modern.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**启用服务**
```bash
sudo systemctl daemon-reload
sudo systemctl enable upscale-api
sudo systemctl start upscale-api
sudo systemctl status upscale-api
```

</details>

## 🌐 反向代理配置

### Nginx配置

**安装Nginx**
```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

**配置文件**
```bash
sudo nano /etc/nginx/sites-available/upscale-api
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    client_max_body_size 100M;   # 允许大文件上传

    location / {
        proxy_pass http://127.0.0.1:3005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 长连接支持
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
```

**启用配置**
```bash
sudo ln -s /etc/nginx/sites-available/upscale-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL证书配置

**使用Let's Encrypt**
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 生产环境优化

### 性能调优

**Docker资源限制**
```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

**系统参数优化**
```bash
# 增加文件描述符限制
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# 内核参数优化
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 监控配置

**Docker健康检查**
```bash
# 查看容器健康状态
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 监控资源使用
docker stats upscale_api-app-1
```

**日志管理**
```bash
# 配置日志轮转
sudo nano /etc/logrotate.d/upscale-api
```

```
/var/log/upscale-api/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
```

## 🛠️ 故障排除

### 常见问题

**1. Docker镜像拉取失败**

**问题现象**:
- `nvidia/cuda:11.8-devel-ubuntu22.04: not found`
- `failed to resolve source metadata`
- `EOF` 网络连接错误
- `version is obsolete` 警告

**解决方案**:

**方案1: 使用备用Dockerfile**
```bash
# GPU用户 - 使用CUDA 12.1版本（推荐）
docker build -f Dockerfile.gpu-alternative -t anime-upscaler-api .

# 手动运行GPU容器
docker run -d \
  --gpus all \
  --name anime-upscaler-api \
  -p 3005:3005 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/config.env:/app/config.env:ro \
  anime-upscaler-api

# 仅限无GPU用户 - 使用Ubuntu基础镜像
docker build -f Dockerfile.alternative -t anime-upscaler-api .

# 手动运行CPU容器
docker run -d \
  --name anime-upscaler-api \
  -p 3005:3005 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/config.env:/app/config.env:ro \
  anime-upscaler-api
```

**方案2: 配置Docker代理**

*Windows用户*:
```powershell
# 设置环境变量
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"

# 或在Docker Desktop设置中配置代理
# Settings -> Resources -> Proxies
```

*Linux用户*:
```bash
# 创建Docker代理配置目录
sudo mkdir -p /etc/systemd/system/docker.service.d

# 创建代理配置文件
sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7897"
Environment="HTTPS_PROXY=http://127.0.0.1:7897"
Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.somecorporation.com"
EOF

# 重新加载配置并重启Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# 验证配置
sudo systemctl show --property=Environment docker
```

**方案3: 配置Docker镜像加速器**
```bash
# 创建或编辑Docker配置文件
sudo tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://dockerhub.azk8s.cn"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# 重启Docker服务
sudo systemctl restart docker

# 验证配置
docker info | grep -A 10 "Registry Mirrors"
```

**方案4: 手动拉取镜像**
```bash
# 尝试手动拉取基础镜像
docker pull nvidia/cuda:11.8-devel-ubuntu22.04

# 如果失败，使用其他版本
docker pull nvidia/cuda:11.8-runtime-ubuntu22.04
docker pull nvidia/cuda:12.0-devel-ubuntu22.04

# 修改Dockerfile中的FROM行
sed -i 's/nvidia\/cuda:11.8-devel-ubuntu22.04/nvidia\/cuda:11.8-runtime-ubuntu22.04/g' Dockerfile
```

**2. Docker启动失败**
```bash
# 检查Docker服务
sudo systemctl status docker

# 检查端口占用
sudo netstat -tlnp | grep 3005

# 查看详细错误
sudo docker-compose logs app
```

**3. GPU不可用**
```bash
# 检查NVIDIA驱动
nvidia-smi

# 检查Docker GPU支持
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 重启Docker服务
sudo systemctl restart docker
```

**4. 内存不足**
```bash
# 检查系统内存
free -h

# 检查容器内存使用
docker stats

# 调整配置
echo "MAX_WORKERS=1" >> config.env
echo "USE_HALF_PRECISION=true" >> config.env
```

**5. 网络连接问题**
```bash
# 检查防火墙
sudo ufw status
sudo iptables -L

# 开放端口
sudo ufw allow 3005
sudo firewall-cmd --permanent --add-port=3005/tcp
sudo firewall-cmd --reload
```

**6. 版本兼容性问题**

**问题**: Docker Compose版本警告
```
time="2025-06-30T16:48:51+08:00" level=warning msg="version is obsolete"
```

**解决**: 已修复，更新项目即可:
```bash
git pull origin main
```

### 日志分析

**应用日志**
```bash
# Docker日志
sudo docker-compose logs -f app

# 系统服务日志
sudo journalctl -u upscale-api -f

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

**性能监控**
```bash
# 系统资源监控
htop
iotop
nvidia-smi -l 1

# API性能测试
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3005/health
```

## 📊 部署验证

### 功能测试

**基础API测试**
```bash
# 健康检查
curl http://localhost:3005/health

# 系统状态
curl http://localhost:3005/api/v1/system/status

# 图像处理测试
curl -X POST "http://localhost:3005/api/v1/upscale" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg" \
     -o upscaled_result.jpg
```

**压力测试**
```bash
# 安装测试工具
sudo apt install apache2-utils

# 并发测试
ab -n 100 -c 10 http://localhost:3005/health

# 文件上传测试
for i in {1..10}; do
  curl -X POST "http://localhost:3005/api/v1/upscale" \
       -F "file=@test.jpg" \
       -o "result_$i.jpg" &
done
wait
```

## 🎉 部署完成

部署成功后，您的API服务将在以下地址可用：

- **API服务**: http://localhost:3005
- **API文档**: http://localhost:3005/docs
- **健康检查**: http://localhost:3005/health
- **系统状态**: http://localhost:3005/api/v1/system/status

### 后续步骤

1. **域名配置**: 配置DNS解析到服务器IP
2. **SSL证书**: 启用HTTPS加密
3. **监控告警**: 配置服务监控和告警
4. **备份策略**: 设置数据备份计划
5. **更新策略**: 建立版本更新流程

### 获得帮助

如果部署过程中遇到问题：
- 📖 查看 [README.md](README.md) 了解基础使用
- 🔧 查看 [CONFIG_GUIDE.md](CONFIG_GUIDE.md) 了解配置详情
- 🐛 在 [GitHub Issues](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues) 提交问题
- 💬 在 [GitHub Discussions](https://github.com/RuthlessXdream/anime-image-upscaler-api/discussions) 参与讨论 