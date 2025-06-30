# 🐳 Docker 一键部署指南

## 概述

本项目提供完整的Docker部署方案，支持GPU和CPU两种模式，实现真正的一键部署。

## 🚀 快速开始

### 方法一：使用一键部署脚本（推荐）

```bash
# Linux/macOS
chmod +x deploy.sh
./deploy.sh

# Windows (Git Bash)
bash deploy.sh
```

脚本会自动：
- 检测GPU支持情况
- 选择合适的部署模式
- 构建Docker镜像
- 启动服务
- 显示访问地址

### 方法二：手动部署

#### GPU模式部署

```bash
# 构建和启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### CPU模式部署

```bash
# 构建和启动
docker-compose -f docker-compose.cpu.yml up -d

# 查看日志
docker-compose -f docker-compose.cpu.yml logs -f
```

## 📋 系统要求

### 基础要求
- Docker 20.10+
- Docker Compose 2.0+
- 至少4GB可用内存
- 至少10GB可用磁盘空间

### GPU模式额外要求
- NVIDIA GPU (支持CUDA 11.8+)
- NVIDIA Docker Runtime (nvidia-docker2)
- NVIDIA驱动 450.80.02+

## 🔧 配置说明

### 环境变量配置

可以通过以下方式配置：

1. **修改config.env文件**（推荐）
2. **Docker Compose环境变量**
3. **运行时环境变量**

```bash
# 示例：修改端口
docker-compose up -d -e PORT=8080
```

### 主要配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| PORT | 7999 | API服务端口 |
| HOST | 0.0.0.0 | 服务绑定地址 |
| GPU_ID | 0 | GPU设备ID (-1禁用GPU) |
| MAX_WORKERS | 2 | 最大并发数 |
| MAX_FILE_SIZE | 52428800 | 最大文件大小(字节) |

## 📁 数据持久化

项目使用Docker卷来持久化数据：

```
./uploads       -> /app/uploads       # 上传文件
./outputs       -> /app/outputs       # 输出文件  
./Real-ESRGAN/weights -> /app/Real-ESRGAN/weights # 模型文件
./config.env    -> /app/config.env    # 配置文件
```

## 🌐 服务访问

部署成功后，可通过以下地址访问：

- **API服务**: http://localhost:7999
- **API文档**: http://localhost:7999/docs
- **交互式文档**: http://localhost:7999/redoc
- **健康检查**: http://localhost:7999/health

## 📝 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec anime-upscaler-api bash
```

### 镜像管理

```bash
# 重新构建镜像
docker-compose build --no-cache

# 清理未使用的镜像
docker image prune

# 查看镜像大小
docker images | grep anime-upscaler
```

### 数据管理

```bash
# 备份输出文件
tar -czf outputs_backup.tar.gz outputs/

# 清理临时文件
docker-compose exec anime-upscaler-api find /app/uploads -name "*.tmp" -delete
```

## 🔍 故障排除

### 常见问题

#### 1. 端口冲突
```bash
# 查看端口占用
netstat -tulpn | grep 7999

# 修改端口
docker-compose down
# 编辑docker-compose.yml，修改ports配置
docker-compose up -d
```

#### 2. GPU不可用
```bash
# 检查GPU状态
nvidia-smi

# 检查Docker GPU支持
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi

# 使用CPU模式
docker-compose -f docker-compose.cpu.yml up -d
```

#### 3. 内存不足
```bash
# 检查内存使用
docker stats

# 减少并发数
# 修改config.env: MAX_WORKERS=1
```

#### 4. 模型下载失败
```bash
# 手动下载模型
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
     -O Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth

# 重启服务
docker-compose restart
```

### 日志分析

```bash
# 查看详细日志
docker-compose logs -f --tail=100

# 查看特定服务日志
docker-compose logs anime-upscaler-api

# 导出日志
docker-compose logs > debug.log
```

## 🔒 安全配置

### 生产环境建议

1. **修改默认端口**
```yaml
ports:
  - "8080:7999"  # 外部8080，内部7999
```

2. **限制访问来源**
```yaml
environment:
  - CORS_ORIGINS=https://yourdomain.com
```

3. **设置资源限制**
```yaml
deploy:
  resources:
    limits:
      memory: 4G
      cpus: '2.0'
```

4. **使用反向代理**
```nginx
# Nginx配置示例
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:7999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🚀 性能优化

### GPU模式优化

```yaml
# docker-compose.yml
environment:
  - USE_HALF_PRECISION=true
  - TILE_SIZE=512
  - MAX_WORKERS=4
```

### CPU模式优化

```yaml
# docker-compose.cpu.yml  
environment:
  - MAX_WORKERS=2
  - TILE_SIZE=256
```

## 📊 监控和日志

### 健康检查

Docker Compose已配置健康检查：

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:7999/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 日志配置

```yaml
# 添加到docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 🆙 更新升级

```bash
# 拉取最新代码
git pull

# 重新构建和部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 清理旧镜像
docker image prune -f
```

## 💡 开发调试

### 开发模式

```bash
# 使用开发配置
cp config.env config.dev.env
# 修改config.dev.env: DEBUG=true, RELOAD=true

# 挂载代码目录
docker-compose -f docker-compose.dev.yml up -d
```

### 调试容器

```bash
# 进入容器调试
docker-compose exec anime-upscaler-api bash

# 查看Python环境
python3 -c "import torch; print(torch.cuda.is_available())"

# 测试API
curl -X GET http://localhost:7999/health
```

## 📞 技术支持

如果遇到问题，请：

1. 查看日志: `docker-compose logs -f`
2. 检查配置: `python3 config_manager.py validate`
3. 提交Issue时请附带：
   - 系统信息 (`docker version`, `nvidia-smi`)
   - 错误日志
   - 配置文件

---

🎉 **恭喜！您已成功部署动漫图片高清修复API服务！** 