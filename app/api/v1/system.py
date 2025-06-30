"""
系统状态API路由
"""

import psutil
import time
from datetime import datetime
from fastapi import APIRouter

from ...config import settings
from ...core.model_manager import model_manager
from ...models.response import SystemStatusResponse

router = APIRouter()

# 记录启动时间
_start_time = time.time()


def get_gpu_info():
    """获取GPU信息"""
    gpu_info = {
        "available": False,
        "device_count": 0,
        "current_device": 0,
        "device_name": "N/A",
        "memory_total": 0,
        "memory_used": 0,
        "memory_free": 0,
        "temperature": 0
    }
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_info["available"] = True
            gpu_info["device_count"] = torch.cuda.device_count()
            gpu_info["current_device"] = torch.cuda.current_device()
            gpu_info["device_name"] = torch.cuda.get_device_name()
            
            # GPU内存信息
            memory_stats = torch.cuda.memory_stats()
            gpu_info["memory_total"] = torch.cuda.get_device_properties(0).total_memory
            gpu_info["memory_used"] = memory_stats.get("allocated_bytes.all.current", 0)
            gpu_info["memory_free"] = gpu_info["memory_total"] - gpu_info["memory_used"]
            
            # 尝试获取GPU温度
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_info["temperature"] = gpus[0].temperature
            except ImportError:
                pass
                
    except ImportError:
        pass
    
    return gpu_info


def get_memory_info():
    """获取内存信息"""
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percent": memory.percent,
        "total_gb": round(memory.total / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2)
    }


@router.get("/system/status", response_model=SystemStatusResponse)
async def get_system_status():
    """获取系统状态"""
    
    uptime = time.time() - _start_time
    
    return SystemStatusResponse(
        status="running",
        model_loaded=model_manager.is_loaded,
        active_tasks=0,  # TODO: 从任务管理器获取
        max_concurrent=settings.max_workers or 4,
        gpu_info=get_gpu_info(),
        memory_info=get_memory_info(),
        queue_length=0,  # TODO: 从任务管理器获取
        uptime=uptime,
        version=settings.app_version
    )


@router.get("/system/model")
async def get_model_info():
    """获取模型信息"""
    return model_manager.get_model_info()


@router.post("/system/model/reload")
async def reload_model():
    """重新加载模型"""
    try:
        success = model_manager.reload_model()
        return {
            "success": success,
            "message": "模型重新加载成功" if success else "模型重新加载失败"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"模型重新加载失败: {str(e)}"
        }