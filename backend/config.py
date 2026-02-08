from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/student_system"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # AI/LLM
    LLM_API_KEY: str = ""
    LLM_API_URL: str = ""
    OCR_API_URL: str = ""
    
    # Alibaba Cloud Qwen (OpenAI Compatible Mode)
    DASHSCOPE_API_KEY: str = ""
    QWEN_API_KEY: str = ""
    QWEN_MODEL_NAME: str = "qwen-plus"
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_VL_MODEL: str = "qwen-vl-max"  # Using MAX model for better accuracy
    
    # Feishu Integration
    FEISHU_APP_ID: str = ""
    FEISHU_APP_SECRET: str = ""
    FEISHU_ENCRYPT_KEY: str = "feishu-secret-encryption-key-change-in-production"  # 用于加密存储App Secret
    
    # CORS
    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from comma-separated string or list"""
        if isinstance(v, str):
            # If wildcard is specified, return it directly as a list with single element
            if v.strip() == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
