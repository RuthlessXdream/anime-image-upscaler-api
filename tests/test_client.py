#!/usr/bin/env python3
"""
API测试客户端
"""

import requests
import time
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_api():
    """测试API功能"""
    print("🧪 开始测试动漫图片高清修复API...")
    
    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"健康检查失败: {e}")
        return
    
    # 2. 测试根路径
    print("\n2. 测试根路径...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"根路径测试失败: {e}")
        return
    
    # 3. 测试图片上传（需要有测试图片）
    test_image_path = Path("../test.jpg")
    if test_image_path.exists():
        print(f"\n3. 测试图片上传: {test_image_path}")
        try:
            with open(test_image_path, "rb") as f:
                files = {"file": ("test.jpg", f, "image/jpeg")}
                response = requests.post(f"{API_BASE_URL}/upscale", files=files)
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
            if response.status_code == 200:
                task_id = result["task_id"]
                print(f"任务ID: {task_id}")
                
                # 4. 轮询任务状态
                print("\n4. 轮询任务状态...")
                while True:
                    status_response = requests.get(f"{API_BASE_URL}/status/{task_id}")
                    status_data = status_response.json()
                    print(f"状态: {status_data['status']}, 进度: {status_data['progress']:.1f}%")
                    
                    if status_data["status"] in ["completed", "failed"]:
                        break
                    
                    time.sleep(2)
                
                # 5. 下载结果
                if status_data["status"] == "completed":
                    print("\n5. 下载处理结果...")
                    download_response = requests.get(f"{API_BASE_URL}/download/{task_id}")
                    if download_response.status_code == 200:
                        output_path = f"test_result_{task_id}.jpg"
                        with open(output_path, "wb") as f:
                            f.write(download_response.content)
                        print(f"结果已保存到: {output_path}")
                    else:
                        print("下载失败")
                
        except Exception as e:
            print(f"图片上传测试失败: {e}")
    else:
        print(f"\n3. 跳过图片上传测试（找不到测试图片: {test_image_path}）")
    
    print("\n✅ 测试完成！")

def upload_image(image_path: str):
    """上传单个图片进行处理"""
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"图片文件不存在: {image_path}")
        return
    
    print(f"📤 上传图片: {image_path}")
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (image_path.name, f, "image/jpeg")}
            response = requests.post(f"{API_BASE_URL}/upscale", files=files)
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ 上传成功，任务ID: {task_id}")
            
            # 轮询状态
            print("⏳ 等待处理完成...")
            while True:
                status_response = requests.get(f"{API_BASE_URL}/status/{task_id}")
                status_data = status_response.json()
                print(f"📊 状态: {status_data['status']}, 进度: {status_data['progress']:.1f}%")
                
                if status_data["status"] == "completed":
                    print("🎉 处理完成！")
                    download_url = f"{API_BASE_URL}/download/{task_id}"
                    print(f"📥 下载链接: {download_url}")
                    break
                elif status_data["status"] == "failed":
                    print(f"❌ 处理失败: {status_data['message']}")
                    break
                
                time.sleep(3)
        else:
            print(f"❌ 上传失败: {response.text}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 如果提供了图片路径参数，直接上传处理
        upload_image(sys.argv[1])
    else:
        # 否则运行完整测试
        test_api() 