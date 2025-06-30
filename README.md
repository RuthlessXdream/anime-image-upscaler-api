# 🎨 现代化动漫图片高清修复API

基于Real-ESRGAN的高性能动漫图片四倍放大和高清修复服务，采用现代化Python架构重构。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-red.svg)](https://pydantic.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

- 🚀 **高性能处理**：基于Real-ESRGAN的AI图片放大，处理速度0.1-0.3秒
- 🏗️ **现代化架构**：企业级Python项目结构，模块化设计
- 🔒 **类型安全**：完整的Pydantic v2数据验证和配置管理
- 📊 **系统监控**：GPU状态、内存使用、任务队列实时监控
- 📚 **自动文档**：FastAPI自动生成的交互式API文档
- 🔧 **灵活配置**：支持环境变量和配置文件
- 🛡️ **错误处理**：完整的异常处理体系
- 🌐 **CORS支持**：跨域资源共享配置

## 🛠️ 技术栈

- **框架**: FastAPI + Uvicorn
- **AI模型**: Real-ESRGAN (RealESRGAN_x4plus_anime_6B)
- **数据验证**: Pydantic v2 + pydantic-settings
- **图像处理**: OpenCV + Pillow
- **深度学习**: PyTorch + TorchVision
- **系统监控**: psutil
- **开发工具**: Black + isort + MyPy + Pytest

## 📦 安装

### 环境要求

- Python 3.8+
- CUDA 11.8+ (推荐使用GPU)
- 8GB+ RAM
- 4GB+ GPU显存 (使用GPU时)

### 快速开始

1. **克隆项目**
```bash
git clone --recursive https://github.com/your-username/anime-image-upscaler-api.git
cd anime-image-upscaler-api
```

2. **安装依赖**
```bash
# 基础依赖
pip install -r requirements/base.txt

# 开发依赖 (可选)
pip install -r requirements/dev.txt

# 安装Real-ESRGAN依赖
python install_dependencies.py
```

3. **下载AI模型**
```bash
# 模型会自动下载到 Real-ESRGAN/weights/ 目录
python -c "from scripts.download_models import download_model; download_model()"
```

4. **启动服务**
```bash
# 使用现代化启动脚本
python start_modern.py

# 或使用传统方式
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 🚀 使用指南

### API文档

启动服务后访问：
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### 基本使用

#### 图片放大
```bash
curl -X POST "http://localhost:8001/upscale" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

#### 健康检查
```bash
curl http://localhost:8001/health
```

#### 系统状态
```bash
curl http://localhost:8001/system/status
```

### Python客户端示例

```python
import requests

# 上传图片进行放大
with open("anime.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8001/upscale",
        files={"file": f}
    )
    
result = response.json()
task_id = result["task_id"]

# 下载处理结果
download_response = requests.get(f"http://localhost:8001/download/{task_id}")
with open("upscaled_anime.jpg", "wb") as f:
    f.write(download_response.content)
```

## 📁 项目结构

```
anime-image-upscaler-api/
├── app/                    # 主应用目录
│   ├── __init__.py
│   ├── main.py            # FastAPI应用入口
│   ├── config.py          # Pydantic配置管理
│   ├── models/            # 数据模型
│   │   ├── request.py     # 请求模型
│   │   ├── response.py    # 响应模型
│   │   └── task.py        # 任务状态模型
│   ├── api/v1/            # API路由
│   │   ├── health.py      # 健康检查
│   │   ├── system.py      # 系统状态
│   │   └── upscale.py     # 图片处理
│   ├── core/              # 核心业务逻辑
│   │   └── model_manager.py # AI模型管理
│   └── utils/             # 工具模块
│       └── exceptions.py  # 自定义异常
├── Real-ESRGAN/           # Real-ESRGAN子模块
├── requirements/          # 依赖管理
│   ├── base.txt          # 基础依赖
│   └── dev.txt           # 开发依赖
├── pyproject.toml         # 项目配置
├── start_modern.py        # 现代化启动脚本
└── README.md
```

## ⚙️ 配置

### 环境变量

创建 `.env` 文件：

```env
# 应用配置
APP_NAME=动漫图片高清修复API
APP_VERSION=2.0.0
DEBUG=false

# 服务器配置
HOST=0.0.0.0
PORT=8001
RELOAD=false

# AI模型配置
MODEL_NAME=RealESRGAN_x4plus_anime_6B.pth
MODEL_SCALE=4
USE_HALF_PRECISION=true

# GPU配置
GPU_ID=0
MEMORY_THRESHOLD=0.8

# 文件配置
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=[".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]

# 日志配置
LOG_LEVEL=INFO
```

### 高级配置

所有配置项都支持通过环境变量或配置文件设置，详见 `app/config.py`。

## 📊 性能指标

### 处理速度
- **小图片** (512x512): ~0.1-0.2秒
- **中等图片** (1024x1024): ~0.3-0.5秒
- **大图片** (2048x2048): ~1-2秒

### 系统要求
- **GPU显存**: 4GB+ (推荐8GB+)
- **内存**: 8GB+ (推荐16GB+)
- **存储**: 2GB+ (模型文件约400MB)

## 🔧 开发

### 代码格式化
```bash
# 格式化代码
black app/
isort app/

# 类型检查
mypy app/

# 运行测试
pytest
```

### 开发模式启动
```bash
python start_modern.py
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 🐳 Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements/base.txt
RUN python install_dependencies.py

EXPOSE 8001
CMD ["python", "start_modern.py"]
```

## 🤝 贡献

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 强大的图像超分辨率模型
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [Pydantic](https://pydantic.dev/) - 数据验证和设置管理

## 📞 支持

如果您遇到问题或有建议，请：
- 创建 [Issue](https://github.com/your-username/anime-image-upscaler-api/issues)
- 发送邮件至: your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给它一个星标！ 