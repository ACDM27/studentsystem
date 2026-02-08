"""
Activities Router - 校园活动管理API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import get_db
from utils import success_response, error_response
from dependencies import require_student, require_admin
from models import SysStudent, SysUser

router = APIRouter(prefix="/api/v1/activities", tags=["Activities"])


@router.get("")
async def get_activities(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_student)
):
    """
    获取活动列表（学生端）
    支持分页和状态筛选
    """
    # Mock数据 - 实际应该从数据库查询
    # TODO: 创建Activity模型和数据库表
    
    activities = [
        {
            "id": 1,
            "title": "编程马拉松大赛",
            "description": "为期48小时的编程挑战赛，团队协作完成创新项目",
            "category": "竞赛",
            "status": "报名中",
            "start_time": "2024-03-15T09:00:00",
            "end_time": "2024-03-17T18:00:00",
            "location": "科技楼101",
            "max_participants": 100,
            "current_participants": 45,
            "organizer": "计算机学院",
            "created_at": "2024-01-20T10:00:00"
        },
        {
            "id": 2,
            "title": "职业规划讲座",
            "description": "邀请行业专家分享职业发展经验",
            "category": "讲座",
            "status": "进行中",
            "start_time": "2024-02-01T14:00:00",
            "end_time": "2024-02-01T16:00:00",
            "location": "大礼堂",
            "max_participants": 300,
            "current_participants": 280,
            "organizer": "就业指导中心",
            "created_at": "2024-01-15T10:00:00"
        },
        {
            "id": 3,
            "title": "创新创业工作坊",
            "description": "学习创业基础知识，体验商业计划书撰写",
            "category": "工作坊",
            "status": "报名中",
            "start_time": "2024-03-10T10:00:00",
            "end_time": "2024-03-10T17:00:00",
            "location": "创客空间",
            "max_participants": 50,
            "current_participants": 32,
            "organizer": "创新创业中心",
            "created_at": "2024-01-25T10:00:00"
        }
    ]
    
    # 筛选
    if status:
        activities = [a for a in activities if a["status"] == status]
    
    # 分页
    total = len(activities)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_activities = activities[start_idx:end_idx]
    
    return success_response(data={
        "list": paginated_activities,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{activity_id}")
async def get_activity_detail(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_student)
):
    """
    获取活动详情
    """
    # Mock数据
    if activity_id == 1:
        activity = {
            "id": 1,
            "title": "编程马拉松大赛",
            "description": "为期48小时的编程挑战赛，团队协作完成创新项目",
            "detailed_description": "本次大赛面向全校学生开放，参赛者可以自由组队（3-5人）。大赛将提供丰富的API接口和数据集，要求参赛队伍在48小时内完成一个具有创新性和实用性的软件项目。",
            "category": "竞赛",
            "status": "报名中",
            "start_time": "2024-03-15T09:00:00",
            "end_time": "2024-03-17T18:00:00",
            "location": "科技楼101",
            "max_participants": 100,
            "current_participants": 45,
            "organizer": "计算机学院",
            "contact_person": "张老师",
            "contact_email": "zhang@university.edu",
            "contact_phone": "138-0000-0000",
            "requirements": ["具备编程基础", "能够团队协作", "拥有笔记本电脑"],
            "rewards": ["一等奖：5000元 + 证书", "二等奖：3000元 + 证书", "三等奖：1000元 + 证书"],
            "registration_deadline": "2024-03-10T23:59:59",
            "created_at": "2024-01-20T10:00:00",
            "updated_at": "2024-01-28T10:00:00"
        }
    else:
        return error_response(msg="活动不存在", code=404)
    
    return success_response(data=activity)
