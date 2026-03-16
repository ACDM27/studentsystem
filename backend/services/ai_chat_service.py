"""
AI Chat Service using OpenAI Compatible API (Alibaba Cloud Qwen)
Provides conversational AI capabilities for student achievement analysis
"""

import json
import re
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI
from config import settings


class AiChatService:
    """Service for AI-powered chat with student context awareness"""

    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY or settings.QWEN_API_KEY
        self.model_name = settings.QWEN_MODEL_NAME
        self.base_url = settings.QWEN_BASE_URL

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        self.system_prompt = """你是一位专业的学生成果画像分析师，专注于分析大学生的各类学术与实践成果。

你的核心职责：
1. 基于学生的成果数据（竞赛、科研、项目、论文、专利、证书）进行深度分析
2. 识别学生的优势领域和发展潜力
3. 提供基于数据的个性化发展建议
4. 帮助学生理解自身成果的含金量和竞争力

分析维度：
- 成果类型分布：6类成果（竞赛/科研/项目/论文/专利/证书）的数量与占比
- 成果含金量：关注奖项级别（国家级/省部级/市级/校级/院级）
- 成长趋势：成果产出的时间变化规律
- 发展均衡性：是否存在偏科或短板
- 审核质量：通过率反映材料规范度

回答风格：
- 数据驱动，用具体数字说话
- 直接指出优势和不足，不空泛鼓励
- 建议具体可行，有针对性
- 简洁明了，重点突出

重要原则：
- 如果学生询问与学习成果无关的话题，礼貌地引导回成果相关内容
- 始终保持积极正面但客观的态度
- 尊重学生隐私"""

    def chat(
        self,
        user_message: str,
        student_context: Optional[Dict] = None,
        chat_history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 800
    ) -> Dict:
        try:
            messages = []

            system_content = self.system_prompt
            if student_context:
                context_str = self._format_student_context(student_context)
                system_content += f"\n\n当前学生信息：\n{context_str}"

            messages.append({
                "role": "system",
                "content": system_content
            })

            if chat_history:
                limited_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
                messages.extend(limited_history)

            messages.append({
                "role": "user",
                "content": user_message
            })

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

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

    def generate_persona(
        self,
        student_context: Dict,
        chat_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Generate structured student persona based on achievements and chat history.
        Returns a structured JSON persona.
        """
        persona_prompt = """你是一位学生成果画像生成专家。请根据以下学生的成果数据和对话记录，生成一份结构化的人物画像。

你必须严格返回以下JSON格式，不要添加任何其他文字、解释或markdown标记：

{
  "summary": "一段50-100字的人物概述，概括该学生的成果特征和发展方向",
  "tags": ["标签1", "标签2", "标签3"],
  "dimensions": {
    "quantity": {"label": "成果数量", "analysis": "简短文字分析，10-20字"},
    "quality": {"label": "成果含金量", "analysis": "简短文字分析，10-20字"},
    "diversity": {"label": "发展多样性", "analysis": "简短文字分析，10-20字"},
    "growth": {"label": "成长趋势", "analysis": "简短文字分析，10-20字"},
    "activity": {"label": "活跃程度", "analysis": "简短文字分析，10-20字"}
  },
  "strengths": ["优势描述1", "优势描述2"],
  "suggestions": ["发展建议1", "发展建议2"]
}

dimensions中每个维度的analysis要求：
- quantity（成果数量）：基于成果总数给出简短评价，如"成果丰富，积累深厚"、"起步阶段，有待积累"
- quality（成果含金量）：基于最高奖项级别评价，如"已获省部级以上荣誉"、"以校级成果为主，可冲击更高级别"
- diversity（发展多样性）：基于成果类型覆盖面评价，如"覆盖4个领域，发展均衡"、"集中于竞赛方向，建议拓展"
- growth（成长趋势）：基于时间分布评价，如"产出逐年增长，势头良好"、"近期较为沉寂"
- activity（活跃程度）：基于最近成果时间和频率评价，如"近期活跃，持续产出"、"已有一段时间未更新"

tags要求：3-6个关键词标签，如"竞赛达人"、"科研新星"、"全面发展"、"论文能手"等
strengths：2-4条具体优势
suggestions：2-4条具体建议"""

        try:
            messages = [
                {"role": "system", "content": persona_prompt}
            ]

            context_str = self._format_student_context(student_context)

            # Build the user message with context and chat summary
            user_content = f"学生信息与成果数据：\n{context_str}"

            if chat_history:
                # Summarize recent chat for persona context
                chat_summary_parts = []
                for msg in chat_history[-20:]:
                    role = "学生" if msg.get("role") == "user" else "AI"
                    content = msg.get("content", "")[:200]
                    chat_summary_parts.append(f"{role}: {content}")
                user_content += f"\n\n近期对话记录：\n" + "\n".join(chat_summary_parts)

            user_content += "\n\n请根据以上信息生成该学生的人物画像JSON。"
            messages.append({"role": "user", "content": user_content})

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.5,
                max_tokens=1200
            )

            ai_response = completion.choices[0].message.content.strip()

            # Try to extract JSON from the response
            persona_data = self._extract_json(ai_response)

            if persona_data and self._validate_persona(persona_data):
                # Ensure dimensions use analysis text format, not score format
                if "dimensions" in persona_data:
                    for key, dim in persona_data["dimensions"].items():
                        if isinstance(dim, dict) and "score" in dim and "analysis" not in dim:
                            # Convert old score format to text analysis
                            dim["analysis"] = f"评分 {dim['score']}/100"
                        if isinstance(dim, dict):
                            dim.pop("score", None)
                persona_data["generated_at"] = datetime.utcnow().isoformat()
                return {"success": True, "data": persona_data}
            else:
                # Return a fallback persona based on raw stats
                return {
                    "success": True,
                    "data": self._build_fallback_persona(student_context)
                }

        except Exception as e:
            import traceback
            print(f"❌ Persona Generation Exception: {str(e)}")
            print(f"Traceback:\n{traceback.format_exc()}")
            return {
                "success": False,
                "error": f"Persona generation error: {str(e)}"
            }

    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from AI response text."""
        # Try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON block in markdown
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Try to find first { ... } block
        brace_match = re.search(r'\{.*\}', text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        return None

    def _validate_persona(self, data: Dict) -> bool:
        """Check if persona data has required fields."""
        required = ["summary", "tags", "dimensions", "strengths", "suggestions"]
        return all(k in data for k in required)

    def _build_fallback_persona(self, context: Dict) -> Dict:
        """Build a basic persona from raw statistics when AI parsing fails."""
        stats = context.get("statistics", {})
        type_dist = context.get("type_distribution", {})
        level_dist = context.get("level_distribution", {})

        total = stats.get("total_achievements", 0)

        # Quantity analysis
        if total == 0: q_text = "暂无成果记录"
        elif total <= 2: q_text = "起步阶段，有待积累"
        elif total <= 5: q_text = "有一定积累，继续保持"
        elif total <= 10: q_text = "成果较为丰富"
        else: q_text = "成果丰富，积累深厚"

        # Quality analysis
        level_order = ["国家级", "省部级", "市级", "校级", "院级"]
        best_level = None
        for level in level_order:
            if level_dist.get(level, 0) > 0:
                best_level = level
                break
        if best_level:
            qual_text = f"最高达{best_level}水平"
        else:
            qual_text = "暂无级别评定"

        # Diversity analysis
        types_with_data = sum(1 for v in type_dist.values() if v > 0)
        if types_with_data >= 4: div_text = f"覆盖{types_with_data}个领域，发展均衡"
        elif types_with_data >= 2: div_text = f"涉及{types_with_data}个领域，可进一步拓展"
        elif types_with_data == 1: div_text = "集中于单一方向，建议拓展"
        else: div_text = "暂无成果类型记录"

        tags = []
        if type_dist.get("竞赛", 0) >= 2: tags.append("竞赛达人")
        if type_dist.get("科研", 0) >= 2: tags.append("科研新星")
        if type_dist.get("论文", 0) >= 2: tags.append("论文能手")
        if type_dist.get("专利", 0) >= 1: tags.append("创新发明")
        if type_dist.get("项目", 0) >= 2: tags.append("项目实践")
        if types_with_data >= 4: tags.append("全面发展")
        if not tags:
            tags = ["成长中"]

        return {
            "summary": f"该学生共有{total}项成果记录，涵盖{types_with_data}个类型领域。",
            "tags": tags[:6],
            "dimensions": {
                "quantity": {"label": "成果数量", "analysis": q_text},
                "quality": {"label": "成果含金量", "analysis": qual_text},
                "diversity": {"label": "发展多样性", "analysis": div_text},
                "growth": {"label": "成长趋势", "analysis": "暂无足够数据判断趋势"},
                "activity": {"label": "活跃程度", "analysis": "暂无足够数据判断活跃度"}
            },
            "strengths": [f"已积累{total}项成果"] if total > 0 else ["暂无明显优势，建议积极参与各类活动"],
            "suggestions": ["建议持续积累更多类型的成果", "关注高级别竞赛和科研机会"],
            "generated_at": datetime.utcnow().isoformat()
        }

    def _format_student_context(self, context: Dict) -> str:
        parts = []

        if "name" in context:
            parts.append(f"姓名：{context['name']}")
        if "major" in context:
            parts.append(f"专业：{context['major']}")
        if "class_name" in context:
            parts.append(f"班级：{context['class_name']}")

        # Type distribution
        if "type_distribution" in context:
            td = context["type_distribution"]
            parts.append(f"\n成果类型分布：")
            type_names = {"竞赛": "competition", "科研": "research", "项目": "project",
                         "论文": "paper", "专利": "patent", "证书": "certificate"}
            for cn_name in type_names:
                count = td.get(cn_name, 0)
                if count > 0:
                    parts.append(f"  {cn_name}：{count} 项")

        # Level distribution
        if "level_distribution" in context:
            ld = context["level_distribution"]
            non_empty = {k: v for k, v in ld.items() if v > 0}
            if non_empty:
                parts.append(f"\n奖项级别分布：")
                for level, count in non_empty.items():
                    parts.append(f"  {level}：{count} 项")

        # Yearly trend
        if "yearly_trend" in context:
            yt = context["yearly_trend"]
            if yt:
                parts.append(f"\n年度成果趋势：")
                for year in sorted(yt.keys()):
                    parts.append(f"  {year}年：{yt[year]} 项")

        # Achievement details
        if "achievements" in context and context["achievements"]:
            parts.append(f"\n成果详情：")
            achievements = context["achievements"]
            total_count = len(achievements)
            display_count = min(10, total_count)

            for i, ach in enumerate(achievements[:display_count], 1):
                ach_type = ach.get("type", "其他")
                ach_title = ach.get("title", "未命名")
                ach_status = ach.get("status", "unknown")

                status_emoji = {
                    "approved": "✅", "pending": "⏳", "rejected": "❌"
                }.get(ach_status, "❓")

                parts.append(f"  {i}. {status_emoji} [{ach_type}] {ach_title}")

                if ach.get("content_json"):
                    content = ach["content_json"]
                    details = []
                    if content.get("award_level"):
                        details.append(f"级别:{content['award_level']}")
                    if content.get("award_rank"):
                        details.append(f"奖项:{content['award_rank']}")
                    if content.get("issuing_organization"):
                        details.append(f"颁发:{content['issuing_organization']}")
                    if details:
                        parts.append(f"     {' | '.join(details)}")

                if ach.get("audit_comment"):
                    parts.append(f"     审核意见: {ach['audit_comment']}")

                if ach.get("teacher_name"):
                    teacher_info = ach['teacher_name']
                    if ach.get("teacher_title"):
                        teacher_info += f"({ach['teacher_title']})"
                    parts.append(f"     指导教师: {teacher_info}")

            if total_count > display_count:
                parts.append(f"  ...以及其他 {total_count - display_count} 项成果")

        # Statistics
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
        return bool(self.api_key)


# Create singleton instance
ai_chat_service = AiChatService()
