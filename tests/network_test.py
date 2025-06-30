#!/usr/bin/env python3
"""
网络连接测试脚本 - 测试局域网访问是否正常
"""

import requests
import socket
import time
from pathlib import Path

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def test_port_open(host, port, timeout=3):
    """测试端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_api_health(base_url):
    """测试API健康状态"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
    except Exception as e:
        return False, str(e)
    return False, "未知错误"

def main():
    """主测试函数"""
    print("🔍 动漫图片高清修复API - 网络连接测试")
    print("="*60)
    
    # 获取本机IP
    local_ip = get_local_ip()
    port = 8000
    
    print(f"🖥️  本机IP地址: {local_ip}")
    print(f"🔌 测试端口: {port}")
    print()
    
    # 测试本地连接
    print("📡 测试本地连接...")
    localhost_url = f"http://localhost:{port}"
    if test_port_open("localhost", port):
        print("✅ 本地端口开放正常")
        
        # 测试API健康状态
        health_ok, health_data = test_api_health(localhost_url)
        if health_ok:
            print("✅ API服务运行正常")
            print(f"🔧 最大并发数: {health_data.get('max_concurrent', 'N/A')}")
            print(f"📊 活跃任务: {health_data.get('active_tasks', 'N/A')}")
        else:
            print(f"❌ API服务异常: {health_data}")
    else:
        print("❌ 本地端口未开放，请确认API服务是否启动")
        return
    
    print()
    
    # 测试局域网连接
    print("🌐 测试局域网连接...")
    lan_url = f"http://{local_ip}:{port}"
    
    if test_port_open(local_ip, port):
        print("✅ 局域网端口开放正常")
        
        # 测试API健康状态
        health_ok, health_data = test_api_health(lan_url)
        if health_ok:
            print("✅ 局域网API访问正常")
        else:
            print(f"❌ 局域网API访问异常: {health_data}")
    else:
        print("❌ 局域网端口未开放")
        print("💡 可能的原因:")
        print("   1. 防火墙阻止了端口8000")
        print("   2. API服务未绑定到0.0.0.0")
        print("   3. 网络配置问题")
    
    print()
    print("📋 访问地址汇总:")
    print(f"   本地访问: {localhost_url}")
    print(f"   局域网访问: {lan_url}")
    print(f"   API文档: {lan_url}/docs")
    print(f"   交互式文档: {lan_url}/redoc")
    
    print()
    print("🔧 故障排除:")
    print("   1. 确认API服务正在运行")
    print("   2. 运行 setup_firewall.bat 配置防火墙")
    print("   3. 检查杀毒软件是否阻止网络访问")
    print("   4. 确认路由器没有阻止内网通信")
    
    # 获取网络接口信息
    print()
    print("🔍 网络接口信息:")
    try:
        hostname = socket.gethostname()
        print(f"   主机名: {hostname}")
        
        # 获取所有IP地址
        ip_list = socket.gethostbyname_ex(hostname)[2]
        for i, ip in enumerate(ip_list, 1):
            if not ip.startswith("127."):
                print(f"   网络接口{i}: {ip}")
    except:
        print("   无法获取网络接口信息")

if __name__ == "__main__":
    main() 