# -*- coding: utf-8 -*-
"""
测试NapCat连接
"""

import requests
import json

print("=" * 60)
print("测试NapCat连接")
print("=" * 60)
print()

# 测试NapCat HTTP接口
url = "http://127.0.0.1:3000/"

try:
    print("1. 测试NapCat HTTP接口...")
    response = requests.get(url, timeout=5)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ NapCat HTTP服务正常")
    print()
except Exception as e:
    print(f"   ✗ 连接失败: {e}")
    print()

# 测试获取登录信息
try:
    print("2. 测试获取登录信息...")
    response = requests.get(url + "get_login_info", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ 已登录")
        print(f"   QQ号: {data.get('data', {}).get('user_id', 'N/A')}")
        print(f"   昵称: {data.get('data', {}).get('nickname', 'N/A')}")
    print()
except Exception as e:
    print(f"   ✗ 获取失败: {e}")
    print()

print("=" * 60)
print("如果上面都成功，说明NapCat工作正常")
print("问题可能在WebSocket配置上")
print("=" * 60)
