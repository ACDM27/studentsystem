"""
Attachment Downloader Service
飞书附件下载服务，复用现有file_manager
"""
from pathlib import Path
from typing import Tuple, Optional
import httpx
from datetime import datetime
import logging
from services.file_manager import file_manager
from services.feishu.feishu_client import FeishuClient

logger = logging.getLogger(__name__)


class AttachmentDownloader:
    """飞书附件下载器"""
    
    def __init__(self, feishu_client: FeishuClient):
        """
        初始化附件下载器
        
        Args:
            feishu_client: 飞书客户端实例
        """
        self.feishu_client = feishu_client
        self.file_manager = file_manager
    
    async def download_and_save(
        self, 
        file_token: str, 
        student_id: int,
        filename_prefix: str = "feishu_cert"
    ) -> Tuple[Optional[str], bool, Optional[str]]:
        """
        下载飞书附件并保存到本地
        
        Args:
            file_token: 飞书文件token
            student_id: 学生ID
            filename_prefix: 文件名前缀
            
        Returns:
            (本地文件URL, 是否成功, 飞书token用于重试)
        """
        try:
            # 步骤1: 下载文件内容
            logger.info(f"开始下载飞书附件: {file_token}")
            file_content = await self.feishu_client.download_file_content(file_token)
            
            if not file_content:
                logger.error(f"下载的文件内容为空: {file_token}")
                return (None, False, file_token)
            
            # 步骤2: 检测文件类型
            file_ext = self._detect_file_extension(file_content)
            
            # 步骤3: 保存到学生目录
            student_dir = Path(self.file_manager.upload_dir) / "certificates" / f"student_{student_id}"
            student_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.{file_ext}"
            file_path = student_dir / filename
            
            # 保存文件
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # 生成相对URL
            relative_url = f"/uploads/certificates/student_{student_id}/{filename}"
            
            logger.info(f"✅ 附件下载成功: {file_token} -> {relative_url}")
            return (relative_url, True, None)
            
        except httpx.HTTPError as e:
            logger.warning(f"⚠️ 网络错误，下载失败: {file_token} - {str(e)}")
            return (None, False, file_token)
        
        except Exception as e:
            logger.error(f"❌ 下载附件失败: {file_token} - {str(e)}")
            return (None, False, file_token)
    
    def _detect_file_extension(self, file_content: bytes) -> str:
        """
        根据文件内容检测文件类型
        
        Args:
            file_content: 文件字节内容
            
        Returns:
            文件扩展名（不含点）
        """
        # 检查文件头（魔数）
        if file_content.startswith(b'\xff\xd8\xff'):
            return 'jpg'
        elif file_content.startswith(b'\x89PNG'):
            return 'png'
        elif file_content.startswith(b'GIF8'):
            return 'gif'
        elif file_content.startswith(b'%PDF'):
            return 'pdf'
        elif file_content.startswith(b'BM'):
            return 'bmp'
        
        # 默认为jpg
        logger.warning("无法检测文件类型，默认使用jpg")
        return 'jpg'
    
    async def batch_download(
        self, 
        file_tokens: list[str], 
        student_id: int
    ) -> list[Tuple[str, Optional[str], bool]]:
        """
        批量下载附件
        
        Args:
            file_tokens: 文件token列表
            student_id: 学生ID
            
        Returns:
            [(file_token, local_url, success), ...]
        """
        results = []
        
        for idx, token in enumerate(file_tokens, 1):
            logger.info(f"批量下载进度: {idx}/{len(file_tokens)}")
            local_url, success, retry_token = await self.download_and_save(
                token, 
                student_id,
                filename_prefix=f"feishu_cert_{idx}"
            )
            results.append((token, local_url, success))
        
        success_count = sum(1 for _, _, success in results if success)
        logger.info(f"批量下载完成: 成功{success_count}/{len(file_tokens)}")
        
        return results


async def retry_failed_downloads(db_session) -> int:
    """
    重试失败的飞书附件下载（后台任务）
    
    Args:
        db_session: 数据库session
        
    Returns:
        成功重试的数量
    """
    from models import BizAchievement
    from config import settings
    
    # 查找需要重试的记录
    failed_records = db_session.query(BizAchievement).filter(
        BizAchievement.feishu_attachment_token.isnot(None),
        BizAchievement.evidence_url.is_(None)
    ).limit(50).all()  # 每次最多重试50个
    
    if not failed_records:
        logger.info("没有需要重试的附件下载")
        return 0
    
    # 初始化飞书客户端和下载器
    feishu_client = FeishuClient(
        settings.FEISHU_APP_ID,
        settings.FEISHU_APP_SECRET
    )
    downloader = AttachmentDownloader(feishu_client)
    
    success_count = 0
    
    for record in failed_records:
        try:
            local_url, success, _ = await downloader.download_and_save(
                record.feishu_attachment_token,
                record.student_id
            )
            
            if success and local_url:
                record.evidence_url = local_url
                record.feishu_attachment_token = None  # 清除token
                success_count += 1
                logger.info(f"✅ 重试成功: Achievement#{record.id}")
            
        except Exception as e:
            logger.error(f"重试失败: Achievement#{record.id} - {str(e)}")
    
    # 提交更新
    db_session.commit()
    
    logger.info(f"重试下载完成: 成功{success_count}/{len(failed_records)}")
    return success_count
