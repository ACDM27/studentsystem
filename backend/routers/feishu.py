"""
Feishu Integration Router
飞书多维表格集成API路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import logging

from database import get_db
from dependencies import require_admin, require_student
from models import SysUser, SysStudent, BizAchievement, AchievementStatus, FeishuConfig, FeishuFieldMapping, FeishuImportLog
from schemas_feishu import (
    FeishuConfigCreate, FeishuConfigResponse,
    FeishuImportRequest, PreviewResponse, ImportResponse,
    FeishuTablesResponse, ImportLogResponse,
    QuickImportPreviewRequest, QuickImportPreviewResponse,
    PreviewRecord, ValidationError, ImportResult
)
from utils import success_response, error_response
from config import settings
from services.feishu import FeishuClient, DataMapper, AttachmentDownloader

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/feishu", tags=["Feishu Integration"])


# ==================== 配置管理 ====================

@router.post("/config")
async def save_feishu_config(
    config: FeishuConfigCreate,
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    保存飞书应用配置（管理员）
    """
    try:
        # 检查是否已存在配置
        existing_config = db.query(FeishuConfig).filter(
            FeishuConfig.status == "active"
        ).first()
        
        if existing_config:
            # 更新现有配置
            existing_config.app_id = config.app_id
            existing_config.app_secret = config.app_secret  # TODO: 加密存储
            existing_config.updated_at = datetime.utcnow()
        else:
            # 创建新配置
            new_config = FeishuConfig(
                app_id=config.app_id,
                app_secret=config.app_secret,  # TODO: 加密存储
                status="active"
            )
            db.add(new_config)
        
        db.commit()
        
        return success_response(msg="飞书配置保存成功")
        
    except Exception as e:
        logger.error(f"保存飞书配置失败: {str(e)}")
        db.rollback()
        return error_response(msg=f"保存配置失败: {str(e)}", code=500)


