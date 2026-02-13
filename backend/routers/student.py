from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
import httpx
from datetime import datetime, timedelta
from database import get_db
from schemas import (
    OCRResponse, AchievementCreate, AchievementResponse,
    ChatRequest, ChatResponse, PersonaResponse
)
from utils import success_response, error_response
from models import (
    SysStudent, BizAchievement, AchievementStatus,
    AiChatSession, AiChatMessage, MessageRole, SysTeacher
)
from dependencies import require_student
from config import settings

router = APIRouter(prefix="/api/v1/student", tags=["Student"])


@router.post("/ocr/recognize")
async def ocr_recognize(
    file: UploadFile = File(...),
    student: SysStudent = Depends(require_student)
):
    """
    Certificate recognition with permanent storage (Step 1 of 2)
    - Accepts certificate image
    - Saves file permanently to student's directory
    - Calls AI vision model (qwen-vl-max) for extraction
    - Returns structured data + file URL
    - User can then confirm and submit achievement in Step 2
    """
    from services.file_manager import file_manager
    from services.certificate_recognition_openai import certificate_recognition_service_openai
    
    try:
        # Step 1: Save certificate permanently
        file_info = await file_manager.save_certificate_permanent(file, student.id)
        
        # Step 2: Recognize certificate using AI (OpenAI-compatible API)
        recognition_result = certificate_recognition_service_openai.recognize_certificate(
            file_info["file_path"]
        )
        
        # Step 3: Validate result
        validated_result = certificate_recognition_service_openai.validate_recognition_result(
            recognition_result
        )
        
        # Step 4: Return result
        if validated_result.get("success"):
            data = validated_result.get("data", {})
            
            return success_response(data={
                "recognized_data": {
                    # Basic fields
                    "title": data.get("certificate_name"),
                    "date": data.get("issue_date"),
                    "issuer": data.get("issuing_organization"),
                    "suggested_type": data.get("category"),
                    "award_level": data.get("award_level"),  # 奖项级别（国家级、省部级等）
                    "award": data.get("award"),  # 具体奖项（一等奖、二等奖等）
                    "certificate_number": data.get("certificate_number"),
                    "recipient_name": data.get("recipient_name"),
                    
                    # New enhanced fields
                    "project_name": data.get("project_name"),
                    "team_members": data.get("team_members", []),
                    "advisors": data.get("advisors", []),
                    "additional_info": data.get("additional_info"),
                    
                    # Confidence scores
                    "recognition_confidence": data.get("recognition_confidence", {})
                },
                "file_url": file_info["file_url"],
                "file_info": {
                    "filename": file_info["filename"],
                    "original_filename": file_info["original_filename"],
                    "size_bytes": file_info["size_bytes"]
                },
                "ai_metadata": {
                    "model_used": data.get("model_used"),
                    "recognition_time": data.get("recognition_time"),
                    "confidence": data.get("confidence")
                },
                "usage": validated_result.get("usage", {})
            })
        else:
            # Recognition failed, but file is still saved
            return error_response(
                msg=f"Certificate saved but recognition failed: {validated_result.get('error')}",
                code=500,
                data={
                    "file_url": file_info["file_url"],
                    "recognized_data": None
                }
            )
            
    except HTTPException as e:
        raise e
    except Exception as e:
        return error_response(msg=f"Error processing certificate: {str(e)}", code=500)


