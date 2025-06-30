# 项目文件结构说明

## 📁 目录结构

```
anime-image-upscaler-api/
├── app/                    # 核心应用代码
│   ├── api/               # API路由
│   ├── core/              # 核心功能模块
│   ├── models/            # 数据模型
│   ├── utils/             # 工具函数
│   ├── config.py          # 配置管理
│   └── main.py            # 应用入口
├── docs/                  # 项目文档
│   ├── CONFIG_GUIDE.md    # 配置指南
│   ├── CONTRIBUTING.md    # 贡献指南
│   └── README.md          # 文件结构说明 (本文件)
├── requirements/          # 依赖管理
│   ├── base.txt          # 基础依赖
│   ├── dev.txt           # 开发依赖
│   └── production.txt    # 生产环境依赖
├── scripts/              # 工具脚本
│   ├── config_manager.py # 配置管理工具
│   └── install_dependencies.py # 依赖安装脚本
├── tests/                # 测试文件
├── Real-ESRGAN/          # AI模型子模块
├── uploads/              # 上传文件目录
├── outputs/              # 输出文件目录
├── logs/                 # 日志文件目录
├── config.env            # 环境配置文件
├── requirements.txt      # 依赖快捷方式
├── start_modern.py       # 现代化启动脚本
├── start.sh              # Shell启动脚本
├── README.md             # 项目说明
└── QUICKSTART.md         # 快速开始指南
```

## 🔧 配置管理

### 环境配置
- `config.env` - 主要配置文件
- `app/config.py` - 配置类定义

### 配置工具
```bash
# 查看当前配置
python scripts/config_manager.py show

# 修改配置
python scripts/config_manager.py set PORT 9000

# 验证配置
python scripts/config_manager.py validate
```

## 📦 依赖管理

### 依赖文件层次
- `requirements.txt` - 快捷入口，指向生产环境依赖
- `requirements/production.txt` - 生产环境完整依赖
- `requirements/base.txt` - 基础依赖
- `requirements/dev.txt` - 开发依赖

### 安装依赖
```bash
# 生产环境
pip install -r requirements.txt

# 开发环境
pip install -r requirements/dev.txt
```

## 🚀 启动方式

### 快速启动
```bash
./start.sh quick          # 跳过环境检查
```

### 完整启动
```bash
./start.sh                # 完整检查和启动
python start_modern.py    # 直接启动
```

## 📚 文档位置

- 项目说明: `README.md`
- 快速开始: `QUICKSTART.md`
- 配置指南: `docs/CONFIG_GUIDE.md`
- 贡献指南: `docs/CONTRIBUTING.md`
- 文件结构: `docs/README.md` (本文件) 