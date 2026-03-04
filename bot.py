"""
JMComic QQ机器人 - 主程序
作者：浮浮酱 ฅ'ω'ฅ
小群专用版
"""

# 修复 Windows 编码问题
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from pathlib import Path

# 初始化
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
nonebot.load_plugins("plugins")

# 启动信息
@driver.on_startup
async def startup():
    print("=" * 60)
    print("JMComic QQ Bot 启动成功")
    print("作者：浮浮酱")
    print("=" * 60)
    print("\n可用命令:")
    print("  /jm <本子ID> - 下载本子")
    print("  /jm status - 查看状态")
    print("  @机器人 <数字ID> - 智能识别\n")


if __name__ == "__main__":
    nonebot.run()
