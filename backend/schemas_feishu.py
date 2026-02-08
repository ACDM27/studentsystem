"""
Feishu Integration Schemas
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== 配置相关 ====================

class FeishuConfigCreate(BaseModel):
    """创建飞书配置请求"""
    app_id: str = Field(..., min_length=10, max_length=100, description="飞书应用ID")
    app_secret: str = Field(..., min_length=10, max_length=500, description="飞书应用密钥")


class FeishuConfigResponse(BaseModel):
    """飞书配置响应"""
    id: int
    app_id: str
    app_secret: str = "******"  # 脱敏显示
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 字段映射相关 ====================

class TransformRule(BaseModel):
    """字段转换规则"""
    type: str = Field(..., description="转换类型: enum_mapping, teacher_name_to_id, date_parse 等")
    mapping: Optional[Dict[str, Any]] = Field(None, description="枚举映射字典")
    match_mode: Optional[str] = Field("exact", description="匹配模式: exact, fuzzy")
    date_format: Optional[str] = Field(None, description="日期格式")


class FieldMappingCreate(BaseModel):
    """创建字段映射"""
    name: str = Field(..., max_length=100, description="映射模板名称")
    feishu_field_name: str = Field(..., description="飞书字段名")
    db_field_name: str = Field(..., description="数据库字段名")
    transform_rule: Optional[TransformRule] = None
    is_required: bool = Field(False, description="是否必填")
    display_order: int = Field(0, description="显示顺序")


class FieldMappingResponse(BaseModel):
    """字段映射响应"""
    id: int
    config_id: int
    name: str
    feishu_field_name: str
    db_field_name: str
    transform_rule: Optional[Dict[str, Any]] = None
    is_required: int
    display_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 导入相关 ====================

class FeishuImportRequest(BaseModel):
    """飞书导入请求"""
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="数据表table_id")
    mapping_id: Optional[int] = Field(None, description="字段映射配置ID")
    skip_invalid: bool = Field(True, description="是否跳过无效记录")
    preview_limit: Optional[int] = Field(None, description="预览限制数量")


class QuickImportPreviewRequest(BaseModel):
    """学生快捷导入请求"""
    app_token: str
    table_id: str
    student_name: str = Field(..., description="学生姓名，用于过滤数据")


class ValidationError(BaseModel):
    """验证错误"""
    field: str = Field(..., description="错误字段")
    message: str = Field(..., description="错误信息")


class PreviewRecord(BaseModel):
    """预览记录"""
    row_number: int
    original_data: Dict[str, Any]
    transformed_data: Optional[Dict[str, Any]] = None
    is_valid: bool
    validation_errors: List[ValidationError] = []


class PreviewResponse(BaseModel):
    """预览响应"""
    total: int
    valid: int
    invalid: int
    records: List[PreviewRecord]


class ImportResult(BaseModel):
    """导入结果"""
    row: int
    status: str  # success, failed
    error: Optional[str] = None
    achievement_id: Optional[int] = None


class ImportResponse(BaseModel):
    """导入响应"""
    total: int
    imported: int
    failed: int
    details: List[ImportResult]
    import_log_id: int


# ==================== 导入日志相关 ====================

class ImportLogResponse(BaseModel):
    """导入日志响应"""
    id: int
    operator_id: int
    operator_role: str
    app_token: Optional[str]
    table_id: Optional[str]
    table_name: Optional[str]
    total_records: int
    success_count: int
    failed_count: int
    error_details: Optional[List[Dict[str, Any]]] = None
    import_duration_seconds: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== 飞书表格相关 ====================

class FeishuTable(BaseModel):
    """飞书表格信息"""
    table_id: str
    name: str
    record_count: Optional[int] = 0


class FeishuTablesResponse(BaseModel):
    """飞书表格列表响应"""
    tables: List[FeishuTable]


# ==================== 快捷导入预览 ====================

class QuickImportPreviewRecord(BaseModel):
    """快捷导入预览记录"""
    title: str
    date: Optional[str] = None
    type: Optional[str] = None
    level: Optional[str] = None
    award: Optional[str] = None
    teacherName: Optional[str] = None
    teacherId: Optional[int] = None
    certificateUrl: Optional[str] = None
    validationErrors: List[str] = []
    isValid: bool


class QuickImportPreviewResponse(BaseModel):
    """快捷导入预览响应"""
    records: List[QuickImportPreviewRecord]
    total: int


# ==================== 批量映射配置 ====================

class BulkMappingCreate(BaseModel):
    """批量创建映射配置"""
    config_id: int
    template_name: str = Field(..., description="模板名称")
    mappings: List[FieldMappingCreate]


class LinkParseRequest(BaseModel):
    """链接解析请求"""
    feishu_link: str = Field(..., description="飞书表格链接")
    
    @validator('feishu_link')
    def validate_feishu_link(cls, v):
        if 'feishu.cn' not in v and 'lark' not in v:
            raise ValueError('无效的飞书链接')
        return v


class LinkParseResponse(BaseModel):
    """链接解析响应"""
    app_token: str
    table_id: str
    view_id: Optional[str] = None

