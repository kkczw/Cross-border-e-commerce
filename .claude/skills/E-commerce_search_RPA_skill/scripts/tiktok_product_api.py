#!/usr/bin/env python3
import sys, time, json
from datetime import datetime
from DrissionPage import ChromiumPage

def print_log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    keywords = sys.argv[1]
    brand = sys.argv[2] if len(sys.argv) > 2 else ""
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    print_log("Task Status: running")
    try:
        # 接管本地浏览器
        page = ChromiumPage()
        search_term = f"{brand} {keywords}".strip()
        
        # 访问 TikTok 搜索页
        page.get(f'https://www.tiktok.com/search?q={search_term}')
        page.wait.load_start()
        
        # ==========================================
        # 【核心升级：滑动验证码防御与人工接管机制】
        # ==========================================
        print_log("正在检查页面状态，如果浏览器弹出【滑动验证码】，请直接手动完成滑动...")
        
        # 循环检测页面是否顺利加载出 "Shop" (商品) 选项卡
        wait_time = 0
        shop_tab = None
        
        while wait_time < 60: # 给人工预留最多 60 秒的滑动时间
            # 兼容英文版(Shop)和中文版(商品)的标签
            shop_tab = page.ele('text:Shop', timeout=2) or page.ele('text:商品', timeout=2)
            
            if shop_tab:
                print_log("✅ 成功进入搜索结果页，未被拦截或已通过验证！")
                shop_tab.click()
                time.sleep(3) # 等待商品列表渲染
                break
            else:
                print_log(f"⚠️ 脚本被卡住 (可能遇到了滑动验证码)。请在浏览器中手动滑一下！(已等待 {wait_time} 秒)")
                time.sleep(3)
                wait_time += 3
                
        if not shop_tab:
             print_log("❌ 等待验证超时或页面结构发生变化，脚本退出。")
             sys.exit(1)
             
        # ==========================================

        extracted_data = []

        for current_page in range(1, max_pages + 1):
            print_log(f"Task Status: running (Scraping TikTok page {current_page})")
            
            # 向下滚动加载更多数据
            page.scroll.down(500)
            time.sleep(2)
            
            # TikTok 的商品卡片 - 使用多种备用定位方案
            # 方案1: 搜索结果商品卡片
            items = list(page.eles('@data-e2e=search-shop-card'))
            print_log(f"方案1找到 {len(items)} 个商品")
            
            # 方案2: 使用通用的商品容器选择器
            if not items:
                items = list(page.eles('.css-1goymlf-DivProductCardContainer'))
                print_log(f"方案2找到 {len(items)} 个商品")
            
            # 方案3: 快速查找包含价格的链接元素
            if not items:
                print_log("尝试使用备用元素定位方案...")
                # 只查找前500个div以提高性能
                all_divs = list(page.eles('tag:div'))[:500]
                items = [d for d in all_divs if d.ele('text:$', timeout=0.1)]
                print_log(f"方案3找到 {len(items)} 个商品")

            for item in items:
                # 尝试抓取标题
                title_ele = item.ele('@data-e2e=search-shop-title', timeout=0.2)
                if not title_ele:
                    # 尝试找h2或h3标签
                    title_ele = item.ele('tag:h2', timeout=0.2) or item.ele('tag:h3', timeout=0.2)
                title = title_ele.text if title_ele else "未知商品名称"
                if len(title) < 3: continue
                
                # 价格 - 使用contains方式查找
                price_ele = item.ele('@data-e2e=search-shop-price', timeout=0.2)
                if not price_ele:
                    price_ele = item.ele('text:$', timeout=0.2)
                
                # 销量
                sales_ele = item.ele('@data-e2e=search-shop-sales', timeout=0.2)
                
                # 链接
                link_ele = item if item.tag == 'a' else item.ele('tag:a', timeout=0.2)
                product_url = link_ele.attr('href') if link_ele else None
                
                parsed_item = {
                    "platform": "TikTok Shop",
                    "product_title": title.strip(),
                    "asin": None, 
                    "product_url": product_url,
                    "brand": brand,
                    "price_current_amount": price_ele.text.strip() if price_ele else None,
                    "price_original_amount": None,
                    "rating_average": None,
                    "rating_count": sales_ele.text.strip() if sales_ele else None, 
                    "featured": None,
                    "color": None, "material": None, "style": None
                }
                # 简单去重
                if not any(i['product_title'] == title for i in extracted_data):
                    extracted_data.append(parsed_item)

            break # 瀑布流暂不翻页

        print_log("Task Status: completed")
        print("\n--- Extracted Product Data ---")
        print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: TikTok automation failed. Details: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()