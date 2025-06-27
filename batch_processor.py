#!/usr/bin/env python3
"""
批量图片处理脚本 - 保持目录结构的批量高清修复
"""

import os
import requests
import time
from pathlib import Path
import concurrent.futures
from datetime import datetime
import shutil
from collections import defaultdict
import json

API_BASE_URL = "http://localhost:8000"

class BatchProcessor:
    def __init__(self, source_dir, target_dir, max_workers=4):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.max_workers = max_workers
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None
        }
        self.failed_files = []
        
        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    def print_separator(self, title="", width=80):
        """打印分隔线"""
        if title:
            padding = (width - len(title) - 2) // 2
            print(f"\n{'='*padding} {title} {'='*padding}")
        else:
            print("="*width)
    
    def format_time(self, seconds):
        """格式化时间显示"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            return f"{seconds//60:.0f}分{seconds%60:.0f}秒"
        else:
            return f"{seconds//3600:.0f}小时{(seconds%3600)//60:.0f}分"
    
    def check_api_status(self):
        """检查API服务状态"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API服务正常")
                print(f"🔧 最大并发数: {data.get('max_concurrent', 'N/A')}")
                print(f"📊 当前活跃任务: {data.get('active_tasks', 'N/A')}")
                return True
            else:
                print(f"❌ API服务异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 无法连接API服务: {e}")
            return False
    
    def scan_images(self):
        """扫描所有图片文件"""
        print("🔍 扫描图片文件...")
        image_files = []
        
        if not self.source_dir.exists():
            print(f"❌ 源目录不存在: {self.source_dir}")
            return []
        
        # 遍历所有文件
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.image_extensions:
                    # 计算相对路径
                    rel_path = file_path.relative_to(self.source_dir)
                    target_path = self.target_dir / rel_path
                    
                    image_files.append({
                        'source': file_path,
                        'target': target_path,
                        'relative': rel_path
                    })
        
        self.stats['total_files'] = len(image_files)
        print(f"📊 找到 {len(image_files)} 个图片文件")
        
        # 显示目录结构统计
        dir_stats = defaultdict(int)
        for img in image_files:
            parts = img['relative'].parts
            if len(parts) >= 2:
                series_id = parts[0]
                dir_stats[series_id] += 1
        
        print(f"📁 涉及 {len(dir_stats)} 个系列目录")
        print(f"📈 平均每个系列 {sum(dir_stats.values()) / len(dir_stats):.1f} 张图片")
        
        return image_files
    
    def create_target_structure(self, image_files):
        """创建目标目录结构"""
        print("📁 创建目标目录结构...")
        
        # 创建根目录
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建所有需要的子目录
        dirs_to_create = set()
        for img in image_files:
            dirs_to_create.add(img['target'].parent)
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ 创建了 {len(dirs_to_create)} 个目录")
    
    def process_single_image(self, image_info):
        """处理单个图片"""
        source_path = image_info['source']
        target_path = image_info['target']
        relative_path = image_info['relative']
        
        try:
            # 检查目标文件是否已存在
            if target_path.exists():
                print(f"⏭️  跳过已存在: {relative_path}")
                self.stats['skipped'] += 1
                return {'status': 'skipped', 'path': relative_path}
            
            print(f"📤 处理: {relative_path}")
            start_time = time.time()
            
            # 上传文件到API
            with open(source_path, 'rb') as f:
                files = {"file": (source_path.name, f, f"image/{source_path.suffix[1:]}")}
                response = requests.post(f"{API_BASE_URL}/upscale", files=files, timeout=30)
            
            if response.status_code != 200:
                error_msg = f"上传失败: {response.status_code}"
                print(f"❌ {relative_path}: {error_msg}")
                self.failed_files.append({'path': relative_path, 'error': error_msg})
                self.stats['failed'] += 1
                return {'status': 'failed', 'path': relative_path, 'error': error_msg}
            
            result = response.json()
            task_id = result["task_id"]
            
            # 等待处理完成
            while True:
                status_response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=10)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    
                    if status_data["status"] == "completed":
                        # 下载处理结果
                        download_response = requests.get(f"{API_BASE_URL}/download/{task_id}", timeout=60)
                        if download_response.status_code == 200:
                            # 保存到目标路径
                            with open(target_path, 'wb') as f:
                                f.write(download_response.content)
                            
                            processing_time = time.time() - start_time
                            file_size = target_path.stat().st_size
                            print(f"✅ {relative_path} (耗时: {processing_time:.1f}s, 大小: {file_size//1024}KB)")
                            
                            # 清理任务
                            try:
                                requests.delete(f"{API_BASE_URL}/task/{task_id}", timeout=5)
                            except:
                                pass
                            
                            self.stats['processed'] += 1
                            return {'status': 'success', 'path': relative_path, 'time': processing_time}
                        else:
                            error_msg = f"下载失败: {download_response.status_code}"
                            print(f"❌ {relative_path}: {error_msg}")
                            self.failed_files.append({'path': relative_path, 'error': error_msg})
                            self.stats['failed'] += 1
                            return {'status': 'failed', 'path': relative_path, 'error': error_msg}
                    
                    elif status_data["status"] == "failed":
                        error_msg = f"处理失败: {status_data.get('message', '未知错误')}"
                        print(f"❌ {relative_path}: {error_msg}")
                        self.failed_files.append({'path': relative_path, 'error': error_msg})
                        self.stats['failed'] += 1
                        return {'status': 'failed', 'path': relative_path, 'error': error_msg}
                
                time.sleep(1)  # 等待1秒再查询
                
        except Exception as e:
            error_msg = f"处理异常: {str(e)}"
            print(f"❌ {relative_path}: {error_msg}")
            self.failed_files.append({'path': relative_path, 'error': error_msg})
            self.stats['failed'] += 1
            return {'status': 'failed', 'path': relative_path, 'error': error_msg}
    
    def process_batch(self, image_files):
        """批量处理图片"""
        print(f"🚀 开始批量处理 (并发数: {self.max_workers})")
        self.stats['start_time'] = time.time()
        
        # 使用线程池进行并发处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_image = {
                executor.submit(self.process_single_image, img): img 
                for img in image_files
            }
            
            # 处理完成的任务
            completed = 0
            for future in concurrent.futures.as_completed(future_to_image):
                completed += 1
                progress = (completed / len(image_files)) * 100
                
                # 显示进度
                if completed % 10 == 0 or completed == len(image_files):
                    elapsed = time.time() - self.stats['start_time']
                    eta = (elapsed / completed) * (len(image_files) - completed) if completed > 0 else 0
                    print(f"📊 进度: {completed}/{len(image_files)} ({progress:.1f}%) | "
                          f"已用时: {self.format_time(elapsed)} | "
                          f"预计剩余: {self.format_time(eta)}")
        
        self.stats['end_time'] = time.time()
    
    def print_summary(self):
        """打印处理总结"""
        self.print_separator("处理完成")
        
        total_time = self.stats['end_time'] - self.stats['start_time']
        
        print(f"📊 处理统计:")
        print(f"   总文件数: {self.stats['total_files']}")
        print(f"   成功处理: {self.stats['processed']}")
        print(f"   处理失败: {self.stats['failed']}")
        print(f"   跳过文件: {self.stats['skipped']}")
        print(f"   总耗时: {self.format_time(total_time)}")
        
        if self.stats['processed'] > 0:
            avg_time = total_time / self.stats['processed']
            throughput = self.stats['processed'] / total_time
            print(f"   平均耗时: {avg_time:.2f}秒/张")
            print(f"   处理速度: {throughput:.2f}张/秒")
        
        if self.failed_files:
            print(f"\n❌ 失败文件列表:")
            for fail in self.failed_files[:10]:  # 只显示前10个
                print(f"   {fail['path']}: {fail['error']}")
            if len(self.failed_files) > 10:
                print(f"   ... 还有 {len(self.failed_files) - 10} 个失败文件")
        
        # 保存失败列表到文件
        if self.failed_files:
            failed_log = self.target_dir / "failed_files.json"
            with open(failed_log, 'w', encoding='utf-8') as f:
                json.dump(self.failed_files, f, ensure_ascii=False, indent=2)
            print(f"💾 失败文件列表已保存到: {failed_log}")
    
    def run(self):
        """运行批量处理"""
        self.print_separator("动漫图片批量高清修复")
        
        print(f"📁 源目录: {self.source_dir}")
        print(f"📁 目标目录: {self.target_dir}")
        print(f"🔧 并发数: {self.max_workers}")
        
        # 检查API状态
        if not self.check_api_status():
            print("❌ API服务不可用，请先启动API服务")
            return False
        
        # 扫描图片文件
        image_files = self.scan_images()
        if not image_files:
            print("❌ 没有找到图片文件")
            return False
        
        # 创建目标目录结构
        self.create_target_structure(image_files)
        
        # 确认处理
        print(f"\n⚠️  即将处理 {len(image_files)} 个图片文件")
        confirm = input("是否继续? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 用户取消操作")
            return False
        
        # 开始批量处理
        self.process_batch(image_files)
        
        # 打印总结
        self.print_summary()
        
        return True

def main():
    """主函数"""
    print("🚀 动漫图片批量高清修复工具")
    
    # 默认路径
    source_dir = r"C:\animate-photos\top100_series"
    target_dir = r"C:\animate-photos\top100_series_upscale"
    
    # 检查源目录
    if not Path(source_dir).exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return
    
    # 创建处理器
    processor = BatchProcessor(source_dir, target_dir, max_workers=4)
    
    # 运行处理
    success = processor.run()
    
    if success:
        print("\n🎉 批量处理完成!")
    else:
        print("\n❌ 批量处理失败!")

if __name__ == "__main__":
    main() 