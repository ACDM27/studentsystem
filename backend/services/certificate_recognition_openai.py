"""
Certificate Recognition Service using OpenAI Compatible API
Uses Alibaba Cloud DashScope with OpenAI-compatible interface
Enhanced to extract team members and advisors information
"""

import base64
import json
from typing import Dict, Optional
from datetime import datetime
from openai import OpenAI
from config import settings


class CertificateRecognitionServiceOpenAI:
    """Service for recognizing and extracting information from certificates using OpenAI-compatible API"""
    
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY or settings.QWEN_API_KEY
        self.model_name = settings.QWEN_VL_MODEL  # Use VL model for vision tasks
        self.base_url = settings.QWEN_BASE_URL
        
        # Initialize OpenAI client with DashScope endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode image file to base64 string
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded string of the image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def recognize_certificate(self, image_path: str) -> Dict:
        """
        Recognize certificate and extract structured information using OpenAI-compatible API
        
        Args:
            image_path: Path to the certificate image
            
        Returns:
            Dictionary containing extracted certificate information
        """
        try:
            # Encode image to base64
            image_base64 = self.encode_image_to_base64(image_path)
            
            # Prepare the prompt for certificate recognition
            prompt = """请仔细识别这张获奖证书/成果证书，并提取以下所有信息。

【最重要原则】
- certificate_name 必须提取证书中【具体的赛事名称/项目名称/论文名称/职业证书全称】
- 【严格禁止】将 certificate_name 设为 "荣誉证书"、"获奖证书"、"证书"、"奖状" 等泛指词汇
- 即便证书上印有"荣誉证书"大字，也必须找到下方正文中的具体活动/赛事/成果名称

【人名识别注意事项】
1. 仔细辨认每个汉字，特别是人名
2. 对于相似字要特别注意区分（如：华/华、锋/峰、涛/滔等）
3. 如果某个字不确定，请在该人名后标注"(?)"
4. 请多次检查人名是否识别正确
5. **特别注意团队奖项**：如果是团队获奖，"recipient_name"应设为null，必须在"team_members"中列出所有成员

【需要提取的信息】

**基本信息：**
1. certificate_name: 证书中最核心的具体内容名称（赛事/论文/项目/职业资格证书全称）【禁止填写"荣誉证书"】
2. recipient_name: 主要获奖者姓名（个人奖项），团队奖则填null
3. issuing_organization: 颁发单位/组织的完整名称，用顿号分隔多个单位
4. issue_date: 获奖时间/颁发日期（格式：YYYY-MM-DD）
5. certificate_number: 证书编号（如果有）

**奖项详情：**
6. award_level: 奖项等级（如：一等奖、二等奖、三等奖、优秀奖、优胜奖等）
7. category: 成果类别，从以下选项中选一个：
   - "competition"（学科竞赛/技能大赛）
   - "research"（科研成果）
   - "project"（创新创业项目）
   - "paper"（学术论文发表）
   - "patent"（专利/软件著作权）
   - "certificate"（职业资格证书/荣誉表彰/其他）
8. award_rank: 具体奖项名称（如"一等奖"、"金奖"、"优胜奖"、"已发表"等）
9. project_name: 完整的项目/作品/论文名称
10. paper_title: 若为论文类，提取完整论文题目
11. journal_name: 若为论文类，提取期刊名称及级别（SCI/EI/核心等）
12. role: 获奖人在团队中的角色（第一作者/项目负责人/主要参与者等）

**人员信息（最重要，请仔细识别）：**
13. team_members: 所有团队成员名单（数组）                                      
14. advisors: 指导老师/指导教师列表（数组）
15. additional_info: 其他重要信息（所在学院、班界、特别说明等）

【返回格式】
请严格按照以下JSON格式返回，不要添加任何其他文字：

{
    "certificate_name": "第六届智警杯大数据技能竞赛",
    "recipient_name": null,
    "issuing_organization": "广西警察学院",
    "issue_date": "2024-06-01",
    "certificate_number": null,
    "award_level": "校级",
    "category": "competition",
    "award_rank": "优胜奖",
    "project_name": null,
    "paper_title": null,
    "journal_name": null,
    "role": null,
    "team_members": ["朱雄", "潘思翰", "庄嘉洛"],
    "advisors": ["秦振旗", "李雄"],
    "additional_info": null,
    "recognition_confidence": {
        "team_members": "high",
        "advisors": "high"
    }
}

【注意事项】
- 如果字段不存在或无法识别，使用null
- team_members和advisors必须是数组
- 人名识别不确定时，在recognition_confidence中标注为medium或low
- 只返回JSON，不要有任何解释性文字"""
            
            # Create chat completion request with vision
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                temperature=0.1,  # Lower temperature for more consistent output
                max_tokens=1500  # Increased for more detailed extraction
            )
            
            # Extract the response
            content = completion.choices[0].message.content
            
            # Try to parse JSON from the response
            # The model might return JSON wrapped in markdown code blocks
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            certificate_data = json.loads(content)
            
            # Add metadata
            certificate_data["recognition_time"] = datetime.utcnow().isoformat()
            certificate_data["model_used"] = self.model_name
            certificate_data["confidence"] = "high"
            
            return {
                "success": True,
                "data": certificate_data,
                "raw_response": content,
                "usage": {
                    "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
                    "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
                    "total_tokens": completion.usage.total_tokens if completion.usage else 0
                }
            }
                    
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "raw_response": content if 'content' in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def batch_recognize_certificates(self, image_paths: list[str]) -> list[Dict]:
        """
        Batch recognize multiple certificates
        
        Args:
            image_paths: List of paths to certificate images
            
        Returns:
            List of dictionaries containing extracted information for each certificate
        """
        results = []
        for image_path in image_paths:
            result = self.recognize_certificate(image_path)
            results.append(result)
        return results
    
    def _generate_smart_title(self, data: Dict) -> str:
        """
        根据OCR识别出的各字段，智能生成一个具体、有描述性的证书标题。
        当 certificate_name 为泛化词（如"荣誉证书"）时调用此方法。

        Args:
            data: OCR识别的原始字段字典

        Returns:
            生成的标题字符串
        """
        category = (data.get("category") or "").strip()
        cert_name = (data.get("certificate_name") or "").strip()
        recipient = (data.get("recipient_name") or "").strip()
        # award_rank 是新字段，兼容旧字段 award_level
        award = (data.get("award_rank") or data.get("award") or "").strip()
        award_level = (data.get("award_level") or "").strip()
        issuer = (data.get("issuing_organization") or "").strip()
        paper_title = (data.get("paper_title") or "").strip()
        journal_name = (data.get("journal_name") or "").strip()
        project_name = (data.get("project_name") or "").strip()
        role = (data.get("role") or "").strip()
        advisor_list = data.get("advisors") or []
        advisor = "、".join(advisor_list) if isinstance(advisor_list, list) else str(advisor_list)
        team = data.get("team_members") or []
        # 如果没有单独的 recipient，从 team_members 里取第一个
        if not recipient and team and isinstance(team, list):
            recipient = "、".join(team[:3])  # 最多显示3人

        generic_names = {"荣誉证书", "获奖证书", "奖状", "证书", "证明", "奖励证书", "优秀证书", "honorary credential"}
        is_generic_cert_name = cert_name.lower() in {n.lower() for n in generic_names} or not cert_name

        # ── 1. 学术论文发表类 ──
        if category == "paper":
            core = paper_title or (cert_name if not is_generic_cert_name else "")
            title = "学术论文发表证明"
            if recipient:
                title += f"——{recipient}"
            if core:
                title += f"发表论文《{core}》"
            if journal_name:
                title += f"于{journal_name}"
            if issuer:
                title += f"（颁发单位：{issuer}）"
            return title

        # ── 2. 科研成果类 ──
        if category == "research":
            core = project_name or (cert_name if not is_generic_cert_name else "")
            title = "科研成果证明"
            if recipient:
                title += f"——{recipient}"
            if core:
                title += f"参与科研项目《{core}》"
            if role:
                title += f"（角色：{role}）"
            if award_level:
                title += f"[{award_level}]"
            if issuer:
                title += f"（颁发单位：{issuer}）"
            return title

        # ── 3. 创新创业项目类 ──
        if category == "project":
            core = project_name or (cert_name if not is_generic_cert_name else "")
            title = "创新创业项目证明"
            if recipient:
                title += f"——{recipient}"
            if core:
                title += f"参与项目《{core}》"
            if role:
                title += f"（角色：{role}）"
            if award and award not in {"参与"}:
                title += f"获{award}"
            if award_level:
                title += f"[{award_level}]"
            if issuer:
                title += f"（颁发单位：{issuer}）"
            return title

        # ── 4. 专利/软件著作权类 ──
        if category == "patent":
            core = cert_name if not is_generic_cert_name else (project_name or "")
            title = "专利/软件著作权证书"
            if recipient:
                title += f"——{recipient}"
            if core:
                title += f"《{core}》"
            if role:
                title += f"（角色：{role}）"
            if issuer:
                title += f"（颁发单位：{issuer}）"
            return title

        # ── 5. 学科竞赛类（competition 或未分类但有奖项） ──
        if category == "competition" or (not category and award):
            event_name = cert_name if not is_generic_cert_name else ""
            parts = []
            if award_level:
                parts.append(award_level)
            if event_name:
                parts.append(event_name)
            elif issuer:
                parts.append(f"{issuer}主办赛事")
            if award:
                parts.append(award)
            core_desc = "".join(parts) if parts else "学科竞赛获奖"
            if recipient:
                title = f"{recipient}在{core_desc}中获奖证明"
            else:
                title = f"{core_desc}获奖证明"
            if advisor:
                title += f"（指导教师：{advisor}）"
            return title

        # ── 6. 职业资格证书/荣誉表彰/其他 ──
        if not is_generic_cert_name:
            title = cert_name
            if recipient:
                title = f"{recipient}——{title}"
            if award and award not in {"通过", "参与"}:
                title += f"（{award}）"
            if issuer:
                title += f"[{issuer}颁发]"
            return title

        # ── 最终兜底 ──
        fallback_parts = []
        if award_level:
            fallback_parts.append(award_level)
        if award and award not in {"通过", "参与"}:
            fallback_parts.append(award)
        if issuer:
            fallback_parts.append(f"{issuer}颁发")
        if fallback_parts:
            base = "".join(fallback_parts)
            if recipient:
                return f"{recipient}获{base}证明"
            return f"{base}证明"
        return "成果证明"

    def validate_recognition_result(self, result: Dict) -> Dict:
        """
        Validate and clean the recognition result.
        加入智能标题生成，确保标题不会停留在"荣誉证书"等泛化词汇。

        Args:
            result: Recognition result dictionary

        Returns:
            Validated and cleaned result
        """
        if not result.get("success"):
            return result

        data = result.get("data", {})

        # 放宽校验：只要有识别内容就继续处理，由智能标题生成兜底
        # （不再强制要求 certificate_name 和 issuing_organization 非空，避免遗漏信息）
        has_recipient = bool(data.get("recipient_name"))
        has_team = bool(data.get("team_members") and len(data.get("team_members", [])) > 0)

        if not has_recipient and not has_team:
            # 如果真的完全识别不到人名，才报错
            return {
                "success": False,
                "error": "Missing recipient info: Valid certificate must have either 'recipient_name' or 'team_members'",
                "data": data
            }

        # 清洗数据，兼容新旧字段名
        cleaned_data = {
            "certificate_name": (data.get("certificate_name") or "").strip(),
            "recipient_name": data.get("recipient_name", "").strip() if data.get("recipient_name") else None,
            "issuing_organization": (data.get("issuing_organization") or "").strip(),
            "issue_date": data.get("issue_date"),
            "certificate_number": data.get("certificate_number"),
            "award_level": data.get("award_level"),
            "category": data.get("category"),
            # award_rank 是新字段名，兼容旧字段 award
            "award": data.get("award_rank") or data.get("award"),
            "project_name": data.get("project_name"),
            "paper_title": data.get("paper_title"),
            "journal_name": data.get("journal_name"),
            "role": data.get("role"),
            "team_members": data.get("team_members", []),
            "advisors": data.get("advisors", []),
            "additional_info": data.get("additional_info"),
            "recognition_confidence": data.get("recognition_confidence", {}),
            "recognition_time": data.get("recognition_time"),
            "model_used": data.get("model_used"),
            "confidence": data.get("confidence")
        }

        # ─── 智能标题生成 ───
        GENERIC_NAMES = {"荣誉证书", "获奖证书", "奖状", "证书", "证明", "奖励证书", "优秀证书"}
        raw_cert_name = cleaned_data["certificate_name"]

        if raw_cert_name and raw_cert_name not in GENERIC_NAMES:
            # AI 识别到了具体名称，补充获奖人和奖项信息，使标题更完整
            title = raw_cert_name
            recipient = (cleaned_data.get("recipient_name") or "").strip()
            award = (cleaned_data.get("award") or "").strip()
            if award and award not in {"通过", "参与"} and award not in title:
                title = f"{title}——{award}"
            if recipient and recipient not in title:
                title = f"{recipient}在{title}"
            cleaned_data["title"] = title
        else:
            # certificate_name 是泛化词或为空，启用智能标题生成
            cleaned_data["title"] = self._generate_smart_title(data)

        return {
            "success": True,
            "data": cleaned_data,
            "usage": result.get("usage", {})
        }


# Create a singleton instance
certificate_recognition_service_openai = CertificateRecognitionServiceOpenAI()
