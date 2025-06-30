# 🎨 动漫图像高清修复API

基于Real-ESRGAN的高性能动漫图像4x放大和高清修复服务，采用现代化Python架构和Docker容器化部署。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-支持-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

- 🚀 **AI图像放大**：基于Real-ESRGAN的动漫图像4x超分辨率处理
- 🐳 **容器化部署**：支持Docker一键启动，GPU/CPU双模式
- 🏗️ **现代化架构**：FastAPI + Pydantic v2，企业级代码结构
- 📊 **实时监控**：GPU状态、内存使用、任务队列监控
- 📚 **自动文档**：Swagger UI交互式API文档
- 🔧 **灵活配置**：统一配置文件管理，支持环境变量
- 🛡️ **健壮性**：完整的异常处理和错误恢复机制
- 🌐 **跨域支持**：CORS配置，支持前端集成

## 🚀 快速开始

### 🐳 Docker一键启动（推荐）

**1. 克隆项目**
```bash
git clone --recursive https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api
```

**2. 配置服务**
```bash
# 编辑配置文件（可选）
cp config.env.example config.env
nano config.env  # 修改端口、模型等配置
```

**3. 一键启动**
```bash
# GPU版本（推荐，需要NVIDIA GPU + CUDA支持）
sudo docker-compose up --build -d

# CPU版本（适用于无GPU环境）
sudo docker-compose -f docker-compose.cpu.yml up --build -d
```

**4. 验证服务**
```bash
# 检查服务状态
curl http://localhost:3005/health

# 访问API文档
# 浏览器打开: http://localhost:3005/docs
```

### 📦 传统安装方式

<details>
<summary>点击展开传统安装步骤</summary>

#### 环境要求
- Python 3.8+
- CUDA 11.8+ (GPU版本)
- 8GB+ RAM
- 4GB+ GPU显存 (GPU版本)

#### 安装步骤
```bash
# 1. 克隆项目
git clone --recursive https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python start_modern.py
```
</details>

## 🛠️ 配置说明

### 主要配置项

编辑 `config.env` 文件：

```env
# 服务器配置
HOST=0.0.0.0
PORT=3005                    # 服务端口
DEBUG=false

# AI模型配置
MODEL_NAME=RealESRGAN_x4plus_anime_6B.pth
MODEL_SCALE=4                # 放大倍数
USE_HALF_PRECISION=true      # 半精度加速（GPU）

# 性能配置
MAX_WORKERS=2                # 并发处理数
AUTO_DETECT_WORKERS=true     # 自动检测CPU核心数
TASK_TIMEOUT=300            # 任务超时时间（秒）

# 文件配置
MAX_FILE_SIZE=52428800      # 最大文件大小（50MB）
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.bmp,.tiff,.webp
```

### GPU vs CPU 模式选择

| 特性 | GPU模式 | CPU模式 |
|------|---------|---------|
| **性能** | 快速（0.1-0.5秒） | 较慢（2-10秒） |
| **内存需求** | 4GB+ GPU显存 | 8GB+ 系统内存 |
| **适用场景** | 生产环境、高并发 | 开发测试、无GPU环境 |
| **启动命令** | `docker-compose up -d` | `docker-compose -f docker-compose.cpu.yml up -d` |

## 📖 API使用指南

### 接口文档
- **Swagger UI**: http://localhost:3005/docs
- **ReDoc**: http://localhost:3005/redoc
- **健康检查**: http://localhost:3005/health

### 基础API调用

#### 1. 图像放大
```bash
curl -X POST "http://localhost:3005/api/v1/upscale" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@anime.jpg"
```

#### 2. 系统状态
```bash
curl http://localhost:3005/api/v1/system/status
```

#### 3. Python客户端示例
```python
import requests

# 上传并处理图像
def upscale_image(image_path, api_url="http://localhost:3005"):
    with open(image_path, "rb") as f:
        response = requests.post(
            f"{api_url}/api/v1/upscale",
            files={"file": f}
        )
    
    if response.status_code == 200:
        # 直接返回处理后的图像数据
        with open("upscaled_image.jpg", "wb") as f:
            f.write(response.content)
        print("图像处理完成！")
    else:
        print(f"处理失败: {response.json()}")

# 使用示例
upscale_image("input_anime.jpg")
```

## 📁 项目结构

