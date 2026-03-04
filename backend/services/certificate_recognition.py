"""
Certificate Recognition Service
Uses Alibaba Cloud Bailian (Qwen-plus) to recognize and extract information from achievement certificates
"""

import base64
import json
import io
from typing import Dict, Optional
from datetime import datetime
import httpx
from PIL import Image
from config import settings


class CertificateRecognitionService:
    """Service for recognizing and extracting information from certificates using AI"""
    
    def __init__(self):
        self.api_key = settings.QWEN_API_KEY
        self.model_name = settings.QWEN_MODEL_NAME
        self.api_url = settings.QWEN_BASE_URL
        
    def compress_image(self, image_path: str, max_size: int = 1600, quality: int = 85) -> bytes:
        """
        Compress and resize image for faster OCR API transmission
        
        Args:
            image_path: Path to the image file
            max_size: Maximum dimension for width or height
            quality: JPEG quality (1-100)
            
        Returns:
            Compressed image bytes
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB (in case of RGBA/P mode)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate new size while maintaining aspect ratio
                width, height = img.size
                if width > max_size or height > max_size:
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save to buffer
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                return buffer.getvalue()
        except Exception as e:
            print(f"Error compressing image: {e}")
            # Fallback to reading raw file if compression fails
            with open(image_path, "rb") as f:
                return f.read()

    def encode_image_to_base64(self, image_path: str) -> str:
        """
        Encode image file to base64 string with optimization
        """
        image_bytes = self.compress_image(image_path)
        return base64.b64encode(image_bytes).decode('utf-8')
    
    async def recognize_certificate(self, image_path: str) -> Dict:
        """
        Recognize certificate and extract structured information
        
        Args:
            image_path: Path to the certificate image
            
        Returns:
            Dictionary containing extracted certificate information
        """
        try:
            # Encode image to base64 (with compression)
            image_base64 = self.encode_image_to_base64(image_path)
            
            # Prepare the prompt for certificate recognition
            prompt = """请仔细分析这张图片（通常是获奖证书、奖状、成果证明、学术论文发表证明或科研项目证明），并尽可能准确地提取以下关键信息。
如果图片不是证书，请尽量从中分析出相关性最高的内容。

【极其重要原则】
- certificate_name 字段必须提取证书/证明中的【具体活动/项目/论文/竞赛名称】，例如："第十六届全国大学生数学建模竞赛"、"XYZ期刊发表论文：基于深度学习的图像识别研究"
- 【严格禁止】将 certificate_name 设为 "荣誉证书"、"获奖证书"、"证书"、"奖状" 等纯泛指词汇。即便证书上印有这些字样，也必须寻找具体的活动名称、论文名称或项目名称来填充此字段。

需要提取的字段及说明：
1. **certificate_name** (证书核心活动名称): 提取证书中最核心的具体内容名称，如比赛名称、论文题目、项目名称、职业资格证书全称等。【禁止使用"荣誉证书"等泛化词作为此字段值】
2. **recipient_name** (获得者姓名): 证书上表彰的人员姓名（包括团队名称）。
3. **issuing_organization** (颁发单位): 落款处的盖章单位或文字，可能有多个，用顿号分隔。
4. **issue_date** (颁发日期): 格式必须为 "YYYY-MM-DD"（如 2024-05-20）。如果未找到年份，默认使用当前年份。
5. **certificate_number** (证书编号): 通常位于角落或正文中。
6. **award_level** (奖项等级/证书级别): 必须从以下选项中推断最接近的一个：
   - "国家级" (出现"全国"、"国际"、"教育部"等)
   - "省部级" (出现"省"、"厅"、"自治区"等)
   - "校级" (出现"学校"、"大学"、"学院"且无更高行政单位)
   - "院级" (出现"二级学院"、"系"等)
7. **category** (成果类别): 请根据内容推断，从以下选项中选择一个最合适的：
   - "competition" (学科竞赛/技能大赛)
   - "research" (科研成果)
   - "project" (创新创业项目)
   - "paper" (学术论文发表)
   - "patent" (专利/软件著作权)
   - "certificate" (职业资格证书/荣誉表彰/其他)
8. **award** (具体奖项/结论): 如"一等奖"、"二等奖"、"优秀奖"、"金奖"等；若为论文发表则填"已发表"；若为资格证，可填"通过"；若为科研项目参与则填"参与"。
9. **advisor_name** (指导教师): 证书上如有"指导教师"、"指导老师"等字样，请提取其姓名。如有多个用逗号分隔。
10. **paper_title** (论文题目): 若为论文类证书，提取完整的论文题目。
11. **journal_name** (期刊/会议名称): 若为论文类证书，提取期刊名称或会议名称及级别（如"SCI"、"EI"、"核心期刊"等）。
12. **project_name** (项目名称): 若为科研项目/创新创业类，提取完整的项目名称。
13. **role** (承担角色): 若为团队成果，提取获奖人在团队中的具体角色（如"项目负责人"、"第一作者"、"主要参与者"等）。
14. **location** (活动/发表地点): 比赛举办地、期刊出版地等，如果有的话。

请严格以JSON格式返回，不要包含Markdown格式（如```json ... ```），直接返回JSON对象。

JSON 模板（包含所有可能字段，无法识别的填null）：
{
    "certificate_name": "第十六届全国大学生数学建模竞赛",
    "recipient_name": "张三",
    "issuing_organization": "全国大学生数学建模竞赛组委会",
    "issue_date": "2024-11-20",
    "certificate_number": null,
    "award_level": "国家级",
    "category": "competition",
    "award": "一等奖",
    "advisor_name": "李老师",
    "paper_title": null,
    "journal_name": null,
    "project_name": null,
    "role": null,
    "location": null,
    "additional_info": "其他备注"
}

