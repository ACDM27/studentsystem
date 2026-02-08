"""
Courses Router - 课程管理API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import get_db
from utils import success_response, error_response
from dependencies import require_student
from models import SysStudent, SysUser

router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])


@router.get("")
async def get_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    semester: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_student)
):
    """
    获取课程列表（学生端）
    支持分页和各种筛选
    """
    # Mock数据 - 实际应该从数据库查询
    # TODO: 创建Course模型和数据库表
    
    courses = [
        {
            "id": 1,
            "course_code": "CS101",
            "course_name": "数据结构与算法",
            "teacher_name": "李明",
            "teacher_id": 1,
            "credits": 4,
            "semester": "2023-2024-2",
            "category": "专业必修",
            "total_hours": 64,
            "theory_hours": 48,
            "practice_hours": 16,
            "schedule": "周一 1-2节、周三 3-4节",
            "location": "教学楼 A301",
            "max_students": 120,
            "enrolled_students": 95,
            "status": "进行中",
            "description": "本课程主要介绍常用的数据结构和算法设计方法",
            "created_at": "2023-09-01T00:00:00"
        },
        {
            "id": 2,
            "course_code": "CS202",
            "course_name": "计算机网络",
            "teacher_name": "王芳",
            "teacher_id": 2,
            "credits": 3,
            "semester": "2023-2024-2",
            "category": "专业必修",
            "total_hours": 48,
            "theory_hours": 40,
            "practice_hours": 8,
            "schedule": "周二 3-4节",
            "location": "教学楼 B205",
            "max_students": 100,
            "enrolled_students": 88,
            "status": "进行中",
            "description": "学习计算机网络的基本原理、协议和应用",
            "created_at": "2023-09-01T00:00:00"
        },
        {
            "id": 3,
            "course_code": "CS303",
            "course_name": "软件工程",
            "teacher_name": "张伟",
            "teacher_id": 3,
            "credits": 3,
            "semester": "2023-2024-2",
            "category": "专业选修",
            "total_hours": 48,
            "theory_hours": 32,
            "practice_hours": 16,
            "schedule": "周四 1-2节",
            "location": "教学楼 A402",
            "max_students": 80,
            "enrolled_students": 72,
            "status": "进行中",
            "description": "介绍软件开发的全生命周期和各种开发方法",
            "created_at": "2023-09-01T00:00:00"
        },
        {
            "id": 4,
            "course_code": "CS404",
            "course_name": "人工智能基础",
            "teacher_name": "赵丽",
            "teacher_id": 4,
            "credits": 3,
            "semester": "2023-2024-2",
            "category": "专业选修",
            "total_hours": 48,
            "theory_hours": 36,
            "practice_hours": 12,
            "schedule": "周五 3-4节",
            "location": "教学楼 C101",
            "max_students": 60,
            "enrolled_students": 58,
            "status": "进行中",
            "description": "学习人工智能的基本概念、算法和应用",
            "created_at": "2023-09-01T00:00:00"
        }
    ]
    
    # 筛选
    if semester:
        courses = [c for c in courses if c["semester"] == semester]
    if category:
        courses = [c for c in courses if c["category"] == category]
    
    # 分页
    total = len(courses)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_courses = courses[start_idx:end_idx]
    
    return success_response(data={
        "list": paginated_courses,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{course_id}")
async def get_course_detail(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: SysUser = Depends(require_student)
):
    """
    获取课程详情
    """
    # Mock数据
    if course_id == 1:
        course = {
            "id": 1,
            "course_code": "CS101",
            "course_name": "数据结构与算法",
            "teacher_name": "李明",
            "teacher_id": 1,
            "credits": 4,
            "semester": "2023-2024-2",
            "category": "专业必修",
            "total_hours": 64,
            "theory_hours": 48,
            "practice_hours": 16,
            "schedule": "周一 1-2节、周三 3-4节",
            "location": "教学楼 A301",
            "max_students": 120,
            "enrolled_students": 95,
            "status": "进行中",
            "description": "本课程主要介绍常用的数据结构和算法设计方法，包括线性表、栈、队列、树、图等数据结构，以及排序、查找、动态规划等算法。",
            "objectives": [
                "掌握常用数据结构的特点和应用场景",
                "理解算法复杂度分析方法",
                "能够设计和实现基本算法",
                "培养解决实际问题的能力"
            ],
            "textbook": "《数据结构与算法分析》(第3版)",
            "references": [
                "《算法导论》",
                "《数据结构(C语言版)》"
            ],
            "assessment": {
                "attendance": 10,
                "homework": 20,
                "lab": 20,
                "midterm": 20,
                "final": 30
            },
            "syllabus": [
                {"week": 1, "topic": "课程介绍、算法复杂度分析"},
                {"week": 2, "topic": "线性表"},
                {"week": 3, "topic": "栈和队列"},
                {"week": 4, "topic": "字符串"},
                {"week": 5, "topic": "树与二叉树"},
                {"week": 6, "topic": "图的基本概念"},
                {"week": 7, "topic": "图的遍历算法"},
                {"week": 8, "topic": "期中考试"},
            ],
            "created_at": "2023-09-01T00:00:00",
            "updated_at": "2024-01-28T10:00:00"
        }
    else:
        return error_response(msg="课程不存在", code=404)
    
    return success_response(data=course)
