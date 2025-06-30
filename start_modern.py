#!/usr/bin/env python3
"""
现代化架构的启动脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault("PYTHONPATH", str(project_root))

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    # 使用8001端口避免冲突
    port = 8001
    
    print("🚀 启动现代化动漫图片高清修复API服务...")
    print(f"📍 本地访问: http://localhost:{port}")
    print(f"🌐 局域网访问: http://{settings.host}:{port}")
    print(f"📖 API文档: http://localhost:{port}/docs")
    print(f"🔍 交互式文档: http://localhost:{port}/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        access_log=True
    ) 