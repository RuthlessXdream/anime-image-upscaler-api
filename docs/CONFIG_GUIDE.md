# 🔧 配置管理指南

## 概述

本项目采用现代化的配置管理系统，所有参数都通过配置文件管理，避免硬编码，支持灵活的参数调整。

## 配置文件

### 主配置文件：`config.env`

所有可配置的参数都在这个文件中定义：

```env
# 应用基础配置
APP_NAME=动漫图片高清修复API
APP_VERSION=2.0.0
DEBUG=false

# 服务器配置
HOST=0.0.0.0
PORT=7999
RELOAD=false

# AI模型配置
MODEL_NAME=RealESRGAN_x4plus_anime_6B.pth
MODEL_SCALE=4
USE_HALF_PRECISION=true
TILE_SIZE=0
TILE_PAD=10
PRE_PAD=0

# 并发配置
MAX_WORKERS=2
AUTO_DETECT_WORKERS=true

# GPU配置
GPU_ID=0
MEMORY_THRESHOLD=0.8

# 任务配置
TASK_TIMEOUT=300
CLEANUP_INTERVAL=3600
MAX_FILE_SIZE=52428800

# 支持的文件格式（逗号分隔）
ALLOWED_EXTENSIONS=.jpg,.jpeg,.png,.bmp,.tiff,.webp

# 日志配置
LOG_LEVEL=INFO

# CORS配置（逗号分隔）
CORS_ORIGINS=*

# 文件路径配置
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
MODEL_DIR=Real-ESRGAN/weights
```

## 配置管理工具

### 使用 `config_manager.py`

这是一个强大的配置管理工具，提供以下功能：

#### 1. 查看当前配置

```bash
python config_manager.py show
```

显示所有当前配置项的值，包括：
- 📋 应用配置
- 🌐 服务器配置
- 🤖 AI模型配置
- ⚡ 并发配置
- 🎮 GPU配置
- ⏱️ 任务配置
- 📁 文件配置
- 📝 日志配置
- 🌍 CORS配置

#### 2. 修改配置

```bash
python config_manager.py set <KEY> <VALUE>
```

示例：
```bash
# 修改端口
python config_manager.py set PORT 8080

# 修改模型
python config_manager.py set MODEL_NAME RealESRGAN_x4plus.pth

# 修改最大文件大小（字节）
python config_manager.py set MAX_FILE_SIZE 104857600

# 修改GPU设备
python config_manager.py set GPU_ID 1

# 修改并发工作进程数
python config_manager.py set MAX_WORKERS 4
```

#### 3. 验证配置

```bash
python config_manager.py validate
```

检查配置是否有效，包括：
- 端口范围验证
- 模型文件存在性检查
- 目录权限检查
- GPU设备有效性检查

## 配置项详解

### 🌐 服务器配置

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| HOST | 0.0.0.0 | 服务器绑定地址 |
| PORT | 7999 | 服务器端口 |
| RELOAD | false | 开发模式自动重载 |

### 🤖 AI模型配置

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| MODEL_NAME | RealESRGAN_x4plus_anime_6B.pth | 模型文件名 |
| MODEL_SCALE | 4 | 放大倍数 |
| USE_HALF_PRECISION | true | 使用半精度（节省显存） |
| TILE_SIZE | 0 | 瓦片大小（0=自动） |
| TILE_PAD | 10 | 瓦片填充 |
| PRE_PAD | 0 | 预填充 |

### ⚡ 并发配置

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| MAX_WORKERS | 2 | 最大并发工作进程 |
| AUTO_DETECT_WORKERS | true | 自动检测最优进程数 |

### 🎮 GPU配置

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| GPU_ID | 0 | GPU设备ID |
| MEMORY_THRESHOLD | 0.8 | 显存使用阈值 |

### ⏱️ 任务配置

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| TASK_TIMEOUT | 300 | 任务超时时间（秒） |
| CLEANUP_INTERVAL | 3600 | 清理间隔（秒） |
| MAX_FILE_SIZE | 52428800 | 最大文件大小（字节，50MB） |

## 最佳实践

### 1. 生产环境配置

```bash
# 关闭调试模式
python config_manager.py set DEBUG false

# 设置合适的并发数
python config_manager.py set MAX_WORKERS 4

# 设置日志级别
python config_manager.py set LOG_LEVEL WARNING
```

### 2. 开发环境配置

```bash
# 开启调试模式
python config_manager.py set DEBUG true

# 开启自动重载
python config_manager.py set RELOAD true

# 设置详细日志
python config_manager.py set LOG_LEVEL DEBUG
```

### 3. 高性能配置

```bash
# 增加并发数
python config_manager.py set MAX_WORKERS 8

# 增加最大文件大小
python config_manager.py set MAX_FILE_SIZE 104857600

# 使用半精度模式
python config_manager.py set USE_HALF_PRECISION true
```

## 配置优先级

配置系统按以下优先级读取配置：

1. **环境变量** - 最高优先级
2. **config.env文件** - 中等优先级
3. **代码默认值** - 最低优先级

## 注意事项

1. **重启服务**：修改配置后需要重启服务才能生效
2. **配置验证**：建议修改配置后运行验证命令
3. **备份配置**：重要配置修改前建议备份config.env文件
4. **类型转换**：配置工具会自动处理基本类型转换

## 故障排除

### 配置不生效
- 检查配置文件语法是否正确
- 确认服务已重启
- 运行配置验证命令

### 端口冲突
```bash
# 查看端口占用
netstat -ano | findstr :7999

# 修改端口
python config_manager.py set PORT 8080
```

### 模型加载失败
```bash
# 检查模型文件
python config_manager.py validate

# 重新下载模型
python install_dependencies.py
``` 