@router.post("/achievements")
async def create_achievement(
    achievement: AchievementCreate,
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Submit achievement (Step 2 of 2)
    - Creates new achievement record
    - Status defaults to 'pending'
    - Must select existing teacher
    - If evidence_url is provided, verifies student has access to that certificate
    """
    from services.file_manager import file_manager
    
    # Validate teacher exists
    teacher = db.query(SysTeacher).filter(SysTeacher.id == achievement.teacher_id).first()
    if not teacher:
        return error_response(msg="Teacher not found", code=404)
    
    # If evidence_url is provided, verify access
    if achievement.evidence_url:
        if not file_manager.verify_certificate_access(
            achievement.evidence_url, 
            student.id, 
            is_admin=False
        ):
            return error_response(
                msg="Access denied: You can only use your own certificates",
                code=403
            )
    
    # Create achievement
    new_achievement = BizAchievement(
        student_id=student.id,
        teacher_id=achievement.teacher_id,
        title=achievement.title,
        type=achievement.type,
        content_json=achievement.content_json,
        evidence_url=achievement.evidence_url,
        status=AchievementStatus.PENDING
    )
    
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    
    return success_response(data={"id": new_achievement.id}, msg="Achievement submitted successfully")


@router.get("/achievements")
async def get_my_achievements(
    status: Optional[str] = Query(None),
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get my achievements
    - Returns only current student's achievements
    - Optional filter by status
    - Excludes soft-deleted achievements by default
    """
    query = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id,
        BizAchievement.is_deleted == False  # 排除已删除的成果
    )
    
    if status:
        try:
            status_enum = AchievementStatus(status)
            query = query.filter(BizAchievement.status == status_enum)
        except ValueError:
            return error_response(msg="Invalid status value", code=400)
    
    achievements = query.order_by(BizAchievement.created_at.desc()).all()
    
    achievement_list = []
    for ach in achievements:
        achievement_list.append({
            "id": ach.id,
            "title": ach.title,
            "type": ach.type,
            "content_json": ach.content_json,
            "evidence_url": ach.evidence_url,
            "status": ach.status.value,
            "audit_comment": ach.audit_comment,
            "created_at": ach.created_at.isoformat(),
            "teacher_name": ach.teacher.name if ach.teacher else None
        })
    
    return success_response(data=achievement_list)