如果字段完全无法识别，请填 null 或空字符串，不要编造。"""
            
            # Call Qwen API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "image": f"data:image/jpeg;base64,{image_base64}"
                                },
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                }
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract the response text
                if "output" in result and "choices" in result["output"]:
                    content = result["output"]["choices"][0]["message"]["content"]
                    
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
                    
                    try:
                        certificate_data = json.loads(content)
                    except json.JSONDecodeError:
                        # Fallback: try to find the first '{' and last '}'
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        if start != -1 and end != -1:
                            certificate_data = json.loads(content[start:end])
                        else:
                            raise Exception("Could not parse JSON from model output")
                    
                    # Add metadata
                    certificate_data["recognition_time"] = datetime.utcnow().isoformat()
                    certificate_data["model_used"] = self.model_name
                    certificate_data["confidence"] = "high"
                    
                    return {
                        "success": True,
                        "data": certificate_data,
                        "raw_response": content
                    }
                else:
                    return {
                        "success": False,
                        "error": "Unexpected response format from API",
                        "raw_response": result
                    }
                    
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse JSON response: {str(e)}",
                "raw_response": content if 'content' in locals() else None
            }
        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def batch_recognize_certificates(self, image_paths: list[str]) -> list[Dict]:
        """
        Batch recognize multiple certificates
        
        Args:
            image_paths: List of paths to certificate images
            
        Returns:
            List of dictionaries containing extracted information for each certificate
        """
        results = []
        for image_path in image_paths:
            result = await self.recognize_certificate(image_path)
            results.append(result)
        return results
    
    def _generate_smart_title(self, data: Dict) -> str:
        """
        根据OCR识别出的各字段，智能生成一个具体、有描述性的证书标题。
        标题应反映证书性质，包含获奖人、成果描述、颁发机构等关键信息。

        Args:
            data: OCR识别的原始字段字典

        Returns:
            生成的标题字符串
        """
        category = (data.get("category") or "").strip()
        cert_name = (data.get("certificate_name") or "").strip()
        recipient = (data.get("recipient_name") or "").strip()
        award = (data.get("award") or "").strip()
        award_level = (data.get("award_level") or "").strip()
        issuer = (data.get("issuing_organization") or "").strip()
        paper_title = (data.get("paper_title") or "").strip()
        journal_name = (data.get("journal_name") or "").strip()
        project_name = (data.get("project_name") or "").strip()
        role = (data.get("role") or "").strip()
        location = (data.get("location") or "").strip()
        advisor = (data.get("advisor_name") or "").strip()

        generic_names = {"荣誉证书", "获奖证书", "奖状", "证书", "证明", "奖励证书", "优秀证书"}
        is_generic_cert_name = cert_name in generic_names or not cert_name

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

        # ── 5. 学科竞赛类 ──
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
            core_desc = "".join(parts) if parts else "学科竞赛"
            if recipient:
                title = f"{recipient}在{core_desc}中获奖证明"
            else:
                title = f"{core_desc}获奖证明"
            if advisor:
                title += f"（指导教师：{advisor}）"
            if location:
                title += f"（地点：{location}）"
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
        调用智能标题生成，确保标题具体、有描述性，而非统一使用"荣誉证书"等泛化词。

        Args:
            result: Recognition result dictionary

        Returns:
            Validated and cleaned result
        """
        if not result.get("success"):
            return result

        data = result.get("data", {})

        # Clean and normalize data, mapping AI field names to frontend expected names
        cleaned_data = {
            "title": "",  # 将由智能标题生成填入
            "recipient_name": data.get("recipient_name", ""),
            "issuing_organization": data.get("issuing_organization", ""),
            "date": data.get("issue_date"),  # Map issue_date to date
            "certificate_number": data.get("certificate_number"),
            "award_level": data.get("award_level"),
            "category": data.get("category"),
            "suggested_type": data.get("category"),  # Frontend uses suggested_type
            "award": data.get("award", ""),
            "advisor_name": data.get("advisor_name", ""),
            # 新增扩展字段，传递给前端供显示参考
            "paper_title": data.get("paper_title", ""),
            "journal_name": data.get("journal_name", ""),
            "project_name": data.get("project_name", ""),
            "role": data.get("role", ""),
            "location": data.get("location", ""),
            "additional_info": data.get("additional_info"),
            "recognition_time": data.get("recognition_time"),
            "model_used": data.get("model_used")
        }

        # ─── 智能标题生成 ───
        generic_names = {"荣誉证书", "获奖证书", "奖状", "证书", "证明", "奖励证书", "优秀证书"}
        raw_cert_name = (data.get("certificate_name") or "").strip()

        if raw_cert_name and raw_cert_name not in generic_names:
            # AI 识别到了具体名称，使用该名称并补充获奖人和奖项信息使标题更完整
            title = raw_cert_name
            recipient = cleaned_data.get("recipient_name", "").strip()
            award = cleaned_data.get("award", "").strip()
            if award and award not in {"通过", "参与"} and award not in title:
                title = f"{title}——{award}"
            if recipient and recipient not in title:
                title = f"{recipient}在{title}"
            cleaned_data["title"] = title
        else:
            # AI 未能识别具体名称（或返回了泛化词），启用智能标题生成
            cleaned_data["title"] = self._generate_smart_title(data)

        return {
            "success": True,
            "data": cleaned_data,
            "recognized_data": cleaned_data  # Frontend expects recognized_data
        }


# Create a singleton instance
certificate_recognition_service = CertificateRecognitionService()

