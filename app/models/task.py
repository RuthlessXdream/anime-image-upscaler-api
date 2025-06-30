"""
任务状态数据模型
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskState(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(BaseModel):
    """任务状态模型"""
    
    task_id: str = Field(description="任务唯一标识符")
    
    status: TaskState = Field(description="任务状态")
    
    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="任务进度百分比"
    )
    
    message: str = Field(description="状态消息")
    
    current_step: Optional[str] = Field(
        default=None,
        description="当前处理步骤"
    )
    
    # 时间信息
    created_at: datetime = Field(description="任务创建时间")
    
    started_at: Optional[datetime] = Field(
        default=None,
        description="任务开始时间"
    )
    
    completed_at: Optional[datetime] = Field(
        default=None,
        description="任务完成时间"
    )
    
    # 处理信息
    processing_time: Optional[float] = Field(
        default=None,
        description="已处理时间(秒)"
    )
    
    estimated_remaining: Optional[int] = Field(
        default=None,
        description="预估剩余时间(秒)"
    )
    
    estimated_total_time: Optional[int] = Field(
        default=None,
        description="预估总时间(秒)"
    )
    
    # 文件信息
    input_filename: Optional[str] = Field(
        default=None,
        description="输入文件名"
    )
    
    output_filename: Optional[str] = Field(
        default=None,
        description="输出文件名"
    )
    
    file_size: Optional[str] = Field(
        default=None,
        description="文件大小描述"
    )
    
    output_size: Optional[str] = Field(
        default=None,
        description="输出文件大小"
    )
    
    # 图片信息
    input_resolution: Optional[str] = Field(
        default=None,
        description="输入图片分辨率"
    )
    
    output_resolution: Optional[str] = Field(
        default=None,
        description="输出图片分辨率"
    )
    
    # 下载信息
    download_url: Optional[str] = Field(
        default=None,
        description="结果下载链接"
    )
    
    # 错误信息
    error_details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="错误详情"
    )
    
    # 处理参数
    processing_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="处理参数"
    )
    
    @property
    def is_finished(self) -> bool:
        """判断任务是否已完成"""
        return self.status in [TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED]
    
    @property
    def is_successful(self) -> bool:
        """判断任务是否成功完成"""
        return self.status == TaskState.COMPLETED
    
    @property
    def duration(self) -> Optional[float]:
        """获取任务持续时间"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "task_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "processing",
                "progress": 45.5,
                "message": "正在进行AI放大处理...",
                "current_step": "AI处理中",
                "created_at": "2024-01-01T12:00:00Z",
                "started_at": "2024-01-01T12:00:05Z",
                "processing_time": 30.5,
                "estimated_remaining": 25,
                "input_filename": "anime.jpg",
                "file_size": "150KB",
                "input_resolution": "512x512"
            }
        } 