# -*- coding: utf-8 -*-
"""
超简单测试脚本
作者：浮浮酱
直接测试下载+转PDF
"""

import jmcomic
from pathlib import Path
from PIL import Image
import re

def test_simple_download(album_id: str):
    """简单测试下载"""

    print("=" * 60)
    print("JMComic 下载测试（浮浮酱版）")
    print("=" * 60)
    print()

    # 设置下载目录
    download_dir = r"C:\Users\Kindred.C\Downloads\jmcomic_test"
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    print(f"📁 下载目录: {download_dir}")
    print(f"📦 本子ID: {album_id}")
    print()

    # 创建配置
    option = jmcomic.create_option(download_dir)
    option.client.impl = 'api'  # 使用移动端API

    # 下载
    print("📥 开始下载喵～")
    print("⏳ 请耐心等待（可能需要几分钟）...")
    print()

    try:
        jmcomic.download_album(album_id, option)
        print("\n✅ 下载完成喵～")

        # 查找下载的目录
        base_path = Path(download_dir)
        album_dirs = [d for d in base_path.iterdir() if d.is_dir() and album_id in d.name]

        if album_dirs:
            album_dir = album_dirs[0]
            print(f"📂 找到目录: {album_dir.name}")

            # 转换PDF
            print("\n🎨 开始转换PDF...")
            pdf_count = convert_to_pdf(album_dir)

            if pdf_count > 0:
                print(f"\n✅ 成功生成 {pdf_count} 个PDF文件喵～")
                print(f"📍 位置: {album_dir.parent}")

                # 列出文件
                print("\n生成的PDF：")
                for pdf in sorted(album_dir.parent.glob("*.pdf")):
                    size_mb = pdf.stat().st_size / (1024 * 1024)
                    print(f"  📄 {pdf.name} ({size_mb:.1f}MB)")
            else:
                print("\n⚠️ PDF转换失败")
        else:
            print("\n⚠️ 未找到下载目录")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)


def convert_to_pdf(album_dir: Path) -> int:
    """转换为PDF"""
    pdf_count = 0

    for chapter_dir in sorted(album_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue

        try:
            # 获取图片
            images = sorted(
                [f for f in chapter_dir.iterdir()
                 if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}],
                key=lambda x: int(re.search(r'(\d+)', x.stem).group(1))
                              if re.search(r'(\d+)', x.stem) else 0
            )

            if not images:
                continue

            # PDF文件名
            pdf_path = chapter_dir.parent / f"{chapter_dir.name}.pdf"

            if pdf_path.exists():
                print(f"  ⏭️ 已存在: {pdf_path.name}")
                pdf_count += 1
                continue

            print(f"  🎨 转换中: {chapter_dir.name} ({len(images)}张)")

            # 加载图片
            img_list = []
            for img_path in images:
                try:
                    img = Image.open(img_path)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img_list.append(img)
                except Exception as e:
                    print(f"    ⚠️ 图片损坏: {img_path.name}")

            # 保存PDF
            if img_list:
                img_list[0].save(
                    str(pdf_path),
                    "PDF",
                    save_all=True,
                    append_images=img_list[1:],
                    resolution=100.0
                )
                print(f"  ✅ 完成: {pdf_path.name}")
                pdf_count += 1

        except Exception as e:
            print(f"  ❌ 失败: {chapter_dir.name}, {e}")

    return pdf_count


if __name__ == "__main__":
    print("\n")
    print("=" * 60)
    print("   JMComic 本地测试 by 浮浮酱")
    print("=" * 60)
    print()

    # 输入本子ID
    album_id = input("请输入本子ID（例如：123456）: ").strip()

    if not album_id or not album_id.isdigit():
        print("\n❌ ID格式错误（应为纯数字）")
    else:
        print()
        test_simple_download(album_id)

    print()
    input("按回车键退出...")
