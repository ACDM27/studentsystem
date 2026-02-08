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
            prompt = """请仔细分析这张图片（通常是获奖证书、奖状或成果证明），并尽可能准确地提取以下关键信息。
如果图片不是证书，请尽量从中分析出相关性最高的内容。

需要提取的字段及说明：
1. **certificate_name** (证书/活动名称): 请**优先提取具体的比赛名称或活动主题**（如"第六届智警杯大数据技能竞赛"），而不是泛泛的"荣誉证书"、"奖状"。仅在无法找到具体活动名称时才填"荣誉证书"。
2. **recipient_name** (获得者姓名): 证书上表彰的人员姓名（包括团队名称）。
3. **issuing_organization** (颁发单位): 落款处的盖章单位或文字，可能有多个。
4. **issue_date** (颁发日期): 格式必须为 "YYYY-MM-DD"（如 2024-05-20）。如果未找到年份，默认使用当前年份。
5. **certificate_number** (证书编号): 通常位于角落或正文中。
6. **award_level** (奖项等级): 必须从以下选项中推断最接近的一个：
   - "国家级" (出现"全国"、"国际"、"教育部"等)
   - "省部级" (出现"省"、"厅"、"自治区"等)
   - "校级" (出现"学校"、"大学"、"学院"且无更高行政单位)
   - "院级" (出现"二级学院"、"系"等)
7. **category** (获奖类别): 请根据内容推断，从以下选项中选择一个最合适的：
   - "competition" (学科竞赛)
   - "research" (科研成果/论文)
   - "project" (创新创业项目)
   - "paper" (发表论文)
   - "patent" (专利/软著)
   - "certificate" (职业资格证书/其他)
8. **award** (具体奖项): 如"一等奖"、"二等奖"、"优秀奖"、"金奖"、"优胜奖"等。如果是资格证，可填"通过"。
9. **advisor_name** (指导教师): 证书上如有"指导教师"、"指导老师"等字样，请提取其姓名。如有多个用空格分隔。

请严格以JSON格式返回，不要包含Markdown格式（如```json ... ```），直接返回JSON对象。

JSON 模板：
{
    "certificate_name": "内容",
    "recipient_name": "内容",
    "issuing_organization": "内容",
    "issue_date": "YYYY-MM-DD",
    "certificate_number": "内容",
    "award_level": "内容",
    "category": "competition",
    "award": "一等奖",
    "advisor_name": "张三",
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
    
    def validate_recognition_result(self, result: Dict) -> Dict:
        """
        Validate and clean the recognition result
        
        Args:
            result: Recognition result dictionary
            
        Returns:
            Validated and cleaned result
        """
        if not result.get("success"):
            return result
        
        data = result.get("data", {})
        
        # Validate required fields (lax validation to allow partial success)
        # We don't want to fail the whole process just because one field is missing
        
        # Clean and normalize data
        cleaned_data = {
            "title": data.get("certificate_name", "") or data.get("title", ""), # Map certificate_name to title
            "recipient_name": data.get("recipient_name", ""),
            "issuing_organization": data.get("issuing_organization", ""),
            "date": data.get("issue_date"), # Map issue_date to date
            "certificate_number": data.get("certificate_number"),
            "award_level": data.get("award_level"),
            "category": data.get("category"), # Should match frontend enum keys usually
            "suggested_type": data.get("category"), # Frontend uses suggested_type
            "award": data.get("award", ""),
            "advisor_name": data.get("advisor_name", ""),
            "additional_info": data.get("additional_info"),
            "recognition_time": data.get("recognition_time"),
            "model_used": data.get("model_used")
        }
        
        # Ensure title is not empty if possible
        if not cleaned_data["title"] and cleaned_data["award"]:
             cleaned_data["title"] = f"{cleaned_data['award']}证书"
             
        return {
            "success": True,
            "data": cleaned_data,
            "recognized_data": cleaned_data # Frontend expects recognized_data
        }


# Create a singleton instance
certificate_recognition_service = CertificateRecognitionService()

