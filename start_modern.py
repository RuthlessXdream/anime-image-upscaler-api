#!/usr/bin/env python3
"""
现代化架构的启动脚本
完全基于配置文件驱动，无硬编码参数
"""

import sys
import os
import warnings
from pathlib import Path

# 设置警告过滤器 - 在导入其他模块前设置
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")
warnings.filterwarnings("ignore", message=".*torchvision.transforms.functional_tensor.*")
warnings.filterwarnings("ignore", message=".*deprecated.*", module="torchvision.*")

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault("PYTHONPATH", str(project_root))

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    print("🚀 启动现代化动漫图片高清修复API服务...")
    print(f"📋 配置信息:")
    print(f"   - 应用名称: {settings.app_name}")
    print(f"   - 版本: {settings.app_version}")
    print(f"   - 调试模式: {settings.debug}")
    print(f"   - 服务器地址: {settings.host}")
    print(f"   - 服务器端口: {settings.port}")
    print(f"   - AI模型: {settings.model_name}")
    print(f"   - 放大倍数: {settings.model_scale}x")
    print(f"   - GPU设备: {settings.gpu_id}")
    print(f"   - 最大工作进程: {settings.max_workers}")
    print("=" * 60)
    print(f"📍 本地访问: http://localhost:{settings.port}")
    print(f"🌐 局域网访问: http://{settings.host}:{settings.port}")
    print(f"📖 API文档: http://localhost:{settings.port}/docs")
    print(f"🔍 交互式文档: http://localhost:{settings.port}/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        access_log=True
    ) 