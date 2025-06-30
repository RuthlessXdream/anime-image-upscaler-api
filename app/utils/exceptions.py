"""
自定义异常类
"""


class BaseAPIException(Exception):
    """API基础异常类"""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ModelLoadError(BaseAPIException):
    """模型加载错误"""
    
    def __init__(self, message: str):
        super().__init__(message, "MODEL_LOAD_ERROR")


class ImageProcessingError(BaseAPIException):
    """图片处理错误"""
    
    def __init__(self, message: str):
        super().__init__(message, "IMAGE_PROCESSING_ERROR")


class FileUploadError(BaseAPIException):
    """文件上传错误"""
    
    def __init__(self, message: str):
        super().__init__(message, "FILE_UPLOAD_ERROR")


class TaskNotFoundError(BaseAPIException):
    """任务未找到错误"""
    
    def __init__(self, task_id: str):
        super().__init__(f"任务不存在: {task_id}", "TASK_NOT_FOUND")


class GPUMemoryError(BaseAPIException):
    """GPU内存错误"""
    
    def __init__(self, message: str):
        super().__init__(message, "GPU_MEMORY_ERROR")


class ValidationError(BaseAPIException):
    """数据验证错误"""
    
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR") 