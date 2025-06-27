#!/usr/bin/env python3
"""
性能测试脚本 - 测试并发处理能力
"""

import requests
import time
from pathlib import Path
import concurrent.futures
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

def test_single_upload(image_path, test_id):
    """单个上传测试"""
    start_time = time.time()
    
    try:
        print(f"📤 [{test_id}] 开始上传...")
        
        with open(image_path, "rb") as f:
            files = {"file": (f"test_{test_id}.jpg", f, "image/jpeg")}
            response = requests.post(f"{API_BASE_URL}/upscale", files=files)
        
        if response.status_code != 200:
            print(f"❌ [{test_id}] 上传失败: {response.status_code}")
            return None
        
        result = response.json()
        task_id = result["task_id"]
        upload_time = time.time() - start_time
        
        print(f"✅ [{test_id}] 上传成功 (耗时: {upload_time:.2f}s), 任务ID: {task_id[:8]}")
        
        # 等待处理完成
        while True:
            status_response = requests.get(f"{API_BASE_URL}/status/{task_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    total_time = time.time() - start_time
                    processing_time = status_data.get("processing_time", 0)
                    print(f"🎉 [{test_id}] 处理完成! 总耗时: {total_time:.2f}s, 处理耗时: {processing_time:.2f}s")
                    return {
                        "test_id": test_id,
                        "task_id": task_id,
                        "upload_time": upload_time,
                        "processing_time": processing_time,
                        "total_time": total_time,
                        "status": "success"
                    }
                elif status_data["status"] == "failed":
                    print(f"❌ [{test_id}] 处理失败: {status_data['message']}")
                    return {
                        "test_id": test_id,
                        "task_id": task_id,
                        "status": "failed",
                        "error": status_data['message']
                    }
            
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ [{test_id}] 错误: {e}")
        return {
            "test_id": test_id,
            "status": "error",
            "error": str(e)
        }

def test_concurrent_processing(image_path, num_concurrent=4):
    """测试并发处理"""
    print(f"🚀 开始并发测试，并发数: {num_concurrent}")
    print(f"📁 测试图片: {image_path}")
    
    if not Path(image_path).exists():
        print(f"❌ 图片文件不存在: {image_path}")
        return
    
    # 获取系统状态
    try:
        response = requests.get(f"{API_BASE_URL}/system")
        if response.status_code == 200:
            system_info = response.json()
            print(f"🖥️  GPU: {system_info['gpu_info']['name']}")
            print(f"💾 显存: {system_info['gpu_info']['memory_used']} / {system_info['gpu_info']['memory_total']}")
            print(f"🔧 最大并发: {system_info['max_concurrent']}")
            print("="*60)
    except:
        pass
    
    start_time = time.time()
    
    # 使用线程池并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = []
        for i in range(num_concurrent):
            future = executor.submit(test_single_upload, image_path, i+1)
            futures.append(future)
        
        # 等待所有任务完成
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    total_time = time.time() - start_time
    
    # 统计结果
    print("\n" + "="*60)
    print("📊 测试结果统计")
    print("="*60)
    
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") in ["failed", "error"]]
    
    print(f"✅ 成功任务: {len(successful)}/{num_concurrent}")
    print(f"❌ 失败任务: {len(failed)}/{num_concurrent}")
    print(f"⏱️  总测试时间: {total_time:.2f}秒")
    
    if successful:
        avg_upload_time = sum(r["upload_time"] for r in successful) / len(successful)
        avg_processing_time = sum(r["processing_time"] for r in successful) / len(successful)
        avg_total_time = sum(r["total_time"] for r in successful) / len(successful)
        
        print(f"📈 平均上传时间: {avg_upload_time:.2f}秒")
        print(f"📈 平均处理时间: {avg_processing_time:.2f}秒")
        print(f"📈 平均总时间: {avg_total_time:.2f}秒")
        
        # 计算吞吐量
        throughput = len(successful) / total_time
        print(f"🚀 处理吞吐量: {throughput:.2f} 任务/秒")
    
    if failed:
        print(f"\n❌ 失败任务详情:")
        for r in failed:
            print(f"   [{r['test_id']}] {r.get('error', '未知错误')}")

def test_system_load():
    """测试系统负载"""
    print("📊 系统负载测试")
    print("="*40)
    
    try:
        response = requests.get(f"{API_BASE_URL}/system")
        if response.status_code == 200:
            data = response.json()
            
            gpu_info = data["gpu_info"]
            print(f"GPU: {gpu_info['name']}")
            print(f"显存使用: {gpu_info['memory_used']} / {gpu_info['memory_total']}")
            print(f"GPU负载: {gpu_info['gpu_load']}")
            print(f"GPU温度: {gpu_info['temperature']}")
            
            mem_info = data["memory_info"]
            print(f"系统内存: {mem_info['used']} / {mem_info['total']} ({mem_info['percent']})")
            
            print(f"活跃任务: {data['active_tasks']}")
            print(f"最大并发: {data['max_concurrent']}")
            
    except Exception as e:
        print(f"❌ 获取系统状态失败: {e}")

def main():
    """主函数"""
    print("🧪 动漫图片高清修复API - 性能测试")
    print(f"📡 API地址: {API_BASE_URL}")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查服务状态
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API服务不可用")
            return
    except:
        print("❌ 无法连接到API服务")
        return
    
    # 测试图片路径
    test_image = "../test.jpg"
    if not Path(test_image).exists():
        print(f"❌ 测试图片不存在: {test_image}")
        return
    
    # 显示系统负载
    test_system_load()
    
    # 进行并发测试
    concurrent_levels = [1, 2, 4]  # 测试不同并发级别
    
    for concurrent in concurrent_levels:
        print(f"\n{'='*60}")
        print(f"🔄 测试并发级别: {concurrent}")
        print(f"{'='*60}")
        
        test_concurrent_processing(test_image, concurrent)
        
        # 等待一下让系统恢复
        if concurrent < max(concurrent_levels):
            print("\n⏳ 等待系统恢复...")
            time.sleep(5)

if __name__ == "__main__":
    main() 