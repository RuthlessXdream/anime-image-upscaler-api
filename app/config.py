"""
应用配置管理
使用Pydantic Settings进行类型安全的配置管理
"""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基础配置
    app_name: str = Field(default="动漫图片高清修复API", description="应用名称")
    app_version: str = Field(default="2.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    
    # 服务器配置
    host: str = Field(default="0.0.0.0", description="服务器地址")
    port: int = Field(default=8000, description="服务器端口")
    reload: bool = Field(default=False, description="自动重载")
    
    # 文件路径配置
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    upload_dir: Path = Field(default="uploads", description="上传目录")
    output_dir: Path = Field(default="outputs", description="输出目录")
    model_dir: Path = Field(default="Real-ESRGAN/weights", description="模型目录")
    
    # AI模型配置
    model_name: str = Field(default="RealESRGAN_x4plus_anime_6B.pth", description="模型文件名")
    model_scale: int = Field(default=4, description="放大倍数")
    use_half_precision: bool = Field(default=True, description="使用半精度")
    tile_size: int = Field(default=0, description="瓦片大小")
    tile_pad: int = Field(default=10, description="瓦片填充")
    pre_pad: int = Field(default=0, description="预填充")
    
    # 并发配置
    max_workers: Optional[int] = Field(default=None, description="最大工作进程数")
    auto_detect_workers: bool = Field(default=True, description="自动检测工作进程数")
    
    # GPU配置
    gpu_id: int = Field(default=0, description="GPU设备ID")
    memory_threshold: float = Field(default=0.8, description="显存使用阈值")
    
    # 任务配置
    task_timeout: int = Field(default=300, description="任务超时时间(秒)")
    cleanup_interval: int = Field(default=3600, description="清理间隔(秒)")
    max_file_size: int = Field(default=50 * 1024 * 1024, description="最大文件大小(字节)")
    
    # 支持的文件格式
    allowed_extensions: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"],
        description="允许的文件扩展名"
    )
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: Optional[str] = Field(default=None, description="日志文件路径")
    
    # CORS配置
    cors_origins: List[str] = Field(default=["*"], description="CORS允许的源")
    
    @validator("upload_dir", "output_dir", "model_dir", pre=True)
    def resolve_paths(cls, v, values):
        """解析相对路径为绝对路径"""
        if isinstance(v, str):
            v = Path(v)
        if not v.is_absolute():
            project_root = values.get("project_root", Path(__file__).parent.parent)
            v = project_root / v
        return v
    
    @validator("allowed_extensions")
    def validate_extensions(cls, v):
        """确保扩展名以点开头"""
        return [ext if ext.startswith('.') else f'.{ext}' for ext in v]
    
    @property
    def model_path(self) -> Path:
        """获取模型文件完整路径"""
        return self.model_dir / self.model_name
    
    def create_directories(self):
        """创建必要的目录"""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置的单例"""
    return Settings()


# 全局配置实例
settings = get_settings() 