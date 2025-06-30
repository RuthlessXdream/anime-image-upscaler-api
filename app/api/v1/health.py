"""
健康检查API路由
"""

import psutil
from datetime import datetime
from fastapi import APIRouter

from ...config import settings
from ...core.model_manager import model_manager
from ...models.response import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查端点"""
    
    # 检查磁盘空间
    disk_usage = psutil.disk_usage(str(settings.project_root))
    disk_space = {
        "total": f"{disk_usage.total / (1024**3):.1f}GB",
        "used": f"{disk_usage.used / (1024**3):.1f}GB", 
        "free": f"{disk_usage.free / (1024**3):.1f}GB",
        "percent": f"{(disk_usage.used / disk_usage.total) * 100:.1f}%"
    }
    
    # 检查GPU是否可用
    gpu_available = False
    try:
        import torch
        gpu_available = torch.cuda.is_available()
    except ImportError:
        pass
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=model_manager.is_loaded,
        gpu_available=gpu_available,
        disk_space=disk_space,
        version=settings.app_version
    ) 