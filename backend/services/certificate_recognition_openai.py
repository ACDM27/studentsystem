"""
Certificate Recognition Service using OpenAI Compatible API
Uses Alibaba Cloud DashScope with OpenAI-compatible interface
Enhanced to extract team members and advisors information
"""

import base64
import json
import re
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
6. award_level: 奖项行政级别（如：国家级、省部级、市级、校级、院级；【注意】不是一等奖/二等奖，那是 award_rank 的内容）
7. category: 成果类别，从以下选项中选一个：
   - "competition"（学科竞赛/技能大赛）
   - "research"（科研成果）
   - "project"（创新创业项目）
   - "paper"（学术论文发表）
   - "patent"（专利/软件著作权）
   - "certificate"（职业资格证书/荣誉表彰/其他）
8. award_rank: 具体奖项名称（如"一等奖"、"二等奖"、"金奖"、"优胜奖"、"已发表"等；【注意】不是国家级/省级，那是 award_level 的内容）
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

    def classify_document(self, image_path: str) -> str:
        """
        Stage 1: Lightweight classification — determine the uploaded image's document type.

        Returns:
            'paper'       — academic paper / journal article / acceptance notice
            'patent'      — patent certificate / patent application document
            'competition' — competition award / contest certificate
            'certificate' — other certificate / honor / qualification (default fallback)
        """
        try:
            image_base64 = self.encode_image_to_base64(image_path)
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        },
                        {
                            "type": "text",
                            "text": (
                                "请判断这张图片的文档类型，只能从以下四个类别中选择一个：\n"
                                "1. paper — 学术论文页面、期刊文章正文、论文录用通知、版面费票据等论文相关文件\n"
                                "2. patent — 专利证书、专利授权通知书、专利申请受理通知书等专利相关文件\n"
                                "3. competition — 竞赛获奖证书、比赛奖状、学科竞赛证书等竞赛相关文件\n"
                                "4. certificate — 荣誉证书、资格证书、等级证书、结业证书等其他证书类文件\n"
                                "只输出 paper、patent、competition 或 certificate 中的一个，不要有任何其他文字。"
                            )
                        }
                    ]
                }],
                max_tokens=20
            )
            result = completion.choices[0].message.content.strip().lower()
            # 从结果中提取核心类型
            if "paper" in result:
                return "paper"
            elif "patent" in result:
                return "patent"
            elif "competition" in result:
                return "competition"
            elif "certificate" in result:
                return "certificate"
            return "certificate"
        except Exception:
            return "certificate"

    def recognize_paper(self, image_path: str) -> Dict:
        """
        Stage 2 (paper path): Extract structured information from an academic paper
        document using a paper-specific prompt.

        Args:
            image_path: Path to the paper image (page scan / acceptance letter / etc.)

        Returns:
            Dictionary with extracted paper metadata
        """
        try:
            image_base64 = self.encode_image_to_base64(image_path)

            prompt = """请仔细识别这份学术论文相关文件（论文页面/录用通知/期刊封页等），提取以下所有信息。

【最重要原则】
- paper_title 必须是论文的完整标题，禁止填写"学术论文"等泛指词汇
- authors 必须列出文件中出现的所有作者姓名
- journal_level 请根据期刊名称/ISSN/版权页信息判断，尽量准确
- 如果论文是英文的，必须同时提供中文翻译字段（_cn后缀），用于中文检索

【返回格式】
请严格按照以下JSON格式返回，不要添加任何其他文字：

{
    "paper_title": "论文完整标题（保留原文）",
    "journal_name": "期刊或会议完整名称（保留原文）",
    "journal_level": "SCI",
    "publish_status": "已发表",
    "publish_date": "2024-06",
    "authors": ["作者1", "作者2"],
    "first_author": "第一作者姓名（保留原文）",
    "author_order": "第一作者",
    "doi": null,
    "volume": null,
    "issue": null,
    "pages": null,
    "issn": null,
    "issuing_organization": null,
    "paper_title_cn": "论文标题的中文翻译",
    "journal_name_cn": "期刊名称的中文翻译",
    "authors_cn": ["作者1中文名", "作者2中文名"],
    "first_author_cn": "第一作者中文名",
    "issuing_organization_cn": "出版机构中文翻译"
}

【字段说明】
- journal_level：从以下选项中选一个：SCI、EI、北大核心、CSSCI、CSCD、普通期刊、会议论文
- publish_status：从以下选项中选一个：已发表、录用待刊、在审中
- author_order：仅当图片中能明确看出作者排序信息时，从以下选项中选一个：第一作者、通讯作者、第二作者、其他作者。如果图片中无法确定作者排序（如录用通知截图），填null
- publish_date：格式尽量为 YYYY-MM-DD 或 YYYY-MM 或 YYYY
- authors：所有作者姓名组成的数组，不要遗漏
- _cn 后缀字段：仅当论文为英文时必填，提供对应字段的中文翻译。中国人名拼音请还原为中文姓名。如果论文本身是中文，_cn字段填null
- 无法识别的字段用 null

只返回JSON，不要有任何解释性文字。"""

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }],
                temperature=0.1,
                max_tokens=1200
            )

            content = completion.choices[0].message.content

            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()

            paper_data = json.loads(content)
            paper_data["document_type"] = "paper"
            paper_data["recognition_time"] = datetime.utcnow().isoformat()
            paper_data["model_used"] = self.model_name
            paper_data["confidence"] = "high"

            return {
                "success": True,
                "data": paper_data,
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
                "raw_response": content if "content" in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def _is_english(self, text: str) -> bool:
        """判断文本是否主要为英文"""
        if not text:
            return False
        # 统计英文字母占比
        alpha_count = sum(1 for c in text if c.isascii() and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())
        if total_chars == 0:
            return False
        return alpha_count / total_chars > 0.7

    def _translate_paper_to_chinese(self, paper_data: Dict) -> Dict:
        """
        对英文论文的关键字段进行中文翻译，添加 _cn 后缀字段。
        翻译字段：paper_title, journal_name, authors, first_author, issuing_organization
        """
        fields_to_translate = {
            "paper_title": paper_data.get("paper_title", ""),
            "journal_name": paper_data.get("journal_name", ""),
            "first_author": paper_data.get("first_author", ""),
            "issuing_organization": paper_data.get("issuing_organization", ""),
        }

        # 收集需要翻译的英文字段
        english_fields = {k: v for k, v in fields_to_translate.items() if self._is_english(str(v))}

        # 检查 authors 列表
        authors = paper_data.get("authors", [])
        has_english_authors = isinstance(authors, list) and any(self._is_english(str(a)) for a in authors)

        if not english_fields and not has_english_authors:
            return paper_data  # 全是中文，无需翻译

        # 构建翻译请求
        translate_input = {}
        for k, v in english_fields.items():
            translate_input[k] = v
        if has_english_authors:
            translate_input["authors"] = authors

        try:
            text_client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            prompt = f"""请将以下英文学术论文信息翻译为中文。对于人名请音译为常见中文译名，如果是中国人名的拼音则还原为中文姓名。

输入：
{json.dumps(translate_input, ensure_ascii=False)}

请严格按照相同的JSON key返回翻译结果，不要添加任何其他文字。只返回JSON。"""

            completion = text_client.chat.completions.create(
                model=settings.QWEN_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )

            content = completion.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            translated = json.loads(content)

            # 将翻译结果写入 _cn 后缀字段
            for key in ["paper_title", "journal_name", "first_author", "issuing_organization"]:
                if key in translated:
                    paper_data[f"{key}_cn"] = translated[key]

            if "authors" in translated and isinstance(translated["authors"], list):
                paper_data["authors_cn"] = translated["authors"]

        except Exception as e:
            # 翻译失败不影响主流程
            import logging
            logging.getLogger(__name__).warning(f"Paper translation failed: {e}")

        return paper_data

    def _preprocess_image(self, image_path: str) -> str:
        """纠偏 + 增强图片，返回处理后的图片路径（失败则返回原路径）"""
        try:
            from services.image_preprocessor import image_preprocessor
            return image_preprocessor.preprocess_for_ocr(image_path)
        except Exception:
            return image_path

    def recognize_smart(self, image_path: str) -> Dict:
        """
        Two-stage OCR:
          Stage 1 — classify_document() → 'paper' | 'certificate'
          Stage 2 — route to recognize_paper() or recognize_certificate()

        The returned dict always contains data['document_type'] so callers can
        branch on what was detected.
        """
        image_path = self._preprocess_image(image_path)
        doc_type = self.classify_document(image_path)

        if doc_type == "paper":
            return self.recognize_paper(image_path)

        result = self.recognize_certificate(image_path)
        if result.get("success") and isinstance(result.get("data"), dict):
            result["data"]["document_type"] = "certificate"
        return result
    
    _GENERIC_NAMES = {
        "荣誉证书", "获奖证书", "奖状", "证书", "证明",
        "奖励证书", "优秀证书", "honorary credential",
    }

    def _is_generic(self, name: str) -> bool:
        return not name or name.lower() in {n.lower() for n in self._GENERIC_NAMES}

    def _make_title(self, data: Dict) -> str:
        """
        只提取核心名称作为标题，不拼接人名、等级、颁发单位。
        - paper/patent/research/project 用《》包裹
        - competition 保留竞赛全名（不含奖项名）
        - certificate/其他 直接用证书名
        """
        category = (data.get("category") or "").strip()
        cert_name = (data.get("certificate_name") or "").strip()
        paper_title = (data.get("paper_title") or "").strip()
        project_name = (data.get("project_name") or "").strip()
        award = (data.get("award_rank") or data.get("award") or "").strip()

        if category == "paper":
            core = paper_title or cert_name
            return f"《{core}》" if core else "学术论文"

        if category == "patent":
            return f"《{cert_name}》" if cert_name else "专利/软件著作权证书"

        if category in ("research", "project"):
            core = project_name or cert_name
            return f"《{core}》" if core else ("科研成果证书" if category == "research" else "项目证书")

        if category == "competition":
            # 竞赛保留赛事全名；名称泛化时降级用奖项名
            return cert_name if not self._is_generic(cert_name) else (award or "竞赛获奖证书")

        # certificate / certification / 其他兜底
        if not self._is_generic(cert_name):
            return cert_name
        # cert_name 是泛化词，依次尝试 award_rank → award_reason 里的核心词 → 兜底
        if award and award not in {"通过", "参与", "合格", "及格"}:
            return award
        award_reason = (data.get("award_reason") or "").strip()
        if award_reason:
            # 尝试提取"评为/荣获/授予 XXX"之后的核心称号
            honor_match = re.search(r'(?:评为|荣获|授予|称号为|获得)["\s"「『]?([^，。；、！？\s"」』]{2,15})', award_reason)
            if honor_match:
                return honor_match.group(1).strip()
            # 兜底：取第一段（第一个标点前），最多 15 字
            punct_match = re.search(r'[，。；、！？]', award_reason)
            short = award_reason[:punct_match.start()] if punct_match else award_reason[:15]
            if len(short) >= 3:
                return short
        return "荣誉证书"

    def validate_recognition_result(self, result: Dict) -> Dict:
        """
        Validate and clean the recognition result.
        加入智能标题生成，确保标题不会停留在"荣誉证书"等泛化词汇。
        二阶段 OCR：对 paper 类型走专属校验与清洗逻辑。

        Args:
            result: Recognition result dictionary

        Returns:
            Validated and cleaned result
        """
        if not result.get("success"):
            return result

        data = result.get("data", {})
        doc_type = data.get("document_type", "certificate")

        # ── Paper type: dedicated validation & cleaning ──
        if doc_type == "paper":
            has_paper_info = bool(data.get("paper_title") or data.get("journal_name"))
            if not has_paper_info:
                return {
                    "success": False,
                    "error": "Missing paper info: paper_title or journal_name is required",
                    "data": data
                }

            authors = data.get("authors") or []
            first_author = (data.get("first_author") or "").strip()
            if not first_author and isinstance(authors, list) and authors:
                first_author = authors[0]

            paper_title = (data.get("paper_title") or "").strip()
            journal_name = (data.get("journal_name") or "").strip()

            generated_title = self._make_title(data)

            cleaned_data = {
                "document_type": "paper",
                "title": generated_title,
                "paper_title": paper_title,
                "journal_name": journal_name,
                "journal_level": data.get("journal_level"),
                "publish_status": data.get("publish_status"),
                "publish_date": data.get("publish_date"),
                "authors": authors if isinstance(authors, list) else [],
                "first_author": first_author,
                "author_order": data.get("author_order"),
                "doi": data.get("doi"),
                "volume": data.get("volume"),
                "issue": data.get("issue"),
                "pages": data.get("pages"),
                "issn": data.get("issn"),
                "issuing_organization": (data.get("issuing_organization") or "").strip(),
                # 英文论文中文映射字段
                "paper_title_cn": data.get("paper_title_cn"),
                "journal_name_cn": data.get("journal_name_cn"),
                "authors_cn": data.get("authors_cn"),
                "first_author_cn": data.get("first_author_cn"),
                "issuing_organization_cn": data.get("issuing_organization_cn"),
                # Compatibility fields used by existing frontend
                "category": "paper",
                "certificate_name": paper_title or "学术论文",
                "recognition_time": data.get("recognition_time"),
                "model_used": data.get("model_used"),
                "confidence": data.get("confidence")
            }

            return {
                "success": True,
                "data": cleaned_data,
                "usage": result.get("usage", {})
            }

        # ── Certificate type: existing validation ──
        # 放宽校验：只要有识别内容就继续处理，由智能标题生成兜底
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

        # 统一调用 _make_title 生成标题
        cleaned_data["title"] = self._make_title(data)

        return {
            "success": True,
            "data": cleaned_data,
            "usage": result.get("usage", {})
        }

    def _get_prompt_competition(self) -> str:
        return """请识别这张竞赛/学科竞赛获奖证书，提取以下信息。

【返回格式】严格按照以下JSON返回，不要有其他文字：

{
    "certificate_name": "赛事完整名称（如：第十六届全国大学生数学建模竞赛）",
    "award_rank": "具体奖项（如：一等奖、金奖、优胜奖）",
    "award_level": "奖项级别（国家级/省部级/校级/院级）",
    "recipient_name": "个人获奖者姓名（团队获奖则填null）",
    "team_members": ["团队成员姓名数组，团队获奖时填写，个人则为空数组"],
    "advisors": ["指导教师姓名数组"],
    "issuing_organization": "颁奖机构完整名称",
    "issue_date": "颁奖日期（格式：YYYY-MM-DD）",
    "certificate_number": "证书编号（如有）",
    "additional_info": "其他备注信息"
}

【注意】
- certificate_name 必须是赛事全称，禁止填"荣誉证书"等泛指词
- 团队获奖时 recipient_name 填 null，team_members 列出所有成员
- 无法识别的字段填 null"""

    def _get_prompt_patent(self) -> str:
        return """请识别这张专利证书或软件著作权证书，提取以下信息。

【返回格式】严格按照以下JSON返回，不要有其他文字：

{
    "patent_name": "专利名称/发明名称/软件名称（完整名称）",
    "patent_number": "专利号或登记号，完整提取（如：ZL 2023 1 0123456.X 或 2023SR0123456）",
    "patent_type": "专利类型（发明专利/实用新型专利/外观设计专利/软件著作权）",
    "award_level": "级别，根据颁发机构判断：国家知识产权局颁发→填'国家级'，省级知识产权局→填'省级'，其他→填null",
    "inventors": ["发明人/设计人/著作权人姓名数组"],
    "patent_holder": "专利权人/著作权人单位名称",
    "issue_date": "授权公告日/发证日期（格式：YYYY-MM-DD）",
    "issuing_organization": "颁发机构完整名称（如：国家知识产权局、中华人民共和国国家版权局）",
    "application_date": "申请日（格式：YYYY-MM-DD，如有）",
    "additional_info": "其他备注"
}

【注意】
- patent_name 必须是完整的发明/作品名称
- patent_number 必须完整提取，包括前缀（ZL/CN）和后缀（A/B/.X等）
- award_level：国家知识产权局/国家版权局颁发的一律填"国家级"
- inventors 必须是数组，列出所有发明人
- 无法识别的字段填 null"""

    def _get_prompt_research(self) -> str:
        return """请识别这张科技成果登记证书或科研成果证明，提取以下信息。

【返回格式】严格按照以下JSON返回，不要有其他文字：

{
    "achievement_name": "成果名称（完整名称）",
    "registration_number": "登记号（格式特殊，完整提取）",
    "achievement_type": "成果类型（如：应用技术、基础研究、软科学等）",
    "main_contributors": ["主要完成人员姓名数组（可能多人）"],
    "applicant_unit": "申报单位/完成单位",
    "issuing_organization": "登记机构/颁发单位",
    "issue_date": "发证日期（格式：YYYY-MM-DD）",
    "award_level": "成果级别（国家级/省部级/市级/校级，如有）",
    "additional_info": "其他备注（技术领域、应用范围等）"
}

【注意】
- achievement_name 是成果的核心名称，必须完整提取
- main_contributors 必须是数组，科技成果通常有多个完成人
- registration_number 格式特殊（如陕科成登字[2024]第XXX号），完整提取
- 无法识别的字段填 null"""

    def _get_prompt_project(self) -> str:
        return """请识别这张项目立项/结项证书或创新创业项目获奖证书，提取以下信息。

【返回格式】严格按照以下JSON返回，不要有其他文字：

{
    "project_name": "项目完整名称",
    "award_rank": "获奖等级（金奖/银奖/铜奖/优秀奖/一等奖等，如有）",
    "project_level": "项目级别（国家级/省级/校级/院级）",
    "team_leader": "项目负责人/队长姓名",
    "team_members": ["全体团队成员姓名数组（含负责人）"],
    "advisors": ["指导教师姓名数组"],
    "issuing_organization": "颁发机构完整名称",
    "issue_date": "颁发日期（格式：YYYY-MM-DD）",
    "project_source": "项目来源（如：大学生创新创业训练计划、互联网+大学生创新创业大赛等）",
    "additional_info": "其他备注"
}

【注意】
- project_name 必须是项目的完整名称
- team_members 列出所有成员（包括负责人）
- 无法识别的字段填 null"""

    def _get_prompt_certificate(self) -> str:
        return """请识别这张荣誉证书或职业资格证书，提取以下信息。

【certificate_name 提取规则——最重要】
- 如果证书大标题是"荣誉证书"，必须继续找正文中的【具体荣誉名称】填入 certificate_name
- 例如：证书上写"被评为优秀学生干部" → certificate_name = "优秀学生干部"
- 例如：证书上写"荣获三好学生称号" → certificate_name = "三好学生"
- 例如：证书上写"全国计算机等级考试二级" → certificate_name = "全国计算机等级考试二级"
- 【严禁】填写"荣誉证书""获奖证书""证书"等泛指词作为 certificate_name

【返回格式】严格按照以下JSON返回，不要有其他文字：

{
    "certificate_name": "具体荣誉/证书名称（如：优秀学生干部、三好学生、计算机等级证书二级）",
    "recipient_name": "获奖人/持证人姓名",
    "award_reason": "正文完整描述（如：在2024-2025学年表现优秀，被评为优秀学生干部）",
    "award_rank": "等级/评定结果（如：优秀、良好、二级、通过；若无则填null）",
    "issuing_organization": "颁发单位完整名称",
    "issue_date": "颁发日期（格式：YYYY-MM-DD）",
    "certificate_number": "证书编号（如有）",
    "valid_period": "有效期（如有，如：长期/2026-12-31）",
    "additional_info": "其他备注"
}

【注意】
- 无法识别的字段填 null"""

    def recognize_by_type(self, image_path: str, cert_type: str) -> Dict:
        """
        按成果类型使用专属提示词识别证书。

        Args:
            image_path: 证书图片路径
            cert_type: 成果类型，可选值：competition/patent/research/project/certificate/paper

        Returns:
            识别结果字典
        """
        prompt_map = {
            "competition": self._get_prompt_competition,
            "patent": self._get_prompt_patent,
            "research": self._get_prompt_research,
            "project": self._get_prompt_project,
            "certificate": self._get_prompt_certificate,
            "certification": self._get_prompt_certificate,
        }

        # paper 类型走原有专属路径
        if cert_type == "paper":
            return self.recognize_paper(image_path)

        prompt_fn = prompt_map.get(cert_type, self._get_prompt_certificate)
        prompt = prompt_fn()

        try:
            image_path = self._preprocess_image(image_path)
            image_base64 = self.encode_image_to_base64(image_path)
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        },
                        {"type": "text", "text": prompt}
                    ]
                }],
                temperature=0.1,
                max_tokens=1000
            )

            content = completion.choices[0].message.content
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()

            cert_data = json.loads(content)
            cert_data["document_type"] = cert_type
            cert_data["category"] = cert_type
            cert_data["recognition_time"] = datetime.utcnow().isoformat()
            cert_data["model_used"] = self.model_name
            cert_data["confidence"] = "high"

            return {
                "success": True,
                "data": cert_data,
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
                "raw_response": content if "content" in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def _infer_patent_level(self, reg_no: str) -> str:
        """根据专利/登记号格式推断级别"""
        if not reg_no:
            return ""
        cleaned = re.sub(r'[\s.\-]', '', reg_no.strip().upper())
        # ZL/CN 前缀 → 国家知识产权局，国家级
        if cleaned.startswith('ZL') or cleaned.startswith('CN'):
            return "国家级"
        # 软件著作权登记号：YYYYSR0000000 格式
        if re.match(r'^\d{4}SR\d{7}$', cleaned):
            return "国家级"
        # 国家级发明/实用新型/外观：YYYYXXNNNXNNNNNNN
        if re.match(r'^\d{4}[A-Z]{2}\d{3}[A-Z]\d{6}$', cleaned):
            return "国家级"
        # 自治区级
        if re.match(r'^\d{4}N\d{3}[A-Z]\d{6}$', cleaned):
            return "自治区级"
        return ""

    def validate_by_type(self, result: Dict, cert_type: str) -> Dict:
        """
        按类型清洗并标准化 recognize_by_type 的结果，
        将各类型专属字段统一映射到前端通用字段。
        """
        if not result.get("success"):
            return result

        data = result.get("data", {})

        if cert_type == "paper":
            return self.validate_recognition_result(result)

        if cert_type == "patent":
            inventors = data.get("inventors") or []
            recipient = "、".join(inventors[:3]) if inventors else ""
            patent_name = (data.get("patent_name") or "").strip()
            patent_number = (data.get("patent_number") or "").strip()
            patent_type = (data.get("patent_type") or "专利").strip()

            # 推断专利等级：优先用 OCR 识别的 award_level，再按登记号格式推断
            raw_level = (data.get("award_level") or "").strip()
            if not raw_level or raw_level == "待人工确认":
                raw_level = self._infer_patent_level(patent_number)

            # patent_name 映射到 certificate_name 供 _make_title 使用
            data["certificate_name"] = patent_name
            title = self._make_title(data)

            cleaned = {
                "document_type": "patent",
                "category": "patent",
                "title": title,
                "certificate_name": patent_name,
                "recipient_name": recipient or None,
                "team_members": inventors,
                "advisors": [],
                "issuing_organization": (data.get("issuing_organization") or "").strip(),
                "issue_date": data.get("issue_date"),
                "certificate_number": patent_number,
                "award_level": raw_level or None,
                "award": patent_type,  # 专利类型（发明/实用新型/外观设计）
                # 专利专属字段
                "patent_name": patent_name,
                "patent_number": patent_number,
                "patent_type": patent_type,
                "patent_holder": data.get("patent_holder"),
                "application_date": data.get("application_date"),
                "additional_info": data.get("additional_info"),
                "recognition_time": data.get("recognition_time"),
                "model_used": data.get("model_used"),
            }
            return {"success": True, "data": cleaned, "usage": result.get("usage", {})}

        if cert_type == "research":
            contributors = data.get("main_contributors") or []
            achievement_name = (data.get("achievement_name") or "").strip()
            reg_number = (data.get("registration_number") or "").strip()

            data["certificate_name"] = achievement_name
            data["project_name"] = data.get("project_name") or achievement_name
            title = self._make_title(data)

            cleaned = {
                "document_type": "research",
                "category": "research",
                "title": title,
                "certificate_name": achievement_name,
                "recipient_name": contributors[0] if contributors else None,
                "team_members": contributors,
                "advisors": [],
                "issuing_organization": (data.get("issuing_organization") or "").strip(),
                "issue_date": data.get("issue_date"),
                "certificate_number": reg_number,
                "award_level": data.get("award_level"),
                "award": data.get("achievement_type"),
                # 科研专属字段
                "achievement_name": achievement_name,
                "registration_number": reg_number,
                "achievement_type": data.get("achievement_type"),
                "applicant_unit": data.get("applicant_unit"),
                "additional_info": data.get("additional_info"),
                "recognition_time": data.get("recognition_time"),
                "model_used": data.get("model_used"),
            }
            return {"success": True, "data": cleaned, "usage": result.get("usage", {})}

        if cert_type == "project":
            members = data.get("team_members") or []
            project_name = (data.get("project_name") or "").strip()
            leader = (data.get("team_leader") or "").strip()

            title = self._make_title(data)

            cleaned = {
                "document_type": "project",
                "category": "project",
                "title": title,
                "certificate_name": project_name,
                "recipient_name": leader or None,
                "team_members": members,
                "advisors": data.get("advisors") or [],
                "issuing_organization": (data.get("issuing_organization") or "").strip(),
                "issue_date": data.get("issue_date"),
                "certificate_number": None,
                "award_level": data.get("project_level"),
                "award": data.get("award_rank"),
                # 项目专属字段
                "project_name": project_name,
                "team_leader": leader,
                "project_source": data.get("project_source"),
                "additional_info": data.get("additional_info"),
                "recognition_time": data.get("recognition_time"),
                "model_used": data.get("model_used"),
            }
            return {"success": True, "data": cleaned, "usage": result.get("usage", {})}

        if cert_type in ("competition",):
            team = data.get("team_members") or []
            recipient = data.get("recipient_name")
            cert_name = (data.get("certificate_name") or "").strip()
            award = (data.get("award_rank") or "").strip()
            level = (data.get("award_level") or "").strip()

            title = self._make_title(data)

            cleaned = {
                "document_type": "competition",
                "category": "competition",
                "title": title,
                "certificate_name": cert_name,
                "recipient_name": recipient,
                "team_members": team,
                "advisors": data.get("advisors") or [],
                "issuing_organization": (data.get("issuing_organization") or "").strip(),
                "issue_date": data.get("issue_date"),
                "certificate_number": data.get("certificate_number"),
                "award_level": level,
                "award": award,
                "additional_info": data.get("additional_info"),
                "recognition_time": data.get("recognition_time"),
                "model_used": data.get("model_used"),
            }
            return {"success": True, "data": cleaned, "usage": result.get("usage", {})}

        # certificate / certification / 其他兜底
        cert_name = (data.get("certificate_name") or "").strip()
        recipient = (data.get("recipient_name") or "").strip()
        award_reason = (data.get("award_reason") or "").strip()

        title = self._make_title(data)

        cleaned = {
            "document_type": "certificate",
            "category": "certificate",
            "title": title,
            "certificate_name": cert_name,
            "recipient_name": recipient or None,
            "team_members": [],
            "advisors": [],
            "issuing_organization": (data.get("issuing_organization") or "").strip(),
            "issue_date": data.get("issue_date"),
            "certificate_number": data.get("certificate_number"),
            "award_level": None,
            "award": data.get("award_rank"),
            "award_reason": award_reason,
            "valid_period": data.get("valid_period"),
            "additional_info": data.get("additional_info"),
            "recognition_time": data.get("recognition_time"),
            "model_used": data.get("model_used"),
        }
        return {"success": True, "data": cleaned, "usage": result.get("usage", {})}


# Create a singleton instance
certificate_recognition_service_openai = CertificateRecognitionServiceOpenAI()
