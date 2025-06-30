import os
import sys
import uuid
import asyncio
from pathlib import Path
from typing import Optional
import warnings
import aiofiles
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor
import logging
import time
import psutil
import GPUtil

# 过滤torchvision的废弃警告
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")

# 添加Real-ESRGAN路径
sys.path.append(str(Path(__file__).parent.parent / "Real-ESRGAN"))

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="动漫图片高清修复API",
    description="基于Real-ESRGAN的动漫图片四倍放大和高清修复服务",
    version="1.0.0"
)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic模型定义
class UpscaleRequest(BaseModel):
    """图片放大请求模型"""
    ai_model_name: str = Field(default="RealESRGAN_x4plus_anime_6B", description="使用的模型名称")
    outscale: float = Field(default=4.0, description="输出缩放倍数", ge=1.0, le=8.0)
    tile_size: int = Field(default=0, description="瓦片大小，0为自动", ge=0)
    
class UpscaleResponse(BaseModel):
    """图片放大响应模型"""
    task_id: str = Field(description="任务ID")
    status: str = Field(description="任务状态")
    message: str = Field(description="响应消息")
    download_url: Optional[str] = Field(default=None, description="下载链接")
    estimated_time: Optional[int] = Field(default=None, description="预估处理时间(秒)")

class TaskStatus(BaseModel):
    """任务状态模型"""
    task_id: str
    status: str  # pending, processing, completed, failed
    progress: float = Field(ge=0.0, le=100.0)
    message: str
    download_url: Optional[str] = None
    processing_time: Optional[float] = Field(default=None, description="已处理时间(秒)")
    estimated_remaining: Optional[int] = Field(default=None, description="预估剩余时间(秒)")
    current_step: Optional[str] = Field(default=None, description="当前处理步骤")

class SystemStatus(BaseModel):
    """系统状态模型"""
    gpu_info: dict
    memory_info: dict
    active_tasks: int
    queue_length: int
    max_concurrent: int

# 检测最佳并发数量
def detect_optimal_concurrency():
    """根据GPU显存自动检测最佳并发数量"""
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # 使用第一个GPU
            total_memory = gpu.memoryTotal  # MB
            used_memory = gpu.memoryUsed    # MB
            free_memory = total_memory - used_memory
            
            # Real-ESRGAN每个任务大约需要2-3GB显存
            # RTX 4090有24GB显存，预留6GB给系统，剩余18GB
            # 18GB / 3GB = 6个任务，但为了稳定性设置为4个
            if total_memory >= 20000:  # 20GB+
                return 4
            elif total_memory >= 12000:  # 12GB+
                return 3
            elif total_memory >= 8000:   # 8GB+
                return 2
            else:
                return 1
        else:
            return 2  # 没有GPU时的默认值
    except:
        return 2  # 检测失败时的默认值

# 全局变量
MAX_WORKERS = detect_optimal_concurrency()
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
task_status = {}  # 任务状态字典
upsampler = None  # 全局upsampler实例
task_queue = []   # 任务队列

logger.info(f"🚀 检测到最佳并发数量: {MAX_WORKERS}")

# 创建必要的目录
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def get_gpu_info():
    """获取GPU信息"""
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            return {
                "name": gpu.name,
                "memory_total": f"{gpu.memoryTotal}MB",
                "memory_used": f"{gpu.memoryUsed}MB",
                "memory_free": f"{gpu.memoryTotal - gpu.memoryUsed}MB",
                "gpu_load": f"{gpu.load * 100:.1f}%",
                "temperature": f"{gpu.temperature}°C"
            }
    except:
        pass
    return {"error": "无法获取GPU信息"}

def get_memory_info():
    """获取系统内存信息"""
    memory = psutil.virtual_memory()
    return {
        "total": f"{memory.total // (1024**3)}GB",
        "used": f"{memory.used // (1024**3)}GB",
        "free": f"{memory.available // (1024**3)}GB",
        "percent": f"{memory.percent:.1f}%"
    }

