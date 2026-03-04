"""
下载管理器（小群简化版）
作者：浮浮酱 ฅ'ω'ฅ
"""

import asyncio
import jmcomic
from pathlib import Path
from typing import Optional, List
import logging
from .converter import ImageToPDFConverter

logger = logging.getLogger(__name__)


class JMDownloadManager:
    """JMComic下载管理器"""

    def __init__(self, config: dict):
        self.config = config
        self.download_dir = Path(config['download_dir'])
        self.download_dir.mkdir(parents=True, exist_ok=True)

        self.converter = ImageToPDFConverter(
            delete_images=config.get('delete_images_after_convert', True)
        )

        self.jm_option = self._create_jm_option()

    def _create_jm_option(self) -> jmcomic.JmOption:
        """创建JMComic配置"""
        option = jmcomic.JmOption.default()
        option.dir_rule.base_dir = str(self.download_dir)

        # 客户端配置
        option.client.impl = self.config.get('client_impl', 'api')

        # 代理配置
        if 'proxy' in self.config:
            option.client.proxies = {
                'http': self.config['proxy'],
                'https': self.config['proxy']
            }

        # 并发配置
        threading = self.config.get('threading', {})
        option.download.threading.album = threading.get('album', 1)
        option.download.threading.photo = threading.get('photo', 2)
        option.download.threading.image = threading.get('image', 5)

        return option

    async def download_and_convert(self, album_id: str) -> Optional[List[Path]]:
        """下载本子并转PDF"""
        try:
            print(f"[下载管理器] 开始下载: {album_id}")
            logger.info(f"[下载管理器] 开始下载: {album_id}")
            print(f"[下载管理器] 下载目录: {self.download_dir}")
            print(f"[下载管理器] 下载目录是否存在: {self.download_dir.exists()}")

            # 确保下载目录存在
            self.download_dir.mkdir(parents=True, exist_ok=True)
            print(f"[下载管理器] 创建目录后是否存在: {self.download_dir.exists()}")

            # 在线程池执行下载
            loop = asyncio.get_event_loop()
            print(f"[下载管理器] 调用 jmcomic.download_album, base_dir={self.jm_option.dir_rule.base_dir}")
            logger.info(f"[下载管理器] 调用 jmcomic.download_album")
            await loop.run_in_executor(
                None,
                jmcomic.download_album,
                album_id,
                self.jm_option
            )

            print(f"[下载管理器] 下载完成: {album_id}")
            logger.info(f"[下载管理器] 下载完成: {album_id}")

            # 查找目录
            print(f"[下载管理器] 查找下载目录: {self.download_dir}")
            print(f"[下载管理器] 目录内容: {list(self.download_dir.iterdir()) if self.download_dir.exists() else '目录不存在'}")
            logger.info(f"[下载管理器] 查找下载目录: {self.download_dir}")
            album_dir = self._find_album_dir(album_id)
            print(f"[下载管理器] 找到目录: {album_dir}")
            logger.info(f"[下载管理器] 找到目录: {album_dir}")

            if not album_dir:
                print(f"[下载管理器] 未找到目录: {album_id}")
                logger.error(f"[下载管理器] 未找到目录: {album_id}")
                return None

            # 转PDF
            print(f"[下载管理器] 开始转换PDF: {album_id}, 目录={album_dir}")
            logger.info(f"[下载管理器] 开始转换PDF: {album_id}, 目录={album_dir}")
            pdf_files = self.converter.convert_album(album_dir)
            print(f"[下载管理器] 转换结果: {len(pdf_files) if pdf_files else 0}个PDF")
            logger.info(f"[下载管理器] 转换结果: {len(pdf_files) if pdf_files else 0}个PDF")

            if not pdf_files:
                print(f"[下载管理器] PDF转换失败: {album_id}")
                logger.error(f"[下载管理器] PDF转换失败: {album_id}")
                return None

            print(f"[下载管理器] 完成: {album_id}, PDF文件={pdf_files}")
            logger.info(f"[下载管理器] 完成: {album_id}, PDF文件={pdf_files}")
            return pdf_files

        except Exception as e:
            print(f"[下载管理器] 异常: {album_id}, {e}")
            logger.error(f"[下载管理器] 异常: {album_id}, {e}", exc_info=True)
            import traceback
            traceback.print_exc()
            return None

    def _find_album_dir(self, album_id: str) -> Optional[Path]:
        """查找本子目录"""
        # 先尝试精确匹配ID
        for item in self.download_dir.iterdir():
            if item.is_dir() and album_id in item.name:
                return item

        # 如果没找到，返回最新创建的目录（假设是刚下载的）
        dirs = [d for d in self.download_dir.iterdir() if d.is_dir()]
        if dirs:
            latest_dir = max(dirs, key=lambda d: d.stat().st_mtime)
            logger.info(f"使用最新目录: {latest_dir.name}")
            return latest_dir

        return None
