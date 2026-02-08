"""
Feishu Client Service
飞书API客户端，封装飞书SDK调用
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化飞书客户端
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        
        # Token缓存
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    async def get_access_token(self) -> str:
        """
        获取tenant_access_token（企业级访问凭证）
        Token有效期2小时，自动缓存和刷新
        
        Returns:
            str: Access token
        """
        # 检查缓存是否有效（提前30分钟刷新）
        now = datetime.now()
        if self._access_token and self._token_expires_at:
            if now < self._token_expires_at - timedelta(minutes=30):
                return self._access_token
        
        # 获取新token
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            result = response.json()
            
            if result.get("code") == 0:
                self._access_token = result["tenant_access_token"]
                # Token有效期2小时
                self._token_expires_at = now + timedelta(hours=2)
                logger.info("飞书Access Token获取成功")
                return self._access_token
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"获取飞书Access Token失败: {error_msg}")
                raise Exception(f"获取飞书Access Token失败: {error_msg}")
    
    async def list_tables(self, app_token: str) -> List[Dict[str, Any]]:
        """
        列出多维表格中的所有数据表
        
        Args:
            app_token: 多维表格的app_token
            
        Returns:
            数据表列表
        """
        token = await self.get_access_token()
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            result = response.json()
            
            if result.get("code") == 0:
                tables = result.get("data", {}).get("items", [])
                return [
                    {
                        "table_id": table.get("table_id"),
                        "name": table.get("name"),
                        "record_count": 0  # 飞书API不直接返回记录数
                    }
                    for table in tables
                ]
            else:
                error_msg = result.get("msg", "Unknown error")
                logger.error(f"获取飞书表格列表失败: {error_msg}")
                raise Exception(f"获取表格列表失败: {error_msg}")
    
    async def get_table_records(
        self, 
        app_token: str, 
        table_id: str,
        page_size: int = 100,
        view_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取数据表的所有记录
        
        Args:
            app_token: 多维表格app_token
            table_id: 数据表table_id
            page_size: 每页记录数（最大500）
            view_id: 可选的视图ID
            
        Returns:
            记录列表
        """
        token = await self.get_access_token()
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        all_records = []
        page_token = None
        has_more = True
        
        while has_more:
            params = {
                "page_size": min(page_size, 500)  # 飞书限制最大500
            }
            if page_token:
                params["page_token"] = page_token
            if view_id:
                params["view_id"] = view_id
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, headers=headers, params=params)
                result = response.json()
                
                if result.get("code") == 0:
                    data = result.get("data", {})
                    items = data.get("items", [])
                    all_records.extend(items)
                    
                    has_more = data.get("has_more", False)
                    page_token = data.get("page_token")
                    
                    logger.info(f"已获取 {len(items)} 条记录，总计 {len(all_records)} 条")
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"获取飞书记录失败: {error_msg}")
                    raise Exception(f"获取记录失败: {error_msg}")
        
        return all_records
    
    async def get_file_download_url(self, file_token: str) -> str:
        """
        获取附件的临时下载链接
        
        Args:
            file_token: 文件token
            
        Returns:
            临时下载URL（有效期约1小时）
        """
        token = await self.get_access_token()
        url = f"{self.base_url}/drive/v1/medias/{file_token}/download"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 飞书下载API会302重定向到真实下载地址
            response = await client.get(url, headers=headers, follow_redirects=False)
            
            if response.status_code in [200, 302]:
                # 302重定向时，Location头包含真实下载地址
                if response.status_code == 302:
                    download_url = response.headers.get("Location")
                    logger.info(f"获取附件下载链接成功: {file_token}")
                    return download_url
                else:
                    # 某些情况下直接返回200，需要从响应体解析
                    result = response.json()
                    if result.get("code") == 0:
                        # 注意：飞书drive API可能直接返回文件内容
                        # 这里返回原始URL供后续下载
                        return url
            
            # 错误处理
            try:
                result = response.json()
                error_msg = result.get("msg", "Unknown error")
            except:
                error_msg = f"HTTP {response.status_code}"
            
            logger.error(f"获取附件下载链接失败: {error_msg}")
            raise Exception(f"获取附件下载链接失败: {error_msg}")
    
    async def download_file_content(self, file_token: str) -> bytes:
        """
        直接下载文件内容
        
        Args:
            file_token: 文件token
            
        Returns:
            文件字节内容
        """
        token = await self.get_access_token()
        url = f"{self.base_url}/drive/v1/medias/{file_token}/download"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=headers, follow_redirects=True)
            
            if response.status_code == 200:
                # 检查Content-Type，确保是文件内容
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    # 可能是错误响应
                    result = response.json()
                    if result.get("code") != 0:
                        error_msg = result.get("msg", "Unknown error")
                        raise Exception(f"下载文件失败: {error_msg}")
                
                logger.info(f"文件下载成功: {file_token}, 大小: {len(response.content)} bytes")
                return response.content
            else:
                raise Exception(f"下载文件失败: HTTP {response.status_code}")
    
    async def test_connection(self) -> bool:
        """
        测试飞书连接是否正常
        
        Returns:
            bool: 连接是否成功
        """
        try:
            token = await self.get_access_token()
            return bool(token)
        except Exception as e:
            logger.error(f"飞书连接测试失败: {str(e)}")
            return False
