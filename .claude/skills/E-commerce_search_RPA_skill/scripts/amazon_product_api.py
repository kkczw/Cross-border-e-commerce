import sys
import time
import json
from datetime import datetime
from DrissionPage import ChromiumPage

def print_log(message):
    """输出带有时间戳的日志，满足 Agent 的监控要求"""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] {message}", flush=True)

def main():
    if len(sys.argv) < 2:
        print("Error: Missing required argument.")
        sys.exit(1)

    keywords = sys.argv[1]
    brand = sys.argv[2] if len(sys.argv) > 2 else "Dell"
    
    try:
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    except ValueError:
        print("Error: Maximum_number_of_page_turns must be a valid integer.")
        sys.exit(1)

    print_log("Task Status: running")
    print_log(f"Starting local browser automation... (Keywords: {keywords}, Brand: {brand})")
    
    try:
        # 启动 DrissionPage 接管本地浏览器
        page = ChromiumPage()
        
        page.get('https://www.amazon.com')
        page.wait.load_start()
        
        # 搜索
        search_term = f"{brand} {keywords}".strip()
        page.ele('#twotabsearchtextbox').input(search_term)
        page.ele('#nav-search-submit-button').click()
        page.wait.load_start()

        extracted_data = []

        # 翻页抓取
        for current_page in range(1, max_pages + 1):
            print_log(f"Task Status: running (Scraping page {current_page}/{max_pages})")
            time.sleep(2) 
            
            items = page.eles('@data-component-type=s-search-result')
            
            for item in items:
                # 标题
                title_ele = item.ele('tag:h2', timeout=0.5)
                product_title = title_ele.text if title_ele else None
                if not product_title:  # 过滤掉空卡片
                    continue
                
                # ASIN
                asin = item.attr('data-asin') or None
                
                # 链接
                link_ele = item.ele('tag:a', timeout=0.5)
                product_url = None
                if link_ele and link_ele.attr('href'):
                    raw_link = link_ele.attr('href')
                    product_url = raw_link if raw_link.startswith('http') else f"https://www.amazon.com{raw_link}"

                # 价格
                price_ele = item.ele('.a-price', timeout=0.5)
                price_current_amount = price_ele.ele('.a-offscreen', timeout=0).text if price_ele else None
                original_price_ele = item.ele('.a-text-price', timeout=0.5)
                price_original_amount = original_price_ele.ele('.a-offscreen', timeout=0).text if original_price_ele else None

                # 评分
                rating_ele = item.ele('.a-icon-alt', timeout=0.5)
                rating_average = rating_ele.text if rating_ele else None
                rating_count_ele = item.ele('.a-size-base s-underline-text', timeout=0.5)
                rating_count = rating_count_ele.text if rating_count_ele else None

                # 特色徽章
                badge_ele = item.ele('.a-badge-text', timeout=0.5)
                featured = badge_ele.text if badge_ele else None

                # 组装 12 字段结构
                parsed_item = {
                    "product_title": product_title,
                    "asin": asin,
                    "product_url": product_url,
                    "brand": brand, 
                    "price_current_amount": price_current_amount,
                    "price_original_amount": price_original_amount,
                    "rating_average": rating_average,
                    "rating_count": rating_count,
                    "featured": featured,
                    "color": None,     
                    "material": None,  
                    "style": None      
                }
                extracted_data.append(parsed_item)

            if current_page < max_pages:
                next_btn = page.ele('.s-pagination-next', timeout=2)
                if next_btn and 's-pagination-disabled' not in next_btn.attr('class'):
                    next_btn.click()
                    page.wait.load_start()
                else:
                    break

        print_log("Task Status: completed")
        print("\n--- Extracted Product Data ---")
        print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: Browser automation failed. Details: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()