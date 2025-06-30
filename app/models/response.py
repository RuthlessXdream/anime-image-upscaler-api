"""
响应数据模型
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .task import TaskStatus


class UpscaleResponse(BaseModel):
    """图片放大响应模型"""
    
    task_id: str = Field(description="任务ID")
    
    status: str = Field(description="任务状态")
    
    message: str = Field(description="响应消息")
    
    download_url: Optional[str] = Field(
        default=None,
        description="下载链接"
    )
    
    estimated_time: Optional[int] = Field(
        default=None,
        description="预估处理时间(秒)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "pending",
                "message": "任务已提交，正在处理中",
                "estimated_time": 30
            }
        }


class TaskStatusResponse(BaseModel):
    """任务状态响应模型"""
    
    success: bool = Field(description="请求是否成功")
    
    data: TaskStatus = Field(description="任务状态数据")
    
    message: Optional[str] = Field(
        default=None,
        description="响应消息"
    )


class SystemStatusResponse(BaseModel):
    """系统状态响应模型"""
    
    status: str = Field(description="系统状态")
    
    model_loaded: bool = Field(description="模型是否已加载")
    
    active_tasks: int = Field(description="活跃任务数")
    
    max_concurrent: int = Field(description="最大并发数")
    
    gpu_info: Dict[str, Any] = Field(description="GPU信息")
    
    memory_info: Dict[str, Any] = Field(description="内存信息")
    
    queue_length: int = Field(default=0, description="队列长度")
    
    uptime: Optional[float] = Field(
        default=None,
        description="运行时间(秒)"
    )
    
    version: str = Field(description="API版本")


class TaskListResponse(BaseModel):
    """任务列表响应模型"""
    
    total_tasks: int = Field(description="总任务数")
    
    active_tasks: int = Field(description="活跃任务数")
    
    completed_tasks: int = Field(description="已完成任务数")
    
    failed_tasks: int = Field(description="失败任务数")
    
    tasks: List[TaskStatus] = Field(description="任务列表")


class HealthCheckResponse(BaseModel):
    """健康检查响应模型"""
    
    status: str = Field(description="健康状态")
    
    timestamp: str = Field(description="检查时间戳")
    
    model_loaded: bool = Field(description="模型是否已加载")
    
    gpu_available: bool = Field(description="GPU是否可用")
    
    disk_space: Dict[str, str] = Field(description="磁盘空间信息")
    
    version: str = Field(description="API版本")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    
    error: bool = Field(default=True, description="是否为错误")
    
    error_code: str = Field(description="错误代码")
    
    error_message: str = Field(description="错误消息")
    
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="错误详情"
    )
    
    timestamp: str = Field(description="错误时间戳")


class SuccessResponse(BaseModel):
    """成功响应模型"""
    
    success: bool = Field(default=True, description="是否成功")
    
    message: str = Field(description="成功消息")
    
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="响应数据"
    ) 