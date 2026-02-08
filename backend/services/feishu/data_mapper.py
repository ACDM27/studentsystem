"""
Data Mapper Service
飞书数据字段映射和转换引擎
"""
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import SysTeacher, SysStudent
import logging
import re

logger = logging.getLogger(__name__)


class DataMapper:
    """数据映射引擎"""
    
    # 成果类别枚举映射
    TYPE_MAPPING = {
        "竞赛类": "competition",
        "科研类": "research",
        "项目类": "project",
        "论文类": "paper",
        "专利类": "patent",
        "证书类": "certificate",
        "学科竞赛": "competition",
        "创新创业项目": "project",
        "发表论文": "paper",
        "职业资格证书": "certificate"
    }
    
    # 奖项等级映射
    LEVEL_MAPPING = {
        "国家级": "national",
        "省部级": "provincial",
        "校级": "school",
        "院级": "department",
        "全国": "national",
        "国际": "international",
        "省": "provincial",
        "市": "city"
    }
    
    def __init__(self, mappings: List[Any], db: Session):
        """
        初始化数据映射器
        
        Args:
            mappings: 字段映射配置列表（FeishuFieldMapping对象）
            db: 数据库session
        """
        self.mappings = mappings
        self.db = db
        
        # 缓存教师和学生数据（优化性能）
        self._teacher_cache: Dict[str, int] = {}
        self._student_cache: Dict[str, int] = {}
        self._load_cache()
    
    def _load_cache(self):
        """预加载教师和学生数据到缓存"""
        # 加载所有教师
        teachers = self.db.query(SysTeacher).all()
        for teacher in teachers:
            self._teacher_cache[teacher.name] = teacher.id
        
        # 加载所有学生
        students = self.db.query(SysStudent).all()
        for student in students:
            self._student_cache[student.name] = student.id
        
        logger.info(f"缓存已加载: {len(self._teacher_cache)}位教师, {len(self._student_cache)}位学生")
    
    def transform_record(
        self, 
        feishu_record: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        转换单条飞书记录为数据库格式
        
        Args:
            feishu_record: 飞书记录（fields字段）
            
        Returns:
            (转换后的数据, 验证错误列表)
        """
        fields = feishu_record.get("fields", {}) if "fields" in feishu_record else feishu_record
        transformed = {}
        errors = []
        
        for mapping in self.mappings:
            feishu_field = mapping.feishu_field_name
            db_field = mapping.db_field_name
            transform_rule = mapping.transform_rule
            is_required = bool(mapping.is_required)
            
            # 获取原始值
            raw_value = fields.get(feishu_field)
            
            # 检查必填字段
            if is_required and not raw_value:
                errors.append(f"缺少必填字段: {feishu_field}")
                continue
            
            # 跳过空值（非必填字段）
            if not raw_value:
                continue
            
            # 应用转换规则
            try:
                converted_value = self._apply_transform(
                    raw_value, 
                    db_field, 
                    transform_rule
                )
                
                if converted_value is not None:
                    transformed[db_field] = converted_value
                elif is_required:
                    errors.append(f"字段转换失败: {feishu_field} -> {db_field}")
                    
            except Exception as e:
                error_msg = f"转换错误 [{feishu_field}]: {str(e)}"
                errors.append(error_msg)
                logger.warning(error_msg)
        
        return transformed, errors
    
    def _apply_transform(
        self, 
        value: Any, 
        db_field: str, 
        transform_rule: Optional[Dict[str, Any]]
    ) -> Any:
        """
        应用转换规则
        
        Args:
            value: 原始值
            db_field: 目标数据库字段
            transform_rule: 转换规则（JSON）
            
        Returns:
            转换后的值
        """
        # 特殊字段处理
        if db_field == "teacher_id":
            return self._resolve_teacher_id(value, transform_rule)
        elif db_field == "student_id":
            return self._resolve_student_id(value)
        elif db_field == "type":
            return self._map_achievement_type(value)
        elif db_field == "level":
            return self._map_award_level(value)
        elif db_field == "date":
            return self._parse_date(value)
        
        # 通用转换规则
        if not transform_rule:
            return value
        
        rule_type = transform_rule.get("type")
        
        if rule_type == "enum_mapping":
            mapping_dict = transform_rule.get("mapping", {})
            return mapping_dict.get(value, value)
        
        elif rule_type == "date_parse":
            date_format = transform_rule.get("date_format", "%Y-%m-%d")
            return self._parse_date(value, date_format)
        
        return value
    
    def _resolve_teacher_id(
        self, 
        teacher_name: str, 
        transform_rule: Optional[Dict[str, Any]]
    ) -> int:
        """
        教师姓名转ID
        
        Args:
            teacher_name: 教师姓名（可能包含多个，用顿号分隔）
            transform_rule: 转换规则
            
        Returns:
            教师ID
        """
        # 处理多个教师（取第一个）
        if "、" in teacher_name:
            teacher_name = teacher_name.split("、")[0].strip()
        
        # 去除常见后缀
        teacher_name = teacher_name.replace("老师", "").replace("教授", "").strip()
        
        # 精确匹配
        if teacher_name in self._teacher_cache:
            return self._teacher_cache[teacher_name]
        
        # 模糊匹配
        match_mode = transform_rule.get("match_mode", "exact") if transform_rule else "exact"
        if match_mode == "fuzzy":
            for name, teacher_id in self._teacher_cache.items():
                if teacher_name in name or name in teacher_name:
                    logger.info(f"模糊匹配教师: {teacher_name} -> {name}")
                    return teacher_id
        
        raise ValueError(f"未找到教师: {teacher_name}")
    
    def _resolve_student_id(self, student_name: str) -> int:
        """
        学生姓名转ID
        
        Args:
            student_name: 学生姓名
            
        Returns:
            学生ID
        """
        student_name = student_name.strip()
        
        # 精确匹配
        if student_name in self._student_cache:
            return self._student_cache[student_name]
        
        # 去除空格后再试
        student_name_no_space = student_name.replace(" ", "")
        for name, student_id in self._student_cache.items():
            if name.replace(" ", "") == student_name_no_space:
                return student_id
        
        raise ValueError(f"未找到学生: {student_name}")
    
    def _map_achievement_type(self, type_str: str) -> str:
        """
        成果类型映射
        
        Args:
            type_str: 飞书中的类型描述
            
        Returns:
            标准化类型代码
        """
        # 精确匹配
        if type_str in self.TYPE_MAPPING:
            return self.TYPE_MAPPING[type_str]
        
        # 模糊匹配
        for key, value in self.TYPE_MAPPING.items():
            if key in type_str or type_str in key:
                return value
        
        # 默认返回原值
        logger.warning(f"未匹配到成果类型: {type_str}，使用原值")
        return type_str
    
    def _map_award_level(self, level_str: str) -> str:
        """
        奖项等级映射
        
        Args:
            level_str: 飞书中的等级描述
            
        Returns:
            标准化等级代码
        """
        # 精确匹配
        if level_str in self.LEVEL_MAPPING:
            return self.LEVEL_MAPPING[level_str]
        
        # 模糊匹配
        for key, value in self.LEVEL_MAPPING.items():
            if key in level_str:
                return value
        
        # 默认返回原值
        logger.warning(f"未匹配到奖项等级: {level_str}，使用原值")
        return level_str
    
    def _parse_date(
        self, 
        date_value: Any, 
        date_format: str = "%Y-%m-%d"
    ) -> Optional[str]:
        """
        解析日期
        
        Args:
            date_value: 日期值（可能是时间戳、字符串等）
            date_format: 日期格式
            
        Returns:
            标准化日期字符串 (YYYY-MM-DD)
        """
        if not date_value:
            return None
        
        # 如果已经是标准格式
        if isinstance(date_value, str):
            # 验证格式
            try:
                datetime.strptime(date_value, date_format)
                return date_value
            except:
                pass
        
        # 飞书日期字段通常是时间戳（毫秒）
        if isinstance(date_value, (int, float)):
            # 转换为datetime
            timestamp = date_value / 1000  # 飞书使用毫秒时间戳
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d")
        
        # 尝试解析其他格式
        try:
            if isinstance(date_value, str):
                # 尝试常见格式
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日"]:
                    try:
                        dt = datetime.strptime(date_value, fmt)
                        return dt.strftime("%Y-%m-%d")
                    except:
                        continue
        except:
            pass
        
        logger.warning(f"日期解析失败: {date_value}")
        return None


def create_default_mappings() -> List[Dict[str, Any]]:
    """
    创建默认的字段映射配置
    
    Returns:
        默认映射配置列表
    """
    return [
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "学生姓名",
            "db_field_name": "student_id",
            "transform_rule": {"type": "student_name_to_id"},
            "is_required": True,
            "display_order": 1
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "成果标题",
            "db_field_name": "title",
            "is_required": True,
            "display_order": 2
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "成果类别",
            "db_field_name": "type",
            "transform_rule": {"type": "enum_mapping", "mapping": DataMapper.TYPE_MAPPING},
            "is_required": True,
            "display_order": 3
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "奖项等级",
            "db_field_name": "level",
            "transform_rule": {"type": "enum_mapping", "mapping": DataMapper.LEVEL_MAPPING},
            "is_required": True,
            "display_order": 4
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "具体奖项",
            "db_field_name": "award",
            "is_required": True,
            "display_order": 5
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "获奖日期",
            "db_field_name": "date",
            "transform_rule": {"type": "date_parse"},
            "is_required": True,
            "display_order": 6
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "指导教师",
            "db_field_name": "teacher_id",
            "transform_rule": {"type": "teacher_name_to_id", "match_mode": "fuzzy"},
            "is_required": True,
            "display_order": 7
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "颁发单位",
            "db_field_name": "issuer",
            "is_required": False,
            "display_order": 8
        },
        {
            "name": "标准成果导入模板",
            "feishu_field_name": "证书编号",
            "db_field_name": "certificate_number",
            "is_required": False,
            "display_order": 9
        }
    ]
