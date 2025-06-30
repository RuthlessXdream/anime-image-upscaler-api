# 快速开始指南

## 一键启动

```bash
# 克隆项目
git clone --recursive https://github.com/your-repo/anime-image-upscaler-api.git
cd anime-image-upscaler-api

# 一键启动（包含环境检查、依赖安装、模型下载、服务启动）
./start.sh
```

## 分步操作

如果需要分步控制，可以使用以下命令：

```bash
# 1. 检查环境
./start.sh check

# 2. 安装依赖
./start.sh install

# 3. 下载模型
./start.sh models

# 4. 启动服务
./start.sh start
```

## 使用API

服务启动后，访问 http://localhost:8800/docs 查看API文档。

### 上传图片示例

```bash
# 使用curl上传图片
curl -X POST "http://localhost:8800/upscale" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg" \
  -F "scale=4" \
  --output result.jpg
```

### Python客户端示例

```python
import requests

with open('input.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8800/upscale',
        files={'file': f},
        data={'scale': 4}
    )

if response.status_code == 200:
    with open('output.jpg', 'wb') as f:
        f.write(response.content)
    print("处理完成！")
```

## 配置调整

编辑 `config.env` 文件来调整配置：

```env
# 修改端口
PORT=9000

# 调整GPU设备
GPU_ID=0

# 调整并发数
MAX_WORKERS=1
```

## 故障排除

1. **端口被占用**: 修改 `config.env` 中的 `PORT`
2. **GPU内存不足**: 减少 `MAX_WORKERS` 数量
3. **模型下载失败**: 手动下载模型文件到 `Real-ESRGAN/weights/` 目录

更多详细信息请查看 [README.md](README.md)。 