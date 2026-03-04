"""
PDF 转换器模块（集成 image2pdf）
作者：浮浮酱 ฅ'ω'ฅ
"""

import re
from pathlib import Path
from typing import List, Optional
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageToPDFConverter:
    """图片转PDF转换器"""

    def __init__(self, delete_images: bool = True):
        self.delete_images = delete_images
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}

    def convert_album(self, album_dir: Path) -> List[Path]:
        """转换整个本子的所有章节"""
        logger.info(f"[转换器] 开始转换本子: {album_dir}")
        pdf_files = []

        # 检查目录是否存在
        if not album_dir.exists():
            logger.error(f"[转换器] 目录不存在: {album_dir}")
            return pdf_files

        # 检查是否有子目录（多章节）
        subdirs = [d for d in album_dir.iterdir() if d.is_dir()]
        logger.info(f"[转换器] 找到 {len(subdirs)} 个子目录")

        if subdirs:
            # 多章节：每个子目录是一个章节
            logger.info(f"[转换器] 多章节模式")
            for chapter_dir in sorted(subdirs):
                try:
                    logger.info(f"[转换器] 转换章节: {chapter_dir.name}")
                    pdf_path = self.convert_chapter(chapter_dir)
                    if pdf_path:
                        pdf_files.append(pdf_path)
                        logger.info(f"[转换器] 章节转换成功: {pdf_path}")
                except Exception as e:
                    logger.error(f"[转换器] 章节转换失败: {chapter_dir.name}, {e}", exc_info=True)
        else:
            # 单章节：图片直接在根目录
            logger.info(f"[转换器] 单章节模式: {album_dir.name}")
            try:
                pdf_path = self.convert_chapter(album_dir)
                if pdf_path:
                    pdf_files.append(pdf_path)
                    logger.info(f"[转换器] 单章节转换成功: {pdf_path}")
            except Exception as e:
                logger.error(f"[转换器] 转换失败: {album_dir.name}, {e}", exc_info=True)

        logger.info(f"[转换器] 转换完成，共 {len(pdf_files)} 个PDF")
        return pdf_files

    def convert_chapter(self, chapter_dir: Path) -> Optional[Path]:
        """转换单个章节为PDF"""
        try:
            images = self._get_sorted_images(chapter_dir)

            if not images:
                logger.warning(f"章节目录为空: {chapter_dir.name}")
                return None

            pdf_path = chapter_dir.parent / f"{chapter_dir.name}.pdf"

            if pdf_path.exists():
                logger.info(f"PDF已存在: {pdf_path.name}")
                return pdf_path

            logger.info(f"转换PDF: {pdf_path.name} ({len(images)}张)")

            self._images_to_pdf(images, pdf_path)

            if self.delete_images:
                self._cleanup_images(chapter_dir)

            logger.info(f"PDF完成: {pdf_path.name}")
            return pdf_path

        except Exception as e:
            logger.error(f"PDF转换失败: {chapter_dir.name}, {e}")
            return None

    def _get_sorted_images(self, directory: Path) -> List[Path]:
        """获取排序后的图片"""
        images = [
            f for f in directory.iterdir()
            if f.is_file() and f.suffix.lower() in self.supported_formats
        ]

        def extract_number(path: Path) -> int:
            match = re.search(r'(\d+)', path.stem)
            return int(match.group(1)) if match else 0

        return sorted(images, key=extract_number)

    def _images_to_pdf(self, image_paths: List[Path], output_pdf: Path):
        """图片转PDF（内存优化）"""
        img_list = []

        for img_path in image_paths:
            try:
                img = Image.open(img_path)

                # 转RGB
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        rgb_img.paste(img, mask=img.split()[-1])
                    else:
                        rgb_img.paste(img)
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                img_list.append(img)

            except Exception as e:
                logger.warning(f"图片失败: {img_path.name}, {e}")

        if not img_list:
            raise ValueError("没有有效图片")

        img_list[0].save(
            str(output_pdf),
            "PDF",
            save_all=True,
            append_images=img_list[1:],
            resolution=100.0
        )

    def _cleanup_images(self, chapter_dir: Path):
        """清理原图片"""
        try:
            for img_path in chapter_dir.iterdir():
                if img_path.is_file() and img_path.suffix.lower() in self.supported_formats:
                    img_path.unlink()

            if not any(chapter_dir.iterdir()):
                chapter_dir.rmdir()

        except Exception as e:
            logger.error(f"清理失败: {e}")