def initialize_model():
    """初始化Real-ESRGAN模型"""
    global upsampler
    try:
        logger.info("正在初始化Real-ESRGAN模型...")
        
        # 设置模型路径
        model_path = Path(__file__).parent / "Real-ESRGAN" / "weights" / "RealESRGAN_x4plus_anime_6B.pth"
        
        # 创建模型
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        
        # 初始化upsampler
        upsampler = RealESRGANer(
            scale=4,
            model_path=str(model_path),
            model=model,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=True,  # 使用半精度提高速度
            gpu_id=0
        )
        
        logger.info("Real-ESRGAN模型初始化完成")
        return True
    except Exception as e:
        logger.error(f"模型初始化失败: {str(e)}")
        return False

def process_image(input_path: str, output_path: str, task_id: str) -> bool:
    """处理图片的核心函数"""
    start_time = time.time()
    
    try:
        logger.info(f"开始处理图片: {input_path}")
        task_status[task_id]["status"] = "processing"
        task_status[task_id]["progress"] = 5.0
        task_status[task_id]["current_step"] = "正在读取图片..."
        task_status[task_id]["start_time"] = start_time
        
        # 读取图片
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("无法读取图片文件")
        
        # 获取图片信息
        height, width = img.shape[:2]
        task_status[task_id]["progress"] = 15.0
        task_status[task_id]["current_step"] = f"图片尺寸: {width}x{height}, 正在预处理..."
        
        # 预估处理时间（基于图片大小）
        pixels = width * height
        estimated_seconds = max(10, pixels // 100000)  # 粗略估算
        task_status[task_id]["estimated_total_time"] = estimated_seconds
        
        task_status[task_id]["progress"] = 25.0
        task_status[task_id]["current_step"] = "正在进行AI放大处理..."
        
        # 使用Real-ESRGAN处理
        logger.info("正在进行AI放大处理...")
        output, _ = upsampler.enhance(img, outscale=4)
        
        task_status[task_id]["progress"] = 85.0
        task_status[task_id]["current_step"] = "正在保存结果..."
        
        # 保存结果
        success = cv2.imwrite(output_path, output)
        if not success:
            raise ValueError("保存图片失败")
        
        # 获取输出文件大小
        output_size = os.path.getsize(output_path)
        processing_time = time.time() - start_time
        
        task_status[task_id]["status"] = "completed"
        task_status[task_id]["progress"] = 100.0
        task_status[task_id]["download_url"] = f"/download/{task_id}"
        task_status[task_id]["message"] = f"处理完成！耗时 {processing_time:.1f}秒"
        task_status[task_id]["current_step"] = "处理完成"
        task_status[task_id]["processing_time"] = processing_time
        task_status[task_id]["output_size"] = f"{output_size // 1024}KB"
        task_status[task_id]["output_resolution"] = f"{output.shape[1]}x{output.shape[0]}"
        
        logger.info(f"图片处理完成: {output_path}, 耗时: {processing_time:.1f}秒")
        return True
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"图片处理失败: {str(e)}")
        task_status[task_id]["status"] = "failed"
        task_status[task_id]["message"] = f"处理失败: {str(e)}"
        task_status[task_id]["current_step"] = "处理失败"
        task_status[task_id]["processing_time"] = processing_time
        return False

