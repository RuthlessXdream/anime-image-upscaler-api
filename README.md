# 动漫图片高清修复API

基于Real-ESRGAN的动漫图片超分辨率修复API服务，支持2x/4x高清放大。

## 功能特性

- 🎨 专门针对动漫图片优化的AI超分辨率算法
- 🚀 支持2x和4x放大倍数
- 📱 RESTful API接口，易于集成
- ⚡ GPU加速处理（支持NVIDIA CUDA）
- 📊 实时处理状态监控
- 🔧 灵活的配置管理

## 系统要求

### 硬件要求
- **推荐**: NVIDIA GPU（4GB+ 显存）
- **最低**: CPU处理（速度较慢）
- **内存**: 8GB+ RAM
- **存储**: 5GB+ 可用空间

### 软件要求
- Python 3.8+
- NVIDIA驱动（如使用GPU）
- CUDA 11.0+（如使用GPU）

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone --recursive https://github.com/your-repo/anime-image-upscaler-api.git
cd anime-image-upscaler-api

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装Real-ESRGAN

```bash
cd Real-ESRGAN
pip install -e .
cd ..
```

### 3. 下载模型文件

```bash
# 创建模型目录
mkdir -p Real-ESRGAN/weights

# 下载动漫专用模型（约17MB）
wget -O Real-ESRGAN/weights/RealESRGAN_x4plus_anime_6B.pth \
  https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth
```

### 4. 配置环境

```bash
# 复制配置文件
cp config.env.example config.env

# 编辑配置（可选）
nano config.env
```

### 5. 启动服务

```bash
# 启动API服务
python start_modern.py
```

服务启动后访问：
- **API服务**: http://localhost:8800
- **API文档**: http://localhost:8800/docs
- **健康检查**: http://localhost:8800/health

## 配置说明

主要配置项在 `config.env` 文件中：

```env
# 服务配置
HOST=0.0.0.0
PORT=8800
DEBUG=false

# GPU配置
GPU_ID=0                  # GPU设备ID，-1为CPU模式
MAX_WORKERS=2             # 并发处理数量

# 模型配置
MODEL_NAME=RealESRGAN_x4plus_anime_6B.pth
MODEL_SCALE=4             # 默认放大倍数

# 文件配置
MAX_FILE_SIZE=52428800    # 最大文件大小(字节)
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.bmp,.tiff,.webp
```

## API使用

### 上传图片进行处理

```bash
curl -X POST "http://localhost:8800/upscale" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg" \
  -F "scale=4"
```

### Python客户端示例

```python
import requests

# 上传图片
with open('input.jpg', 'rb') as f:
    files = {'file': f}
    data = {'scale': 4}
    response = requests.post('http://localhost:8800/upscale', 
                           files=files, data=data)

if response.status_code == 200:
    with open('output.jpg', 'wb') as f:
        f.write(response.content)
    print("处理完成！")
```

## 性能优化

### GPU加速
确保正确安装NVIDIA驱动和CUDA：
```bash
# 检查GPU状态
nvidia-smi

# 检查CUDA版本
nvcc --version

# 验证PyTorch GPU支持
python -c "import torch; print(torch.cuda.is_available())"
```

### 内存优化
- 调整 `MAX_WORKERS` 参数控制并发数
- 大图片建议分块处理
- 监控系统内存使用情况

## 故障排除

### 常见问题

1. **模型文件未找到**
   ```
   确保模型文件在 Real-ESRGAN/weights/ 目录下
   ```

2. **GPU内存不足**
   ```
   减少 MAX_WORKERS 数量或使用CPU模式
   ```

3. **依赖安装失败**
   ```
   升级pip: pip install --upgrade pip
   使用国内源: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

4. **端口被占用**
   ```
   修改 config.env 中的 PORT 配置
   ```

### 日志查看

服务运行日志会显示在控制台，包含：
- 请求处理状态
- 错误信息
- 性能统计

## 项目结构

```
anime-image-upscaler-api/
├── app/                    # API应用代码
│   ├── api/               # API路由
│   ├── core/              # 核心配置
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── Real-ESRGAN/           # Real-ESRGAN子模块
├── uploads/               # 上传文件目录
├── outputs/               # 输出文件目录
├── config.env             # 环境配置
├── requirements.txt       # Python依赖
└── start_modern.py        # 启动脚本
```

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

## 贡献

欢迎提交Issue和Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 核心超分辨率算法
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架