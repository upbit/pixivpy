# test_webview_novel.py
import sys
import os
import time
import random

# 添加本地pixivpy路径到sys.path最前面（优先级最高）
local_pixivpy_path = ""  # 替换为您的实际路径
sys.path.insert(0, local_pixivpy_path)

# 现在再导入pixivpy
from pixivpy3 import AppPixivAPI, ByPassSniApi
import json

def test_webview_novel():
    # 使用ByPassSniApi绕过GFW和Cloudflare
    print("="*60)
    print("方案1: 使用ByPassSniApi")
    print("="*60)
    
    api = ByPassSniApi()
    
    # 尝试获取真实IP，如果失败则使用默认hosts
    try:
        hosts_result = api.require_appapi_hosts()
        if hosts_result:
            print(f"✓ 成功解析真实IP: {hosts_result}")
        else:
            print("⚠️  DNS解析失败，使用默认hosts")
    except Exception as e:
        print(f"⚠️  DNS解析出错: {e}，使用默认hosts")
    
    api.set_accept_language("zh-CN,zh;q=0.9,en;q=0.8")
    
    # 需要先登录 - 使用您的refresh_token
    try:
        api.auth(refresh_token="")
        print("✓ 登录成功")
    except Exception as e:
        print(f"✗ 登录失败: {e}")
        return
    
    # 测试用的小说ID
    test_novel_ids = []
    
    for novel_id in test_novel_ids:
        print(f"\n测试小说ID: {novel_id}")
        
        try:
            # 添加随机延迟，避免被检测
            time.sleep(random.uniform(1, 3))
            
            result = api.webview_novel(novel_id=novel_id, raw=False, req_auth=True)
            
            print(f"✓ 获取成功")
            print(f"✓ 返回类型: {type(result)}")
            
            # 打印小说基本信息
            if hasattr(result, 'title'):
                print(f"✓ 标题: {result.title}")
            if hasattr(result, 'user_name'):
                print(f"✓ 作者: {result.userName}")
            if hasattr(result, 'text'):
                text_length = len(result.text) if result.text else 0
                print(f"✓ 内容长度: {text_length} 字符")
                if text_length > 0:
                    print(f"✓ 内容预览: {result.text[:100]}...")
                else:
                    print("⚠️  内容为空")
                    
        except Exception as e:
            print(f"✗ 获取失败: {e}")
            print(f"✗ 错误类型: {type(e)}")

if __name__ == "__main__":
    test_webview_novel()