def update_progress_periodically(task_id: str):
    """定期更新进度显示"""
    while task_id in task_status and task_status[task_id]["status"] == "processing":
        current_time = time.time()
        start_time = task_status[task_id].get("start_time", current_time)
        processing_time = current_time - start_time
        
        task_status[task_id]["processing_time"] = processing_time
        
        # 根据已处理时间和当前进度估算剩余时间
        progress = task_status[task_id]["progress"]
        if progress > 5:
            estimated_total = processing_time * 100 / progress
            estimated_remaining = max(0, estimated_total - processing_time)
            task_status[task_id]["estimated_remaining"] = int(estimated_remaining)
        
        time.sleep(2)  # 每2秒更新一次

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化模型"""
    success = initialize_model()
    if not success:
        logger.error("模型初始化失败，API可能无法正常工作")

@app.get("/", response_model=dict)
async def root():
    """根路径，返回API信息"""
    return {
        "message": "动漫图片高清修复API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": upsampler is not None,
        "max_concurrent": MAX_WORKERS,
        "gpu_info": get_gpu_info()
    }

@app.get("/system", response_model=SystemStatus)
async def get_system_status():
    """获取系统状态信息"""
    active_tasks = len([t for t in task_status.values() if t["status"] in ["pending", "processing"]])
    
    return SystemStatus(
        gpu_info=get_gpu_info(),
        memory_info=get_memory_info(),
        active_tasks=active_tasks,
        queue_length=len(task_queue),
        max_concurrent=MAX_WORKERS
    )

@app.post("/upscale", response_model=UpscaleResponse)
async def upscale_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="要处理的图片文件"),
):
    """
    上传图片进行四倍放大处理
    """
    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="只支持图片文件")
    
    if upsampler is None:
        raise HTTPException(status_code=503, detail="模型未加载，请稍后重试")
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    try:
        # 保存上传的文件
        file_extension = Path(file.filename).suffix
        input_filename = f"{task_id}_input{file_extension}"
        output_filename = f"{task_id}_output{file_extension}"
        
        input_path = UPLOAD_DIR / input_filename
        output_path = OUTPUT_DIR / output_filename
        
        # 异步保存文件
        async with aiofiles.open(input_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 获取文件大小用于预估时间
        file_size = len(content)
        estimated_time = max(15, file_size // (1024 * 1024) * 10)  # 每MB大约10秒
        
        # 初始化任务状态
        task_status[task_id] = {
            "task_id": task_id,
            "status": "pending",
            "progress": 0.0,
            "message": "任务已创建，等待处理",
            "download_url": None,
            "input_path": str(input_path),
            "output_path": str(output_path),
            "file_size": f"{file_size // 1024}KB",
            "current_step": "等待处理",
            "created_time": time.time()
        }
        
        # 提交后台任务
        background_tasks.add_task(
            lambda: executor.submit(process_image, str(input_path), str(output_path), task_id)
        )
        
        # 启动进度更新任务
        background_tasks.add_task(
            lambda: executor.submit(update_progress_periodically, task_id)
        )
        
        return UpscaleResponse(
            task_id=task_id,
            status="pending",
            message="任务已提交，正在处理中",
            estimated_time=estimated_time
        )
        
    except Exception as e:
        logger.error(f"上传文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@app.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """
    查询任务状态
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return TaskStatus(**task_status[task_id])

@app.get("/download/{task_id}")
async def download_result(task_id: str):
    """
    下载处理结果
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = task_status[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务未完成")
    
    output_path = Path(task["output_path"])
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="结果文件不存在")
    
    return FileResponse(
        path=str(output_path),
        filename=f"upscaled_{task_id}.jpg",
        media_type="image/jpeg"
    )

@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """
    删除任务和相关文件
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = task_status[task_id]
    
    # 删除文件
    try:
        input_path = Path(task["input_path"])
        output_path = Path(task["output_path"])
        
        if input_path.exists():
            input_path.unlink()
        if output_path.exists():
            output_path.unlink()
    except Exception as e:
        logger.warning(f"删除文件失败: {str(e)}")
    
    # 删除任务状态
    del task_status[task_id]
    
    return {"message": "任务已删除"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    active_tasks = len([t for t in task_status.values() if t["status"] in ["pending", "processing"]])
    
    return {
        "status": "healthy",
        "model_loaded": upsampler is not None,
        "active_tasks": active_tasks,
        "max_concurrent": MAX_WORKERS,
        "gpu_info": get_gpu_info(),
        "memory_info": get_memory_info()
    }

@app.get("/tasks")
async def list_all_tasks():
    """列出所有任务状态"""
    return {
        "total_tasks": len(task_status),
        "active_tasks": len([t for t in task_status.values() if t["status"] in ["pending", "processing"]]),
        "completed_tasks": len([t for t in task_status.values() if t["status"] == "completed"]),
        "failed_tasks": len([t for t in task_status.values() if t["status"] == "failed"]),
        "tasks": list(task_status.values())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 