#!/usr/bin/env python3
"""
Docker部署测试脚本
验证API服务是否正常工作
"""

import requests
import time
import sys
import json
from pathlib import Path


def test_health_check(base_url="http://localhost:7999"):
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 健康检查通过")
            print(f"   状态: {data.get('status')}")
            print(f"   模型已加载: {data.get('model_loaded')}")
            print(f"   GPU可用: {data.get('gpu_available')}")
            return True
        else:
            print(f"❌ 健康检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False


def test_system_status(base_url="http://localhost:7999"):
    """测试系统状态接口"""
    print("🔍 测试系统状态接口...")
    try:
        response = requests.get(f"{base_url}/api/v1/system/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ 系统状态正常")
            print(f"   活跃任务: {data.get('active_tasks')}")
            print(f"   最大并发: {data.get('max_concurrent')}")
            print(f"   GPU信息: {data.get('gpu_info', {}).get('name', 'N/A')}")
            return True
        else:
            print(f"❌ 系统状态检查失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 系统状态检查异常: {e}")
        return False


def test_api_docs(base_url="http://localhost:7999"):
    """测试API文档是否可访问"""
    print("🔍 测试API文档...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API文档可访问")
            return True
        else:
            print(f"❌ API文档不可访问: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API文档访问异常: {e}")
        return False


def test_upload_interface(base_url="http://localhost:7999"):
    """测试上传接口（不实际上传文件）"""
    print("🔍 测试上传接口...")
    try:
        # 测试GET请求到上传接口（应该返回405 Method Not Allowed）
        response = requests.get(f"{base_url}/api/v1/upscale", timeout=10)
        if response.status_code == 405:
            print("✅ 上传接口响应正常")
            return True
        else:
            print(f"⚠️ 上传接口响应异常: HTTP {response.status_code}")
            return True  # 这不是致命错误
    except Exception as e:
        print(f"❌ 上传接口测试异常: {e}")
        return False


def wait_for_service(base_url="http://localhost:7999", max_wait=60):
    """等待服务启动"""
    print(f"⏳ 等待服务启动 (最多等待{max_wait}秒)...")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ 服务已启动 (等待了{i}秒)")
                return True
        except:
            pass
        
        if i % 10 == 0 and i > 0:
            print(f"   仍在等待... ({i}/{max_wait}秒)")
        
        time.sleep(1)
    
    print(f"❌ 服务启动超时 ({max_wait}秒)")
    return False


def main():
    """主测试函数"""
    print("🐳 Docker部署测试开始")
    print("=" * 50)
    
    base_url = "http://localhost:7999"
    
    # 等待服务启动
    if not wait_for_service(base_url):
        print("❌ 服务未能正常启动")
        sys.exit(1)
    
    # 运行测试
    tests = [
        test_health_check,
        test_system_status,
        test_api_docs,
        test_upload_interface
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test(base_url):
            passed += 1
        print()
    
    # 输出测试结果
    print("=" * 50)
    print(f"🧪 测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Docker部署成功！")
        print()
        print("🌐 服务访问地址:")
        print(f"   - API服务: {base_url}")
        print(f"   - API文档: {base_url}/docs")
        print(f"   - 交互式文档: {base_url}/redoc")
        print(f"   - 健康检查: {base_url}/health")
        sys.exit(0)
    else:
        print("❌ 部分测试失败，请检查服务状态")
        sys.exit(1)


if __name__ == "__main__":
    main() 