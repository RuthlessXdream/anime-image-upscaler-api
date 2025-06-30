"""
请求数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field, validator


class UpscaleRequest(BaseModel):
    """图片放大请求模型"""
    
    ai_model_name: str = Field(
        default="RealESRGAN_x4plus_anime_6B",
        description="使用的AI模型名称",
        example="RealESRGAN_x4plus_anime_6B"
    )
    
    outscale: float = Field(
        default=4.0,
        ge=1.0,
        le=8.0,
        description="输出缩放倍数",
        example=4.0
    )
    
    tile_size: int = Field(
        default=0,
        ge=0,
        description="瓦片大小，0为自动",
        example=0
    )
    
    tile_pad: int = Field(
        default=10,
        ge=0,
        description="瓦片填充大小",
        example=10
    )
    
    pre_pad: int = Field(
        default=0,
        ge=0,
        description="预填充大小",
        example=0
    )
    
    use_half_precision: bool = Field(
        default=True,
        description="是否使用半精度加速",
        example=True
    )
    
    @validator("ai_model_name")
    def validate_model_name(cls, v):
        """验证模型名称"""
        allowed_models = [
            "RealESRGAN_x4plus_anime_6B",
            "RealESRGAN_x4plus",
            "RealESRGAN_x2plus"
        ]
        if v not in allowed_models:
            raise ValueError(f"模型名称必须是以下之一: {allowed_models}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "ai_model_name": "RealESRGAN_x4plus_anime_6B",
                "outscale": 4.0,
                "tile_size": 0,
                "tile_pad": 10,
                "pre_pad": 0,
                "use_half_precision": True
            }
        } 