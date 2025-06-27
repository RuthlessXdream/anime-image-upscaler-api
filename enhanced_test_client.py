#!/usr/bin/env python3
"""
增强版API测试客户端 - 支持实时进度显示和系统监控
"""

import requests
import time
import json
from pathlib import Path
from datetime import datetime
import sys

API_BASE_URL = "http://localhost:8000"

def print_separator(title=""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def format_time(seconds):
    """格式化时间显示"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        return f"{seconds//60:.0f}分{seconds%60:.0f}秒"
    else:
        return f"{seconds//3600:.0f}小时{(seconds%3600)//60:.0f}分"

def print_progress_bar(progress, width=50):
    """打印进度条"""
    filled = int(width * progress / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {progress:.1f}%"

def test_system_status():
    """测试系统状态"""
    print_separator("系统状态检查")
    try:
        response = requests.get(f"{API_BASE_URL}/system")
        if response.status_code == 200:
            data = response.json()
            
            print("🖥️  GPU信息:")
            gpu_info = data["gpu_info"]
            if "error" not in gpu_info:
                print(f"   名称: {gpu_info['name']}")
                print(f"   显存: {gpu_info['memory_used']} / {gpu_info['memory_total']} (已用/总计)")
                print(f"   负载: {gpu_info['gpu_load']}")
                print(f"   温度: {gpu_info['temperature']}")
            else:
                print(f"   {gpu_info['error']}")
            
            print("\n💾 内存信息:")
            mem_info = data["memory_info"]
            print(f"   系统内存: {mem_info['used']} / {mem_info['total']} ({mem_info['percent']})")
            
            print(f"\n🔧 并发配置:")
            print(f"   最大并发数: {data['max_concurrent']}")
            print(f"   当前活跃任务: {data['active_tasks']}")
            print(f"   队列长度: {data['queue_length']}")
            
        else:
            print(f"❌ 获取系统状态失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 系统状态检查失败: {e}")

def test_health_check():
    """健康检查"""
    print_separator("健康检查")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务状态: {data['status']}")
            print(f"✅ 模型加载: {'已加载' if data['model_loaded'] else '未加载'}")
            print(f"📊 活跃任务: {data['active_tasks']}")
            print(f"🔧 最大并发: {data['max_concurrent']}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def upload_and_monitor(image_path: str):
    """上传图片并实时监控进度"""
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"❌ 图片文件不存在: {image_path}")
        return None
    
    print_separator(f"处理图片: {image_path.name}")
    
    # 显示文件信息
    file_size = image_path.stat().st_size
    print(f"📁 文件大小: {file_size // 1024}KB")
    
    try:
        # 上传文件
        print("📤 正在上传文件...")
        with open(image_path, "rb") as f:
            files = {"file": (image_path.name, f, "image/jpeg")}
            response = requests.post(f"{API_BASE_URL}/upscale", files=files)
        
        if response.status_code != 200:
            print(f"❌ 上传失败: {response.text}")
            return None
        
        result = response.json()
        task_id = result["task_id"]
        estimated_time = result.get("estimated_time", 0)
        
        print(f"✅ 上传成功!")
        print(f"🆔 任务ID: {task_id}")
        print(f"⏱️  预估时间: {format_time(estimated_time)}")
        
        # 实时监控进度
        print("\n🔄 开始处理...")
        last_step = ""
        start_time = time.time()
        
        while True:
            try:
                status_response = requests.get(f"{API_BASE_URL}/status/{task_id}")
                if status_response.status_code != 200:
                    print(f"❌ 获取状态失败: {status_response.status_code}")
                    break
                
                status_data = status_response.json()
                current_time = time.time()
                elapsed = current_time - start_time
                
                # 清除上一行（如果步骤没变）
                if status_data.get("current_step") == last_step:
                    print("\r", end="")
                else:
                    print()
                    last_step = status_data.get("current_step", "")
                
                # 显示进度信息
                progress = status_data["progress"]
                progress_bar = print_progress_bar(progress)
                current_step = status_data.get("current_step", "处理中")
                processing_time = status_data.get("processing_time", elapsed)
                estimated_remaining = status_data.get("estimated_remaining")
                
                info_line = f"{progress_bar} | {current_step}"
                if processing_time > 0:
                    info_line += f" | 已用时: {format_time(processing_time)}"
                if estimated_remaining is not None and estimated_remaining > 0:
                    info_line += f" | 剩余: {format_time(estimated_remaining)}"
                
                print(info_line, end="", flush=True)
                
                # 检查是否完成
                if status_data["status"] == "completed":
                    print(f"\n\n🎉 处理完成!")
                    print(f"⏱️  总耗时: {format_time(processing_time)}")
                    if "output_size" in status_data:
                        print(f"📁 输出大小: {status_data['output_size']}")
                    if "output_resolution" in status_data:
                        print(f"📐 输出分辨率: {status_data['output_resolution']}")
                    
                    # 下载结果
                    download_url = f"{API_BASE_URL}/download/{task_id}"
                    print(f"📥 下载链接: {download_url}")
                    
                    # 自动下载
                    try:
                        download_response = requests.get(download_url)
                        if download_response.status_code == 200:
                            output_filename = f"result_{image_path.stem}_{task_id[:8]}.jpg"
                            with open(output_filename, "wb") as f:
                                f.write(download_response.content)
                            print(f"💾 结果已保存: {output_filename}")
                        else:
                            print("❌ 自动下载失败")
                    except Exception as e:
                        print(f"❌ 下载错误: {e}")
                    
                    return task_id
                    
                elif status_data["status"] == "failed":
                    print(f"\n\n❌ 处理失败: {status_data['message']}")
                    return None
                
                time.sleep(1)  # 每秒更新一次
                
            except KeyboardInterrupt:
                print(f"\n\n⚠️  用户中断，任务仍在后台运行")
                print(f"🆔 任务ID: {task_id}")
                return task_id
            except Exception as e:
                print(f"\n❌ 监控错误: {e}")
                time.sleep(2)
                continue
                
    except Exception as e:
        print(f"❌ 上传错误: {e}")
        return None

def list_all_tasks():
    """列出所有任务"""
    print_separator("任务列表")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks")
        if response.status_code == 200:
            data = response.json()
            
            print(f"📊 任务统计:")
            print(f"   总任务数: {data['total_tasks']}")
            print(f"   活跃任务: {data['active_tasks']}")
            print(f"   已完成: {data['completed_tasks']}")
            print(f"   失败任务: {data['failed_tasks']}")
            
            if data['tasks']:
                print(f"\n📋 任务详情:")
                for task in data['tasks'][-10:]:  # 显示最近10个任务
                    status_icon = {
                        'pending': '⏳',
                        'processing': '🔄',
                        'completed': '✅',
                        'failed': '❌'
                    }.get(task['status'], '❓')
                    
                    task_id_short = task['task_id'][:8]
                    progress = task.get('progress', 0)
                    current_step = task.get('current_step', '未知')
                    
                    print(f"   {status_icon} {task_id_short} | {progress:5.1f}% | {current_step}")
            else:
                print("\n📋 暂无任务")
                
        else:
            print(f"❌ 获取任务列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取任务列表失败: {e}")

def interactive_menu():
    """交互式菜单"""
    while True:
        print_separator("动漫图片高清修复API - 增强版客户端")
        print("1. 🔍 系统状态检查")
        print("2. ❤️  健康检查")
        print("3. 📤 上传图片处理")
        print("4. 📋 查看任务列表")
        print("5. 🚪 退出")
        
        choice = input("\n请选择操作 (1-5): ").strip()
        
        if choice == "1":
            test_system_status()
        elif choice == "2":
            test_health_check()
        elif choice == "3":
            image_path = input("请输入图片路径: ").strip()
            if image_path:
                upload_and_monitor(image_path)
        elif choice == "4":
            list_all_tasks()
        elif choice == "5":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重试")
        
        input("\n按Enter键继续...")

def main():
    """主函数"""
    print("🚀 动漫图片高清修复API - 增强版测试客户端")
    print(f"📡 API地址: {API_BASE_URL}")
    
    # 检查服务是否可用
    if not test_health_check():
        print("❌ 服务不可用，请检查API服务是否启动")
        return
    
    # 如果提供了命令行参数，直接处理图片
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_system_status()
        upload_and_monitor(image_path)
    else:
        # 否则进入交互模式
        interactive_menu()

if __name__ == "__main__":
    main() 