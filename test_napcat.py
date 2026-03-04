# -*- coding: utf-8 -*-
"""
测试NapCat连接（简化版）
"""

import requests

print("=" * 60)
print("测试NapCat连接")
print("=" * 60)
print()

url = "http://127.0.0.1:3000/"

try:
    print("1. 测试HTTP接口...")
    r = requests.get(url, timeout=5)
    print(f"   状态码: {r.status_code}")
    if r.status_code == 200:
        print("   [OK] HTTP服务正常")
    print()
except Exception as e:
    print(f"   [ERROR] 连接失败: {e}")
    print()

try:
    print("2. 获取登录信息...")
    r = requests.get(url + "get_login_info", timeout=5)
    if r.status_code == 200:
        data = r.json()
        user_id = data.get('data', {}).get('user_id', 'N/A')
        nickname = data.get('data', {}).get('nickname', 'N/A')
        print(f"   [OK] 已登录")
        print(f"   QQ号: {user_id}")
        print(f"   昵称: {nickname}")
    print()
except Exception as e:
    print(f"   [ERROR] 获取失败: {e}")
    print()

try:
    print("3. 测试发送消息API...")
    print("   提示: 如果能私聊给自己发消息，说明功能正常")
    print()
except Exception as e:
    pass

print("=" * 60)
print("结论:")
print("  如果上面都OK，NapCat工作正常")
print("  问题在WebSocket配置")
print("=" * 60)
