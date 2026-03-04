"""
测试下载功能（不依赖QQ）
作者：浮浮酱 ฅ'ω'ฅ
"""

import asyncio
import yaml
from pathlib import Path
from core.downloader import JMDownloadManager


async def test_download():
    """测试下载"""
    print("=" * 60)
    print("JMComic 下载测试")
    print("=" * 60)
    print()

    # 加载配置
    config_path = Path(__file__).parent / "config.yml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 创建管理器
    manager = JMDownloadManager(config['jmcomic'])

    # 测试下载
    album_id = input("请输入本子ID（测试用）: ").strip()

    if not album_id or not album_id.isdigit():
        print("❌ ID格式错误")
        return

    print(f"\n📥 开始下载: {album_id}")
    print("⏳ 请耐心等待...\n")

    pdf_files = await manager.download_and_convert(album_id)

    if pdf_files:
        print(f"\n✅ 下载成功！共{len(pdf_files)}个PDF")
        print("\n生成的文件：")
        for i, pdf in enumerate(pdf_files, 1):
            file_size = pdf.stat().st_size / (1024 * 1024)
            print(f"  [{i}] {pdf.name} ({file_size:.1f}MB)")
        print(f"\n保存位置: {pdf_files[0].parent}")
    else:
        print("\n❌ 下载失败")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(test_download())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    input("\n按回车键退出...")
