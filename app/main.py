"""
现代化的动漫图片高清修复API
基于FastAPI + Pydantic的企业级架构
"""

import logging
import warnings
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .core.model_manager import model_manager
from .utils.exceptions import BaseAPIException
from .models.response import ErrorResponse

# 过滤警告
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")
warnings.filterwarnings("ignore", message=".*torchvision.transforms.functional_tensor.*")
warnings.filterwarnings("ignore", message=".*deprecated.*", module="torchvision.*")

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动动漫图片高清修复API服务...")
    
    # 创建必要目录
    settings.create_directories()
    
    # 加载AI模型
    try:
        model_manager.load_model()
        logger.info("✅ AI模型加载成功")
    except Exception as e:
        logger.error(f"❌ AI模型加载失败: {e}")
        # 根据需要决定是否继续启动服务
    
    # 记录启动信息
    logger.info(f"📍 本地访问: http://localhost:{settings.port}")
    logger.info(f"📖 API文档: http://localhost:{settings.port}/docs")
    logger.info(f"🔍 交互式文档: http://localhost:{settings.port}/redoc")
    
    yield
    
    # 关闭时执行
    logger.info("🛑 正在关闭API服务...")
    model_manager.unload_model()
    logger.info("✅ API服务已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="基于Real-ESRGAN的高性能动漫图片四倍放大和高清修复服务",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """处理自定义API异常"""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error_code=exc.error_code,
            error_message=exc.message,
            timestamp=datetime.now().isoformat()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            error_message="服务器内部错误",
            timestamp=datetime.now().isoformat()
        ).dict()
    )


# 根路径
@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "model_loaded": model_manager.is_loaded,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


# 导入路由
from .api.v1 import health, system, upscale

# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])
app.include_router(system.router, prefix="/api/v1", tags=["系统状态"])
app.include_router(upscale.router, prefix="/api/v1", tags=["图片处理"])

# 为了兼容旧版本，保留根级别的路由
app.include_router(health.router, tags=["健康检查"])
app.include_router(system.router, tags=["系统状态"])
app.include_router(upscale.router, tags=["图片处理"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    ) 