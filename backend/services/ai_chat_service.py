"""
AI Chat Service using OpenAI Compatible API (Alibaba Cloud Qwen)
Provides conversational AI capabilities for student learning assistance
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from config import settings


class AiChatService:
    """Service for AI-powered chat with student context awareness"""
    
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY or settings.QWEN_API_KEY
        self.model_name = settings.QWEN_MODEL_NAME  # Use text model for chat
        self.base_url = settings.QWEN_BASE_URL
        
        # Initialize OpenAI client with DashScope endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # System prompt for student learning assistant
        self.system_prompt = """你是一位专业的AI学习助手，专门帮助大学生进行学习规划、成果分析和职业发展指导。

你的职责：
1. 分析学生的学习成果和成就
2. 提供个性化的学习建议
3. 帮助制定职业规划
4. 解答学习相关问题
5. 鼓励学生持续进步

回答风格：
- 友好、专业、有建设性
- 基于学生的实际成果数据给出建议
- 避免空泛的鼓励，提供具体可行的建议
- 回答简洁明了，重点突出

重要原则：
- 如果学生询问与学习无关的话题，礼貌地引导回学习相关内容
- 始终保持积极正面的态度
- 尊重学生隐私，不要求不必要的个人信息"""
    
    def chat(
        self,
        user_message: str,
        student_context: Optional[Dict] = None,
        chat_history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 800
    ) -> Dict:
        """
        Send a chat message and get AI response
        
        Args:
            user_message: The user's message
            student_context: Optional context about the student (achievements, profile, etc.)
            chat_history: Optional list of previous messages [{"role": "user"/"assistant", "content": "..."}]
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Dictionary containing the AI response and metadata
        """
        try:
            # Build messages array
            messages = []
            
            # Add system prompt with student context
            system_content = self.system_prompt
            if student_context:
                context_str = self._format_student_context(student_context)
                system_content += f"\n\n当前学生信息：\n{context_str}"
            
            messages.append({
                "role": "system",
                "content": system_content
            })
            
            # Add chat history (limit to last 10 messages to control token usage)
            if chat_history:
                limited_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
                messages.extend(limited_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI-compatible API
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract response
            ai_response = completion.choices[0].message.content
            
            return {
                "success": True,
                "message": ai_response,
                "usage": {
                    "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                    "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                    "total_tokens": completion.usage.total_tokens if completion.usage else 0
                },
                "model": self.model_name,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ AI Chat Service Exception: {str(e)}")
            print(f"Traceback:\n{error_details}")
            print(f"API Key configured: {bool(self.api_key)}")
            print(f"Model: {self.model_name}")
            print(f"Base URL: {self.base_url}")
            return {
                "success": False,
                "error": f"AI chat service error: {str(e)}",
                "message": "抱歉，AI助手暂时无法回复，请稍后再试。"
            }
    
    def _format_student_context(self, context: Dict) -> str:
        """
        Format student context into a readable string for the AI
        
        Args:
            context: Dictionary with student information
            
        Returns:
            Formatted context string
        """
        parts = []
        
        # Student basic info
        if "name" in context:
            parts.append(f"姓名：{context['name']}")
        if "major" in context:
            parts.append(f"专业：{context['major']}")
        if "class_name" in context:
            parts.append(f"班级：{context['class_name']}")
        
        # Achievements - now with full details
        if "achievements" in context and context["achievements"]:
            parts.append(f"\n学习成果详情：")
            
            # 显示所有成果，但对于很多成果的情况进行智能摘要
            achievements = context["achievements"]
            total_count = len(achievements)
            
            # 如果成果较多，只详细展示最近10条，其余简要说明
            display_count = min(10, total_count)
            
            for i, ach in enumerate(achievements[:display_count], 1):
                ach_type = ach.get("type", "其他")
                ach_title = ach.get("title", "未命名")
                ach_status = ach.get("status", "unknown")
                
                # 状态标识
                status_emoji = {
                    "approved": "✅",
                    "pending": "⏳",
                    "rejected": "❌"
                }.get(ach_status, "❓")
                
                parts.append(f"  {i}. {status_emoji} [{ach_type}] {ach_title}")
                
                # 如果有详细内容，展示关键信息
                if ach.get("content_json"):
                    content = ach["content_json"]
                    details = []
                    if content.get("award_level"):
                        details.append(f"级别:{content['award_level']}")
                    if content.get("award"):
                        details.append(f"奖项:{content['award']}")
                    if content.get("issuing_organization"):
                        details.append(f"颁发:{content['issuing_organization']}")
                    if details:
                        parts.append(f"     {' | '.join(details)}")
                
                # 如果有审核意见，展示
                if ach.get("audit_comment"):
                    parts.append(f"     审核意见: {ach['audit_comment']}")
                
                # 教师信息
                if ach.get("teacher_name"):
                    teacher_info = ach['teacher_name']
                    if ach.get("teacher_title"):
                        teacher_info += f"({ach['teacher_title']})"
                    parts.append(f"     指导教师: {teacher_info}")
            
            if total_count > display_count:
                parts.append(f"  ...以及其他 {total_count - display_count} 项成果（详见完整数据）")
        
        # Statistics - now with more details
        if "statistics" in context:
            stats = context["statistics"]
            parts.append(f"\n成果统计：")
            if "total_achievements" in stats:
                parts.append(f"  总计：{stats['total_achievements']} 项")
            if "approved_achievements" in stats:
                parts.append(f"  已通过：{stats['approved_achievements']} 项")
            if "pending_achievements" in stats:
                parts.append(f"  待审核：{stats['pending_achievements']} 项")
            if "rejected_achievements" in stats:
                parts.append(f"  已拒绝：{stats['rejected_achievements']} 项")
            if "approval_rate" in stats:
                parts.append(f"  通过率：{stats['approval_rate']}%")
        
        return "\n".join(parts) if parts else "暂无学生信息"
    
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is configured
        
        Returns:
            True if API key is configured, False otherwise
        """
        return bool(self.api_key)


# Create singleton instance
ai_chat_service = AiChatService()
