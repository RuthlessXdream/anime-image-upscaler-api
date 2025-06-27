# 贡献指南

感谢您对动漫图片高清修复API项目的关注！我们欢迎所有形式的贡献。

## 🤝 如何贡献

### 报告问题
如果您发现了bug或有功能建议，请：
1. 检查 [Issues](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues) 中是否已有相关问题
2. 如果没有，请创建新的Issue，并提供：
   - 详细的问题描述
   - 重现步骤
   - 预期行为和实际行为
   - 系统环境信息（操作系统、Python版本、GPU型号等）
   - 相关的错误日志

### 提交代码
1. **Fork** 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 **Pull Request**

### 代码规范
- 使用Python PEP 8代码风格
- 为新功能添加适当的注释和文档字符串
- 确保代码通过现有测试
- 为新功能编写测试用例

## 🔧 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/RuthlessXdream/anime-image-upscaler-api.git
cd anime-image-upscaler-api
```

### 2. 设置环境
```bash
# 创建conda环境
conda create -n anime_upscale python=3.8
conda activate anime_upscale

# 安装依赖
pip install -r requirements.txt
```

### 3. 安装Real-ESRGAN
```bash
# 克隆Real-ESRGAN仓库到上级目录
cd ..
git clone https://github.com/xinntao/Real-ESRGAN.git
cd Real-ESRGAN
pip install basicsr
pip install facexlib
pip install gfpgan
pip install -r requirements.txt
python setup.py develop
```

### 4. 下载模型
```bash
# 下载动漫专用模型
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P weights/
```

### 5. 测试安装
```bash
cd ../anime-image-upscaler-api
python start_server.py
```

## 📝 提交信息规范

请使用清晰的提交信息：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat: 添加批量处理进度显示功能
fix: 修复GPU内存泄漏问题
docs: 更新API文档
```

## 🎯 开发重点

我们特别欢迎以下方面的贡献：

### 高优先级
- 🔧 性能优化和GPU内存管理
- 🌐 多语言支持（英文、日文等）
- 📱 Web界面开发
- 🔍 更多图片格式支持
- 🛡️ 安全性增强

### 中优先级
- 📊 更详细的处理统计和监控
- 🎨 图像质量评估功能
- 🔄 断点续传功能
- 📦 Docker化部署
- ☁️ 云服务集成

### 低优先级
- 🎵 音频处理功能
- 🎬 视频处理功能
- 🤖 AI模型切换功能
- 📈 机器学习模型训练工具

## 🧪 测试

在提交PR之前，请确保：
1. 运行基础测试：`python test_client.py`
2. 运行性能测试：`python performance_test.py`
3. 运行网络测试：`python network_test.py`
4. 测试批量处理功能

## 📚 文档

如果您的贡献涉及新功能，请同时更新：
- README.md
- API文档注释
- 示例代码

## 🙋‍♂️ 获得帮助

如果您在贡献过程中遇到问题：
1. 查看现有的 [Issues](https://github.com/RuthlessXdream/anime-image-upscaler-api/issues)
2. 创建新的Issue询问
3. 在PR中详细描述您的问题

## 🎉 贡献者

感谢所有为这个项目做出贡献的开发者！

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT License](LICENSE) 下授权。 