```
anime-image-upscaler-api/
├── 🐳 Docker配置
│   ├── docker-compose.yml         # GPU版本部署
│   ├── docker-compose.cpu.yml     # CPU版本部署
│   ├── Dockerfile                 # GPU镜像构建
│   ├── Dockerfile.cpu            # CPU镜像构建
│   └── docker-entrypoint.sh      # 容器启动脚本
├── 📱 应用核心
│   ├── app/
│   │   ├── main.py               # FastAPI应用入口
│   │   ├── api/v1/               # API路由版本管理
│   │   ├── core/                 # 核心业务逻辑
│   │   ├── models/               # 数据模型定义
│   │   └── utils/                # 工具函数
│   └── Real-ESRGAN/              # AI模型子模块
├── ⚙️ 配置管理
│   ├── config.env                # 主配置文件
│   ├── config_manager.py         # 配置管理器
│   └── requirements.txt          # Python依赖
├── 📂 运行时目录
│   ├── uploads/                  # 上传文件临时存储
│   ├── outputs/                  # 处理结果输出
│   └── Real-ESRGAN/weights/      # AI模型文件
└── 📚 文档脚本
    ├── README.md                 # 项目说明
    ├── DEPLOYMENT.md             # 部署指南
    ├── CONFIG_GUIDE.md           # 配置说明
    └── scripts/                  # 辅助脚本
```

## 🔧 开发与部署

### 开发模式
```bash
# 启动开发服务器（热重载）
python start_modern.py --reload

# 代码格式化
black app/
isort app/

# 类型检查
mypy app/

# 运行测试
pytest tests/
```

### 生产部署
```bash
# 构建并启动生产环境
sudo docker-compose up --build -d

# 查看服务日志
sudo docker-compose logs -f

# 停止服务
sudo docker-compose down

# 更新服务
git pull
sudo docker-compose up --build -d
```

### 性能监控
```bash
# 实时查看系统状态
curl http://localhost:3005/api/v1/system/status | jq

# 容器资源使用情况
docker stats upscale_api-app-1
```

## 📊 性能指标

### 处理速度对比

| 图像尺寸 | GPU模式 | CPU模式 | 内存使用 |
|----------|---------|---------|----------|
| 512×512 | 0.1-0.2s | 2-3s | 2GB |
| 1024×1024 | 0.3-0.5s | 5-8s | 4GB |
| 2048×2048 | 1-2s | 15-25s | 8GB |

### 系统要求

**最低配置**
- CPU: 4核心
- 内存: 8GB RAM
- 存储: 5GB可用空间
- 网络: 100Mbps

**推荐配置**
- CPU: 8核心+
- 内存: 16GB+ RAM
- GPU: 6GB+ VRAM (NVIDIA)
- 存储: 10GB+ SSD
- 网络: 1Gbps

## 🐛 故障排除

### 常见问题

<details>
<summary>Docker启动失败</summary>

```bash
# 检查Docker服务状态
sudo systemctl status docker

# 重启Docker服务
sudo systemctl restart docker

# 清理Docker缓存
sudo docker system prune -a
```
</details>

<details>
<summary>GPU不可用</summary>

```bash
# 检查NVIDIA驱动
nvidia-smi

# 安装NVIDIA Container Toolkit
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```
</details>

<details>
<summary>内存不足</summary>

```bash
# 减少并发处理数
echo "MAX_WORKERS=1" >> config.env

# 启用半精度模式
echo "USE_HALF_PRECISION=true" >> config.env
```
</details>

### 日志查看
```bash
# 查看应用日志
sudo docker-compose logs app

# 实时跟踪日志
sudo docker-compose logs -f app

# 查看系统资源
curl http://localhost:3005/api/v1/system/status
```

## 🤝 贡献指南

1. **Fork项目** - 点击右上角Fork按钮
2. **创建分支** - `git checkout -b feature/amazing-feature`
3. **提交更改** - `git commit -m 'Add amazing feature'`
4. **推送分支** - `git push origin feature/amazing-feature`
5. **创建PR** - 提交Pull Request

### 开发规范
- 遵循PEP 8代码风格
- 添加类型注解
- 编写单元测试
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 强大的图像超分辨率AI模型
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化高性能Web框架
- [Pydantic](https://pydantic.dev/) - 数据验证和配置管理
- [Docker](https://docker.com) - 容器化部署解决方案

## 📞 支持与反馈

- 🐛 **问题报告**: [GitHub Issues](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/RuthlessXdream/anime-image-upscaler-api/discussions)
- 📧 **联系方式**: [创建Issue](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues/new)

---

⭐ **如果这个项目对您有帮助，请给它一个星标！**

🚀 **快速体验**: `git clone --recursive https://github.com/RuthlessXdream/anime-image-upscaler-api.git && cd anime-image-upscaler-api && sudo docker-compose -f docker-compose.cpu.yml up -d` 