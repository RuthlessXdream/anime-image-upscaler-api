"""
图片处理API路由
"""

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from ...config import settings
from ...core.model_manager import model_manager
from ...models.response import UpscaleResponse
from ...utils.exceptions import FileUploadError, ImageProcessingError

router = APIRouter()


@router.post("/upscale", response_model=UpscaleResponse)
async def upscale_image(file: UploadFile = File(...)):
    """图片放大处理"""
    
    # 检查模型是否已加载
    if not model_manager.is_loaded:
        raise HTTPException(status_code=503, detail="AI模型未加载")
    
    # 检查文件类型
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.allowed_extensions:
        raise FileUploadError(f"不支持的文件格式: {file_ext}")
    
    # 检查文件大小
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.max_file_size:
        raise FileUploadError(f"文件大小超出限制: {file_size} > {settings.max_file_size}")
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    try:
        # 保存上传的文件
        input_path = settings.upload_dir / f"{task_id}_input{file_ext}"
        with open(input_path, "wb") as f:
            f.write(content)
        
        # TODO: 这里应该使用异步任务处理，现在先简化处理
        # 处理图片
        upsampler = model_manager.upsampler
        if upsampler is None:
            raise ImageProcessingError("AI模型未初始化")
        
        # 读取并处理图片
        import cv2
        img = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
        if img is None:
            raise ImageProcessingError("无法读取图片文件")
        
        # AI处理
        output, _ = upsampler.enhance(img, outscale=settings.model_scale)
        
        # 保存处理结果
        output_path = settings.output_dir / f"{task_id}_output{file_ext}"
        cv2.imwrite(str(output_path), output)
        
        return UpscaleResponse(
            task_id=task_id,
            status="completed",
            message="图片处理完成",
            download_url=f"/download/{task_id}",
            estimated_time=None
        )
        
    except Exception as e:
        raise ImageProcessingError(f"图片处理失败: {str(e)}")


@router.get("/download/{task_id}")
async def download_result(task_id: str):
    """下载处理结果"""
    
    # 查找输出文件
    output_files = list(settings.output_dir.glob(f"{task_id}_output.*"))
    
    if not output_files:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    output_file = output_files[0]
    
    return FileResponse(
        path=str(output_file),
        media_type="application/octet-stream",
        filename=f"upscaled_{task_id}{output_file.suffix}"
    )


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """获取任务状态 - 简化版本"""
    
    # 检查输出文件是否存在
    output_files = list(settings.output_dir.glob(f"{task_id}_output.*"))
    
    if output_files:
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100.0,
            "message": "处理完成",
            "download_url": f"/download/{task_id}"
        }
    else:
        return {
            "task_id": task_id,
            "status": "not_found",
            "progress": 0.0,
            "message": "任务不存在"
        } 