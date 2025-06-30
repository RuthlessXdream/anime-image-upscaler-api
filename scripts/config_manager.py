#!/usr/bin/env python3
"""
配置管理工具
用于查看、修改和验证配置文件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径 - 修改为支持从scripts目录运行
current_file = Path(__file__).resolve()
if current_file.parent.name == 'scripts':
    # 从scripts目录运行
    project_root = current_file.parent.parent
else:
    # 从项目根目录运行
    project_root = current_file.parent

sys.path.insert(0, str(project_root))

from app.config import settings


def show_current_config():
    """显示当前配置"""
    print("🔧 当前配置信息")
    print("=" * 60)
    
    print("📋 应用配置:")
    print(f"   应用名称: {settings.app_name}")
    print(f"   版本: {settings.app_version}")
    print(f"   调试模式: {settings.debug}")
    
    print("\n🌐 服务器配置:")
    print(f"   主机地址: {settings.host}")
    print(f"   端口: {settings.port}")
    print(f"   自动重载: {settings.reload}")
    
    print("\n🤖 AI模型配置:")
    print(f"   模型名称: {settings.model_name}")
    print(f"   放大倍数: {settings.model_scale}x")
    print(f"   半精度模式: {settings.use_half_precision}")
    print(f"   瓦片大小: {settings.tile_size}")
    print(f"   瓦片填充: {settings.tile_pad}")
    print(f"   预填充: {settings.pre_pad}")
    
    print("\n⚡ 并发配置:")
    print(f"   最大工作进程: {settings.max_workers}")
    print(f"   自动检测工作进程: {settings.auto_detect_workers}")
    
    print("\n🎮 GPU配置:")
    print(f"   GPU设备ID: {settings.gpu_id}")
    print(f"   显存使用阈值: {settings.memory_threshold}")
    
    print("\n⏱️ 任务配置:")
    print(f"   任务超时时间: {settings.task_timeout}秒")
    print(f"   清理间隔: {settings.cleanup_interval}秒")
    print(f"   最大文件大小: {settings.max_file_size / 1024 / 1024:.1f}MB")
    
    print("\n📁 文件配置:")
    print(f"   上传目录: {settings.upload_dir}")
    print(f"   输出目录: {settings.output_dir}")
    print(f"   模型目录: {settings.model_dir}")
    print(f"   支持格式: {', '.join(settings.allowed_extensions)}")
    
    print("\n📝 日志配置:")
    print(f"   日志级别: {settings.log_level}")
    print(f"   日志文件: {settings.log_file or '控制台'}")
    
    print("\n🌍 CORS配置:")
    print(f"   允许的源: {', '.join(settings.cors_origins)}")
    
    print("=" * 60)


def update_config_file(key: str, value: str):
    """更新配置文件中的值"""
    config_file = project_root / "config.env"
    
    if not config_file.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    # 读取现有配置
    lines = []
    with open(config_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找并更新配置项
    key_upper = key.upper()
    updated = False
    
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith('#'):
            if '=' in line:
                config_key = line.split('=')[0].strip()
                if config_key == key_upper:
                    lines[i] = f"{key_upper}={value}\n"
                    updated = True
                    break
    
    if not updated:
        # 如果没找到，添加新配置项
        lines.append(f"\n# 用户添加的配置\n{key_upper}={value}\n")
    
    # 写回文件
    with open(config_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ 配置已更新: {key_upper}={value}")
    return True


def validate_config():
    """验证配置是否有效"""
    print("🔍 验证配置...")
    
    errors = []
    warnings = []
    
    # 检查端口范围
    if not (1 <= settings.port <= 65535):
        errors.append(f"端口号无效: {settings.port} (应在1-65535范围内)")
    
    # 检查模型文件是否存在
    if not settings.model_path.exists():
        warnings.append(f"模型文件不存在: {settings.model_path}")
    
    # 检查目录权限
    try:
        settings.create_directories()
    except Exception as e:
        errors.append(f"无法创建目录: {e}")
    
    # 检查GPU设备
    if settings.gpu_id < 0:
        warnings.append(f"GPU设备ID为负数: {settings.gpu_id}")
    
    # 显示结果
    if errors:
        print("❌ 配置错误:")
        for error in errors:
            print(f"   - {error}")
    
    if warnings:
        print("⚠️ 配置警告:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if not errors and not warnings:
        print("✅ 配置验证通过")
    
    return len(errors) == 0


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("📋 配置管理工具")
        print("用法:")
        print("  python config_manager.py show                    # 显示当前配置")
        print("  python config_manager.py set <key> <value>       # 设置配置项")
        print("  python config_manager.py validate               # 验证配置")
        print()
        print("示例:")
        print("  python config_manager.py show")
        print("  python config_manager.py set PORT 8080")
        print("  python config_manager.py set MODEL_NAME RealESRGAN_x4plus.pth")
        print("  python config_manager.py validate")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_config()
    elif command == "set":
        if len(sys.argv) != 4:
            print("❌ 使用方法: python config_manager.py set <key> <value>")
            return
        key, value = sys.argv[2], sys.argv[3]
        update_config_file(key, value)
    elif command == "validate":
        validate_config()
    else:
        print(f"❌ 未知命令: {command}")
        print("支持的命令: show, set, validate")


if __name__ == "__main__":
    main() 