"""
AI模型管理器
负责Real-ESRGAN模型的加载、初始化和管理
"""

import sys
from pathlib import Path
from typing import Optional
import logging

from ..config import settings
from ..utils.exceptions import ModelLoadError

# 添加Real-ESRGAN路径
sys.path.append(str(settings.project_root / "Real-ESRGAN"))

try:
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
except ImportError as e:
    raise ImportError(f"无法导入Real-ESRGAN模块: {e}")

logger = logging.getLogger(__name__)


class ModelManager:
    """AI模型管理器"""
    
    def __init__(self):
        self._upsampler: Optional[RealESRGANer] = None
        self._model_loaded = False
        self._model_path = settings.model_path
    
    @property
    def is_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self._model_loaded and self._upsampler is not None
    
    @property
    def upsampler(self) -> Optional[RealESRGANer]:
        """获取upsampler实例"""
        return self._upsampler
    
    def load_model(self) -> bool:
        """加载AI模型"""
        try:
            logger.info("正在初始化Real-ESRGAN模型...")
            
            # 检查模型文件是否存在
            if not self._model_path.exists():
                raise ModelLoadError(f"模型文件不存在: {self._model_path}")
            
            # 创建模型架构
            model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=6,
                num_grow_ch=32,
                scale=settings.model_scale
            )
            
            # 初始化upsampler
            self._upsampler = RealESRGANer(
                scale=settings.model_scale,
                model_path=str(self._model_path),
                model=model,
                tile=settings.tile_size,
                tile_pad=settings.tile_pad,
                pre_pad=settings.pre_pad,
                half=settings.use_half_precision,
                gpu_id=settings.gpu_id
            )
            
            self._model_loaded = True
            logger.info("Real-ESRGAN模型初始化完成")
            return True
            
        except Exception as e:
            logger.error(f"模型初始化失败: {str(e)}")
            self._model_loaded = False
            raise ModelLoadError(f"模型加载失败: {str(e)}")
    
    def unload_model(self):
        """卸载模型"""
        if self._upsampler:
            del self._upsampler
            self._upsampler = None
        self._model_loaded = False
        logger.info("模型已卸载")
    
    def reload_model(self) -> bool:
        """重新加载模型"""
        logger.info("正在重新加载模型...")
        self.unload_model()
        return self.load_model()
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            "model_path": str(self._model_path),
            "model_loaded": self._model_loaded,
            "model_exists": self._model_path.exists(),
            "model_size_mb": round(self._model_path.stat().st_size / (1024 * 1024), 2) if self._model_path.exists() else 0,
            "scale": settings.model_scale,
            "use_half_precision": settings.use_half_precision,
            "gpu_id": settings.gpu_id
        }


# 全局模型管理器实例
model_manager = ModelManager() 