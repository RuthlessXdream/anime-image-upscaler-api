#!/usr/bin/env python3
"""
Real-ESRGAN依赖和模型自动安装脚本
适用于动漫图片高清修复API项目
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 命令执行失败: {cmd}")
            print(f"错误: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ 命令执行异常: {cmd}")
        print(f"错误: {str(e)}")
        return False

def download_file(url, filepath):
    """下载文件"""
    try:
        print(f"📥 下载 {url}")
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ 下载完成: {filepath}")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return False

def main():
    print("🚀 开始安装Real-ESRGAN依赖和模型...")
    print("=" * 50)
    
    # 检查Real-ESRGAN子模块
    real_esrgan_path = Path("Real-ESRGAN")
    if not real_esrgan_path.exists():
        print("❌ Real-ESRGAN子模块不存在，请先运行:")
        print("git submodule update --init --recursive")
        return False
    
    # 安装Real-ESRGAN依赖
    print("\n📦 安装Real-ESRGAN依赖...")
    dependencies = [
        "pip install basicsr",
        "pip install facexlib", 
        "pip install gfpgan",
        "pip install -r requirements.txt"
    ]
    
    for cmd in dependencies:
        print(f"执行: {cmd}")
        if not run_command(cmd, cwd=real_esrgan_path):
            print(f"❌ 依赖安装失败: {cmd}")
            return False
    
    # 安装Real-ESRGAN本体
    print("\n🔧 安装Real-ESRGAN...")
    if not run_command("python setup.py develop", cwd=real_esrgan_path):
        print("❌ Real-ESRGAN安装失败")
        return False
    
    # 创建weights目录
    weights_dir = real_esrgan_path / "weights"
    weights_dir.mkdir(exist_ok=True)
    
    # 下载动漫专用模型
    print("\n🎨 下载动漫专用模型...")
    model_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
    model_path = weights_dir / "RealESRGAN_x4plus_anime_6B.pth"
    
    if model_path.exists():
        print(f"✅ 模型已存在: {model_path}")
    else:
        if not download_file(model_url, model_path):
            print("❌ 模型下载失败")
            return False
    
    # 验证安装
    print("\n🧪 验证安装...")
    test_cmd = "python -c \"import realesrgan; print('Real-ESRGAN导入成功')\""
    if run_command(test_cmd, cwd=real_esrgan_path):
        print("✅ Real-ESRGAN安装验证成功")
    else:
        print("⚠️  Real-ESRGAN导入测试失败，但可能仍然可用")
    
    print("\n🎉 安装完成！")
    print("=" * 50)
    print("现在您可以运行以下命令启动API服务:")
    print("python start_server.py")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1) 