@router.get("/achievements/{achievement_id}")
async def get_achievement_detail(
    achievement_id: int,
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get achievement detail by ID
    - Returns detailed information of a specific achievement
    - Verifies the achievement belongs to the current student
    - Includes teacher information
    """
    # Query achievement and verify ownership
    achievement = db.query(BizAchievement).filter(
        BizAchievement.id == achievement_id,
        BizAchievement.student_id == student.id
    ).first()
    
    if not achievement:
        return error_response(msg="Achievement not found", code=404)
    
    # Build detailed response
    achievement_detail = {
        "id": achievement.id,
        "title": achievement.title,
        "type": achievement.type,
        "type_id": achievement.type,  # For compatibility
        "description": achievement.content_json.get("description", "") if achievement.content_json else "",
        "content_json": achievement.content_json,
        "evidence_url": achievement.evidence_url,
        "status": achievement.status.value if hasattr(achievement.status, 'value') else achievement.status,
        "audit_comment": achievement.audit_comment,
        "created_at": achievement.created_at.isoformat(),
        "awardedAt": achievement.content_json.get("date", achievement.created_at.isoformat()) if achievement.content_json else achievement.created_at.isoformat(),
        "year": achievement.content_json.get("year", "") if achievement.content_json else "",
        "level": achievement.content_json.get("award_level", "") if achievement.content_json else "",
    }
    
    # Add teacher information if exists
    if achievement.teacher:
        achievement_detail["teacher"] = {
            "id": achievement.teacher.id,
            "name": achievement.teacher.name,
            "contactEmail": getattr(achievement.teacher, 'email', ''),
            "contactPhone": getattr(achievement.teacher, 'phone', ''),
            "research_tent": getattr(achievement.teacher, 'research_direction', '')
        }
    else:
        achievement_detail["teacher"] = None
    
    return success_response(data=achievement_detail)


@router.delete("/achievements/{achievement_id}")
async def delete_achievement(
    achievement_id: int,
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Delete achievement (soft delete)
    - Verifies the achievement belongs to the current student
    - Marks achievement as deleted instead of hard deleting
    """
    # Query achievement and verify ownership
    achievement = db.query(BizAchievement).filter(
        BizAchievement.id == achievement_id,
        BizAchievement.student_id == student.id
    ).first()
    
    if not achievement:
        return error_response(msg="Achievement not found", code=404)
    
    # Soft delete: mark as deleted
    achievement.is_deleted = True
    db.commit()
    
    return success_response(msg="Achievement deleted successfully")


@router.get("/certificates")
async def get_my_certificates(
    student: SysStudent = Depends(require_student)
):
    """
    Get list of my certificates
    - Returns all certificate files uploaded by current student
    - Files are stored in student-specific directory
    """
    from services.file_manager import file_manager
    
    certificates = file_manager.get_student_certificates(student.id)
    
    return success_response(data={
        "certificates": certificates,
        "total": len(certificates)
    })


@router.get("/persona")
async def get_persona(
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get student persona
    - Checks cache validity
    - Regenerates if expired (async task in production)
    - Returns AI-generated persona data
    """
    # Check if persona cache exists and is valid
    # For demo, consider cache valid for 7 days
    needs_regeneration = False
    
    if not student.persona_cache:
        needs_regeneration = True
    
    # TODO: Implement actual persona generation using LLM
    # This would analyze approved achievements and chat history
    # For now, return cached data or mock data
    
    if needs_regeneration:
        # Mock persona generation
        # In production, this would be an async task
        persona_data = {
            "strengths": ["数学建模", "创新能力"],
            "achievements_summary": "参与多项竞赛并获奖",
            "suggested_improvements": ["加强英语能力", "拓展跨学科知识"],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        student.persona_cache = persona_data
        db.commit()
    else:
        persona_data = student.persona_cache
    
    return success_response(data=persona_data)


@router.post("/ai/chat")
async def ai_chat(
    chat_req: ChatRequest,
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    AI chat with context management
    - Backend manages conversation history
    - Implements RAG with student achievements
    - Stores messages in database
    - Uses real LLM API (Alibaba Cloud Qwen)
    """
    from services.ai_chat_service import ai_chat_service
    
    # Get or create session
    session_id = chat_req.session_id
    
    if not session_id:
        # Create new session
        session_id = str(uuid.uuid4())
        new_session = AiChatSession(
            id=session_id,
            student_id=student.id,
            title=chat_req.message[:50]  # Use first 50 chars as title
        )
        db.add(new_session)
        db.commit()
    else:
        # Validate session belongs to student
        session = db.query(AiChatSession).filter(
            AiChatSession.id == session_id,
            AiChatSession.student_id == student.id
        ).first()
        
        if not session:
            return error_response(msg="Session not found", code=404)
    
    # Store user message
    user_message = AiChatMessage(
        session_id=session_id,
        role=MessageRole.USER,
        content=chat_req.message
    )
    db.add(user_message)
    db.commit()
    
    # Retrieve chat history (last 10 messages for context)
    history_messages = db.query(AiChatMessage).filter(
        AiChatMessage.session_id == session_id
    ).order_by(AiChatMessage.created_at.desc()).limit(10).all()
    history_messages.reverse()  # Oldest first
    
    # Format history for LLM (exclude current message)
    chat_history = [
        {
            "role": msg.role.value,
            "content": msg.content
        }
        for msg in history_messages[:-1]
    ] if len(history_messages) > 1 else []
    
    # Retrieve all achievements for comprehensive AI analysis (not just approved)
    # 查询所有状态的成果，让AI能够全面分析学生情况
    achievements = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id,
        BizAchievement.is_deleted == False  # 排除已删除的
    ).order_by(BizAchievement.created_at.desc()).all()  # 移除20条限制，获取所有成果
    
    # Count achievements by status for statistics
    approved_count = sum(1 for ach in achievements if ach.status == AchievementStatus.APPROVED)
    pending_count = sum(1 for ach in achievements if ach.status == AchievementStatus.PENDING)
    rejected_count = sum(1 for ach in achievements if ach.status == AchievementStatus.REJECTED)
    
    # Build student context with complete achievement data
    student_context = {
        "name": student.name,
        "major": student.major,
        "class_name": getattr(student, 'class_name', None),
        "achievements": [
            {
                # 基本信息
                "id": ach.id,
                "title": ach.title,
                "type": ach.type,
                "status": ach.status.value,
                
                # 详细内容（OCR识别的结构化数据）
                "content_json": ach.content_json,
                
                # 证书相关
                "evidence_url": ach.evidence_url,
                "feishu_attachment_token": ach.feishu_attachment_token,
                
                # 审核信息
                "audit_comment": ach.audit_comment,
                
                # 时间信息
                "created_at": ach.created_at.isoformat() if ach.created_at else None,
                
                # 教师信息（如果需要）
                "teacher_name": ach.teacher.name if ach.teacher else None,
                "teacher_title": ach.teacher.title if ach.teacher else None,
                "teacher_department": ach.teacher.department if ach.teacher else None,
            }
            for ach in achievements
        ],
        "statistics": {
            "total_achievements": len(achievements),
            "approved_achievements": approved_count,
            "pending_achievements": pending_count,
            "rejected_achievements": rejected_count,
            "approval_rate": round(approved_count / len(achievements) * 100, 2) if len(achievements) > 0 else 0
        }
    }
    
    # Call AI chat service
    ai_result = ai_chat_service.chat(
        user_message=chat_req.message,
        student_context=student_context,
        chat_history=chat_history,
        temperature=0.7,
        max_tokens=800
    )
    
    # Handle AI service response
    if not ai_result.get("success"):
        # Log the error for debugging
        error_msg = ai_result.get("error", "Unknown error")
        print(f"❌ AI Chat Service Error: {error_msg}")
        print(f"Full AI Result: {ai_result}")
        # Fallback response if AI service fails
        ai_response = "抱歉，AI助手暂时无法回复。请检查网络连接或稍后再试。"
    else:
        ai_response = ai_result.get("message", "抱歉，暂时无法生成回复。")
    
    # Store AI response
    assistant_message = AiChatMessage(
        session_id=session_id,
        role=MessageRole.ASSISTANT,
        content=ai_response
    )
    db.add(assistant_message)
    
    # Update session timestamp
    session = db.query(AiChatSession).filter(AiChatSession.id == session_id).first()
    session.updated_at = datetime.utcnow()
    
    db.commit()
    
    return success_response(data={
        "session_id": session_id,
        "message": ai_response,
        "usage": ai_result.get("usage") if ai_result.get("success") else None
    })


@router.get("/me")
async def get_student_me(
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    获取当前登录学生的基本信息
    """
    user = student.user
    
    return success_response(data={
        "id": student.id,
        "student_id": student.student_number,  # Corrected from student_id to student_number
        "name": student.name,
        "class_name": getattr(student, 'class_name', None),  # Handle potential missing field if model updated
        "major": student.major,
        "email": getattr(student, 'email', None),
        "phone": getattr(student, 'phone', None),
        "user_id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "role": user.role.value
    })


@router.get("/profile")
async def get_student_profile(
    student: SysStudent = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    获取学生的详细档案信息
    包含基本信息、成果统计、证书统计等
    """
    user = student.user
    
    # 统计成果数量
    total_achievements = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id
    ).count()
    
    approved_achievements = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id,
        BizAchievement.status == AchievementStatus.APPROVED
    ).count()
    
    pending_achievements = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id,
        BizAchievement.status == AchievementStatus.PENDING
    ).count()
    
    # 获取最近的成果
    recent_achievements = db.query(BizAchievement).filter(
        BizAchievement.student_id == student.id
    ).order_by(BizAchievement.created_at.desc()).limit(5).all()
    
    return success_response(data={
        "basic_info": {
            "id": student.id,
            "student_id": student.student_number,  # Corrected from student_id to student_number
            "name": student.name,
            "class_name": getattr(student, "class_name", None),
            "major": student.major,
            "email": getattr(student, "email", None),
            "phone": getattr(student, "phone", None),
            "avatar_url": user.avatar_url
        },
        "statistics": {
            "total_achievements": total_achievements,
            "approved_achievements": approved_achievements,
            "pending_achievements": pending_achievements,
            "approval_rate": round(approved_achievements / total_achievements * 100, 2) if total_achievements > 0 else 0
        },
        "recent_achievements": [
            {
                "id": ach.id,
                "title": ach.title,
                "type": ach.type,
                "status": ach.status.value,
                "created_at": ach.created_at.isoformat()
            }
            for ach in recent_achievements
        ]
    })

