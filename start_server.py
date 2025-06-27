#!/usr/bin/env python3
"""
动漫图片高清修复API服务启动脚本
"""

import uvicorn
import socket
from pathlib import Path

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 连接到外部地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    """启动API服务"""
    print("🚀 启动动漫图片高清修复API服务...")
    
    # 获取本机IP
    local_ip = get_local_ip()
    port = 8000
    
    print(f"📍 本地访问: http://localhost:{port}")
    print(f"🌐 局域网访问: http://{local_ip}:{port}")
    print(f"📖 API文档: http://{local_ip}:{port}/docs")
    print(f"🔍 交互式文档: http://{local_ip}:{port}/redoc")
    print("="*60)
    print("⚠️  请确保防火墙允许端口8000的入站连接")
    print("💡 Windows防火墙设置: 控制面板 -> 系统和安全 -> Windows Defender防火墙 -> 高级设置")
    print("="*60)
    
    # 启动服务，绑定所有网络接口
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 绑定所有网络接口，允许外部访问
        port=port,
        reload=True,
        reload_dirs=[str(Path(__file__).parent)]
    )

if __name__ == "__main__":
    main() 