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

【重要提示】人名识别准确性至关重要，请务必：
1. 仔细辨认每个汉字，特别是人名
2. 对于相似字要特别注意区分（如：华/华、锋/峰、涛/滔等）
3. 如果某个字不确定，请在该人名后标注"(?)"
4. 请多次检查人名是否识别正确

【需要提取的信息】

**基本信息：**
1. 证书名称/奖项名称
2. 主要获奖者姓名（如果是个人）
3. 颁发单位/组织
4. 获奖时间/颁发日期（格式：YYYY-MM-DD，如果只有年月，日期用01）
5. 证书编号（如果有）

**奖项详情：**
6. 奖项等级（如：一等奖、二等奖、三等奖、优秀奖等）
7. 获奖类别/竞赛类型（如：学术竞赛、科技创新、文体活动、创新创业等）
8. 项目名称/作品名称（完整的项目名称）

**人员信息（最重要，请仔细识别）：**
9. 团队成员名单：
   - 请按证书上的顺序列出所有成员
   - 每个人名请仔细辨认，确保准确
   - 注意区分形近字
   - 如果有不确定的字，标注"(?)"

10. 指导老师/指导教师：
   - 可能标注为"指导老师"、"指导教师"、"导师"等
   - 可能有多位，请全部列出
   - 同样要仔细识别人名

**其他信息：**
11. 其他重要信息（如所在学院、班级、特别说明等）

【返回格式】
请严格按照以下JSON格式返回，不要添加任何其他文字：

{
    "certificate_name": "证书/奖项名称",
    "recipient_name": "主要获奖者姓名，团队奖项填null",
    "issuing_organization": "颁发单位",
    "issue_date": "YYYY-MM-DD",
    "certificate_number": "证书编号或null",
    "award_level": "奖项等级",
    "category": "获奖类别",
    "project_name": "完整的项目/作品名称",
    "team_members": ["成员1", "成员2", "成员3"],
    "advisors": ["指导老师1", "指导老师2"],
    "additional_info": "其他重要信息",
    "recognition_confidence": {
        "team_members": "high/medium/low",
        "advisors": "high/medium/low"
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
        
        # Validate required fields
        required_fields = ["certificate_name", "recipient_name", "issuing_organization"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return {
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "data": data
            }
        
        # Clean and normalize data
        cleaned_data = {
            "certificate_name": data.get("certificate_name", "").strip(),
            "recipient_name": data.get("recipient_name", "").strip() if data.get("recipient_name") else None,
            "issuing_organization": data.get("issuing_organization", "").strip(),
            "issue_date": data.get("issue_date"),
            "certificate_number": data.get("certificate_number"),
            "award_level": data.get("award_level"),
            "category": data.get("category"),
            "project_name": data.get("project_name"),
            "team_members": data.get("team_members", []),
            "advisors": data.get("advisors", []),
            "additional_info": data.get("additional_info"),
            "recognition_confidence": data.get("recognition_confidence", {}),  # New field
            "recognition_time": data.get("recognition_time"),
            "model_used": data.get("model_used"),
            "confidence": data.get("confidence")
        }
        
        return {
            "success": True,
            "data": cleaned_data,
            "usage": result.get("usage", {})
        }


# Create a singleton instance
certificate_recognition_service_openai = CertificateRecognitionServiceOpenAI()
