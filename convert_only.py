# -*- coding: utf-8 -*-
"""
仅转换PDF脚本
"""

from pathlib import Path
from PIL import Image
import re

def convert_to_pdf(chapter_dir):
    """转换为PDF"""

    print(f"处理目录: {chapter_dir.name[:50]}...")

    # 获取图片
    images = sorted(
        [f for f in chapter_dir.iterdir()
         if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}],
        key=lambda x: int(re.search(r'(\d+)', x.stem).group(1))
                      if re.search(r'(\d+)', x.stem) else 0
    )

    if not images:
        print("  没有找到图片")
        return None

    print(f"  找到 {len(images)} 张图片")

    # PDF路径
    pdf_name = f"{chapter_dir.name}.pdf"
    # 替换非法字符
    pdf_name = pdf_name.replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    pdf_path = chapter_dir.parent / pdf_name

    if pdf_path.exists():
        print(f"  PDF已存在: {pdf_path.name}")
        return pdf_path

    print(f"  正在转换...")

    # 加载图片
    img_list = []
    for i, img_path in enumerate(images, 1):
        try:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_list.append(img)
            if i % 5 == 0:
                print(f"    已加载 {i}/{len(images)}")
        except Exception as e:
            print(f"    跳过损坏图片: {img_path.name}")

    # 保存PDF
    if img_list:
        img_list[0].save(
            str(pdf_path),
            "PDF",
            save_all=True,
            append_images=img_list[1:],
            resolution=100.0
        )
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"  完成! {pdf_path.name} ({size_mb:.1f}MB)")
        return pdf_path
    else:
        print("  没有有效图片")
        return None


if __name__ == "__main__":
    download_dir = Path(r"C:\Users\Kindred.C\Downloads\jmcomic_test")

    print("=" * 60)
    print("PDF转换工具")
    print("=" * 60)
    print()

    for item in download_dir.iterdir():
        if item.is_dir():
            convert_to_pdf(item)

    print()
    print("=" * 60)
    print("转换完成!")
    print("=" * 60)