@router.get("/config")
async def get_feishu_config(
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    获取当前飞书配置（管理员）
    """
    config = db.query(FeishuConfig).filter(
        FeishuConfig.status == "active"
    ).first()
    
    if not config:
        return error_response(msg="未配置飞书应用", code=404)
    
    return success_response(data={
        "id": config.id,
        "app_id": config.app_id,
        "app_secret": "******",  # 脱敏
        "status": config.status,
        "created_at": config.created_at.isoformat(),
        "updated_at": config.updated_at.isoformat()
    })


@router.post("/test-connection")
async def test_feishu_connection(
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    测试飞书连接（管理员）
    """
    config = db.query(FeishuConfig).filter(FeishuConfig.status == "active").first()
    
    if not config:
        return error_response(msg="请先配置飞书应用", code=400)
    
    try:
        client = FeishuClient(config.app_id, config.app_secret)
        is_connected = await client.test_connection()
        
        if is_connected:
            return success_response(msg="飞书连接测试成功")
        else:
            return error_response(msg="飞书连接失败，请检查App ID和Secret", code=500)
            
    except Exception as e:
        logger.error(f"飞书连接测试失败: {str(e)}")
        return error_response(msg=f"连接测试失败: {str(e)}", code=500)


# ==================== 表格操作 ====================

@router.get("/tables/{app_token}")
async def list_feishu_tables(
    app_token: str,
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    列出飞书多维表格中的所有数据表（管理员）
    """
    config = db.query(FeishuConfig).filter(FeishuConfig.status == "active").first()
    
    if not config:
        return error_response(msg="请先配置飞书应用", code=400)
    
    try:
        client = FeishuClient(config.app_id, config.app_secret)
        tables = await client.list_tables(app_token)
        
        return success_response(data={"tables": tables})
        
    except Exception as e:
        logger.error(f"获取表格列表失败: {str(e)}")
        return error_response(msg=f"获取表格失败: {str(e)}", code=500)


# ==================== 数据预览和导入 ====================

@router.post("/preview")
async def preview_import_data(
    request: FeishuImportRequest,
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    预览导入数据（管理员）
    """
    config = db.query(FeishuConfig).filter(FeishuConfig.status == "active").first()
    
    if not config:
        return error_response(msg="请先配置飞书应用", code=400)
    
    try:
        # 初始化飞书客户端
        client = FeishuClient(config.app_id, config.app_secret)
        
        # 获取表格记录
        records = await client.get_table_records(
            request.app_token,
            request.table_id
        )
        
        # 限制预览数量
        if request.preview_limit:
            records = records[:request.preview_limit]
        
        # 获取或创建默认映射
        mappings = _get_or_create_default_mappings(db, config.id)
        
        # 数据映射和验证
        mapper = DataMapper(mappings, db)
        preview_results = []
        
        for idx, record in enumerate(records, 1):
            fields = record.get("fields", {})
            transformed, errors = mapper.transform_record(fields)
            
            preview_results.append({
                "row_number": idx,
                "original_data": fields,
                "transformed_data": transformed if not errors else {},
                "is_valid": len(errors) == 0,
                "validation_errors": [
                    {"field": "general", "message": err} for err in errors
                ]
            })
        
        valid_count = sum(1 for r in preview_results if r["is_valid"])
        
        return success_response(data={
            "total": len(preview_results),
            "valid": valid_count,
            "invalid": len(preview_results) - valid_count,
            "records": preview_results
        })
        
    except Exception as e:
        logger.error(f"预览数据失败: {str(e)}")
        return error_response(msg=f"预览失败: {str(e)}", code=500)


@router.post("/import")
async def execute_import(
    request: FeishuImportRequest,
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    执行导入（管理员）
    """
    config = db.query(FeishuConfig).filter(FeishuConfig.status == "active").first()
    
    if not config:
        return error_response(msg="请先配置飞书应用", code=400)
    
    start_time = datetime.now()
    import_results = []
    
    try:
        # 初始化服务
        client = FeishuClient(config.app_id, config.app_secret)
        downloader = AttachmentDownloader(client)
        
        # 获取记录
        records = await client.get_table_records(request.app_token, request.table_id)
        
        # 获取映射配置
        mappings = _get_or_create_default_mappings(db, config.id)
        mapper = DataMapper(mappings, db)
        
        success_count = 0
        failed_count = 0
        
        for idx, record in enumerate(records, 1):
            try:
                fields = record.get("fields", {})
                transformed, errors = mapper.transform_record(fields)
                
                # 跳过无效记录
                if errors and request.skip_invalid:
                    import_results.append({
                        "row": idx,
                        "status": "failed",
                        "error": "; ".join(errors)
                    })
                    failed_count += 1
                    continue
                
                # 处理附件
                evidence_url = None
                feishu_token = None
                
                attachments = fields.get("证书附件", [])
                if attachments and len(attachments) > 0:
                    file_token = attachments[0].get("file_token")
                    if file_token:
                        local_url, success, retry_token = await downloader.download_and_save(
                            file_token,
                            transformed["student_id"]
                        )
                        if success:
                            evidence_url = local_url
                        else:
                            feishu_token = retry_token
                
                # 创建成果记录
                new_achievement = BizAchievement(
                    student_id=transformed["student_id"],
                    teacher_id=transformed["teacher_id"],
                    title=transformed["title"],
                    type=transformed.get("type", ""),
                    content_json={
                        "date": transformed.get("date"),
                        "award_level": transformed.get("level"),
                        "award": transformed.get("award"),
                        "issuer": transformed.get("issuer"),
                        "certificate_number": transformed.get("certificate_number")
                    },
                    evidence_url=evidence_url,
                    feishu_attachment_token=feishu_token,
                    status=AchievementStatus.PENDING
                )
                
                db.add(new_achievement)
                db.flush()  # 获取ID
                
                import_results.append({
                    "row": idx,
                    "status": "success",
                    "achievement_id": new_achievement.id
                })
                success_count += 1
                
            except Exception as e:
                logger.error(f"导入第{idx}行失败: {str(e)}")
                import_results.append({
                    "row": idx,
                    "status": "failed",
                    "error": str(e)
                })
                failed_count += 1
        
        # 记录导入日志
        duration = (datetime.now() - start_time).seconds
        import_log = FeishuImportLog(
            operator_id=admin.id,
            operator_role="admin",
            app_token=request.app_token,
            table_id=request.table_id,
            total_records=len(records),
            success_count=success_count,
            failed_count=failed_count,
            error_details=[r for r in import_results if r["status"] == "failed"],
            import_duration_seconds=duration
        )
        db.add(import_log)
        
        db.commit()
        
        return success_response(data={
            "total": len(records),
            "imported": success_count,
            "failed": failed_count,
            "details": import_results,
            "import_log_id": import_log.id
        })
        
    except Exception as e:
        logger.error(f"执行导入失败: {str(e)}")
        db.rollback()
        return error_response(msg=f"导入失败: {str(e)}", code=500)


# ==================== 导入历史 ====================

@router.get("/import-history")
async def get_import_history(
    page: int = 1,
    page_size: int = 20,
    admin: SysUser = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    获取导入历史（管理员）
    """
    try:
        offset = (page - 1) * page_size
        
        logs = db.query(FeishuImportLog).order_by(
            FeishuImportLog.created_at.desc()
        ).offset(offset).limit(page_size).all()
        
        total = db.query(FeishuImportLog).count()
        
        return success_response(data={
            "logs": [
                {
                    "id": log.id,
                    "operator_id": log.operator_id,
                    "operator_role": log.operator_role,
                    "total_records": log.total_records,
                    "success_count": log.success_count,
                    "failed_count": log.failed_count,
                    "import_duration_seconds": log.import_duration_seconds,
                    "created_at": log.created_at.isoformat()
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "page_size": page_size
        })
        
    except Exception as e:
        logger.error(f"获取导入历史失败: {str(e)}")
        return error_response(msg=f"获取历史失败: {str(e)}", code=500)


# ==================== 学生端快捷导入 ====================

@router.post("/student/quick-preview")
async def student_quick_preview(
    request: QuickImportPreviewRequest,
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    学生快捷预览（自动过滤当前学生数据）
    """
    config = db.query(FeishuConfig).filter(FeishuConfig.status == "active").first()
    
    if not config:
        return error_response(msg="飞书功能未配置", code=400)
    
    try:
        client = FeishuClient(config.app_id, config.app_secret)
        all_records = await client.get_table_records(request.app_token, request.table_id)
        
        # 筛选当前学生的记录
        student_records = []
        for record in all_records:
            fields = record.get("fields", {})
            record_student_name = fields.get("学生姓名", "").replace(" ", "")
            
            if record_student_name == student.name.replace(" ", ""):
                student_records.append(record)
        
        # 转换数据
        mappings = _get_or_create_default_mappings(db, config.id)
        mapper = DataMapper(mappings, db)
        
        preview_records = []
        for record in student_records:
            fields = record.get("fields", {})
            transformed, errors = mapper.transform_record(fields)
            
            attachments = fields.get("证书附件", [])
            certificate_url = attachments[0].get("file_token") if attachments else None
            
            preview_records.append({
                "title": transformed.get("title", ""),
                "date": transformed.get("date"),
                "type": transformed.get("type"),
                "level": transformed.get("level"),
                "award": transformed.get("award"),
                "teacherName": fields.get("指导教师", ""),
                "teacherId": transformed.get("teacher_id"),
                "certificateUrl": certificate_url,
                "validationErrors": errors,
                "isValid": len(errors) == 0
            })
        
        return success_response(data={
            "records": preview_records,
            "total": len(preview_records)
        })
        
    except Exception as e:
        logger.error(f"快捷预览失败: {str(e)}")
        return error_response(msg=f"预览失败: {str(e)}", code=500)


# ==================== 辅助函数 ====================

def _get_or_create_default_mappings(db: Session, config_id: int) -> List[FeishuFieldMapping]:
    """获取或创建默认字段映射"""
    from services.feishu.data_mapper import create_default_mappings
    
    # 检查是否已存在
    existing = db.query(FeishuFieldMapping).filter(
        FeishuFieldMapping.config_id == config_id
    ).all()
    
    if existing:
        return existing
    
    # 创建默认映射
    default_configs = create_default_mappings()
    mappings = []
    
    for cfg in default_configs:
        mapping = FeishuFieldMapping(
            config_id=config_id,
            **cfg
        )
        db.add(mapping)
        mappings.append(mapping)
    
    db.commit()
    return mappings
