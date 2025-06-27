# 🎨 动漫图片高清修复API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![CUDA](https://img.shields.io/badge/CUDA-11.0+-red.svg)](https://developer.nvidia.com/cuda-downloads)

基于Real-ESRGAN的高性能动漫图片四倍放大和高清修复API服务，支持GPU加速、并发处理和局域网访问。

## ✨ 主要特性

- 🚀 **高性能AI处理** - 基于Real-ESRGAN_x4plus_anime_6B模型，专门优化动漫图片
- 🔄 **智能并发处理** - 根据GPU显存自动调整并发数，支持批量处理
- 🌐 **局域网访问** - 支持多设备访问，手机、平板、电脑都能使用
- 📊 **实时进度跟踪** - 详细的处理状态和进度显示
- 🛡️ **类型安全** - 使用Pydantic进行强类型验证
- 📖 **自动文档** - 自动生成API文档和交互式界面
- 🔧 **完整工具链** - 测试、监控、批量处理工具一应俱全

## 🎯 性能表现

### RTX 4090 测试数据
- **处理速度**: 最高3.88张/秒（4并发）
- **显存占用**: 4.9GB稳定运行
- **处理能力**: 每小时~13,800张图片
- **GPU温度**: 48°C稳定运行

## 🚀 快速开始

### 📋 系统要求

#### 硬件要求
- **GPU**: NVIDIA显卡（推荐RTX 4090/3080/2080Ti）
- **显存**: 最少4GB，推荐8GB以上
- **内存**: 最少8GB，推荐16GB以上
- **存储**: 至少10GB可用空间

#### 软件要求
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.8+
- **CUDA**: 11.0+

### 🔧 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api
```

#### 2. 设置Python环境
```bash
# 创建conda环境（推荐）
conda create -n anime_upscale python=3.8
conda activate anime_upscale

# 或使用venv
python -m venv anime_upscale
source anime_upscale/bin/activate  # Linux/macOS
# anime_upscale\Scripts\activate  # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 安装Real-ESRGAN
```bash
# 克隆Real-ESRGAN到上级目录
cd ..
git clone https://github.com/xinntao/Real-ESRGAN.git
cd Real-ESRGAN

# 安装Real-ESRGAN依赖
pip install basicsr
pip install facexlib
pip install gfpgan
pip install -r requirements.txt
python setup.py develop
```

#### 5. 下载AI模型
```bash
# 下载动漫专用模型（约18MB）
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P weights/

# Windows用户可手动下载到 Real-ESRGAN/weights/ 目录
```

#### 6. 启动服务
```bash
cd ../animate-photo-upscale-api
python start_server.py
```

### 🌐 配置局域网访问（可选）

#### Windows用户
```bash
# 以管理员身份运行
setup_firewall.bat
```

#### Linux/macOS用户
```bash
# 开放端口8000
sudo ufw allow 8000  # Ubuntu
sudo firewall-cmd --add-port=8000/tcp --permanent  # CentOS
```

## 📱 使用方法

### 🖥️ Web界面访问
- **本地访问**: http://localhost:8000/docs
- **局域网访问**: http://[你的IP]:8000/docs

### 🔌 API调用示例

#### Python
```python
import requests

# 上传图片
with open('anime.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upscale',
        files={'file': f}
    )
task_id = response.json()['task_id']

# 查询状态
status = requests.get(f'http://localhost:8000/status/{task_id}')
print(status.json())

# 下载结果
result = requests.get(f'http://localhost:8000/download/{task_id}')
with open('result.jpg', 'wb') as f:
    f.write(result.content)
```

#### cURL
```bash
# 上传图片
curl -X POST "http://localhost:8000/upscale" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@anime.jpg"

# 查询状态
curl "http://localhost:8000/status/YOUR_TASK_ID"

# 下载结果
curl -O "http://localhost:8000/download/YOUR_TASK_ID"
```

## 🛠️ 工具集合

### 🚀 启动和管理
- `start_server.py` - 启动API服务
- `setup_firewall.bat` - 配置Windows防火墙
- `network_test.py` - 网络连接测试

### 🧪 测试工具
- `test_client.py` - 基础API测试
- `enhanced_test_client.py` - 增强版测试（实时进度）
- `performance_test.py` - 性能测试和并发测试

### 📦 批量处理
- `batch_processor.py` - 批量图片处理（保持目录结构）

## 📊 API接口文档

### 核心接口
| 接口 | 方法 | 描述 |
|-----|------|------|
| `/upscale` | POST | 上传图片进行处理 |
| `/status/{task_id}` | GET | 查询任务状态 |
| `/download/{task_id}` | GET | 下载处理结果 |
| `/health` | GET | 健康检查 |
| `/system` | GET | 系统状态信息 |

### 管理接口
| 接口 | 方法 | 描述 |
|-----|------|------|
| `/tasks` | GET | 列出所有任务 |
| `/task/{task_id}` | DELETE | 删除任务 |

## 🔧 配置和优化

### GPU并发优化
系统会根据GPU显存自动调整并发数：
- **24GB+**: 4个并发任务
- **12GB+**: 3个并发任务  
- **8GB+**: 2个并发任务
- **4GB+**: 1个并发任务

### 自定义配置
```python
# 在main.py中修改
MAX_WORKERS = 2  # 手动设置并发数
```

## 🛠️ 故障排除

<details>
<summary><strong>常见问题解决</strong></summary>

### GPU相关问题
- **CUDA out of memory**: 降低并发数或重启服务
- **模型加载失败**: 检查模型文件路径和权限
- **GPU不可用**: 确认CUDA和PyTorch安装正确

### 网络访问问题
- **局域网无法访问**: 运行`python network_test.py`诊断
- **防火墙阻止**: 运行`setup_firewall.bat`（Windows）
- **端口占用**: 更改端口或关闭占用程序

### 性能问题
- **处理速度慢**: 检查GPU使用率和显存占用
- **内存不足**: 增加系统内存或降低并发数
- **磁盘空间不足**: 清理outputs和uploads目录

</details>

## 🤝 贡献

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 开发重点
- 🔧 性能优化和GPU内存管理
- 🌐 多语言支持
- 📱 Web界面开发
- 🔍 更多图片格式支持

## 📝 更新日志

### v1.1.0 (最新)
- ✅ 新增局域网访问支持
- ✅ 修复Pydantic模型警告
- ✅ 过滤torchvision废弃警告
- ✅ 添加防火墙配置脚本
- ✅ 添加网络连接测试工具
- ✅ 优化启动脚本显示信息

### v1.0.0
- ✅ 基础API服务功能
- ✅ GPU加速处理
- ✅ 并发处理支持
- ✅ 批量处理工具
- ✅ 性能测试工具

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

## 🙏 致谢

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - 提供强大的AI超分辨率算法
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- 所有贡献者和使用者的支持

## 📞 支持

如果您遇到问题或有建议：
1. 查看 [Issues](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues)
2. 创建新的Issue
3. 运行`python network_test.py`进行诊断

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！ 