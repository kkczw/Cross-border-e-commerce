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
        page = ChromiumPage()
        search_term = f"{brand} {keywords}".strip()
        # Etsy 搜索 URL 规律
        page.get(f'https://www.etsy.com/search?q={search_term}')
        page.wait.load_start()

        extracted_data = []

        for current_page in range(1, max_pages + 1):
            print_log(f"Task Status: running (Scraping Etsy page {current_page})")
            time.sleep(2)
            
            # 找到所有的商品卡片
            items = page.eles('@data-listing-id')
            
            # 使用集合来跟踪已经处理过的 ASIN (Listing ID)，避免重复
            seen_asins = set()
            
            for item in items:
                # 提取 ASIN (Listing ID)
                asin = item.attr('data-listing-id')
                
                # 如果没有 ASIN 或者已经抓取过这个 ASIN，则跳过
                if not asin or asin in seen_asins:
                    continue
                
                # 标题通常在 h3 标签中
                title_ele = item.ele('tag:h3', timeout=0.5)
                if not title_ele: continue
                
                # Etsy 的价格通常有 currency-value 类名
                price_ele = item.ele('.currency-value', timeout=0.5)
                
                # 评分文本（通常是隐藏的屏幕阅读器文本）
                rating_ele = item.ele('text:out of 5 stars', timeout=0.5)
                
                link_ele = item.ele('tag:a', timeout=0.5)
                product_url = link_ele.attr('href') if link_ele else None
                
                # 如果缺少必要的 URL，跳过
                if not product_url:
                    continue
                
                parsed_item = {
                    "platform": "Etsy",
                    "product_title": title_ele.text.strip(),
                    "asin": asin,
                    "product_url": product_url,
                    "brand": brand,
                    "price_current_amount": price_ele.text if price_ele else None,
                    "price_original_amount": None,
                    "rating_average": rating_ele.text.split(' ')[0] if rating_ele else None,
                    "rating_count": None,
                    "featured": None,
                    "color": None, "material": None, "style": None
                }
                
                # 记录已抓取的 ASIN
                seen_asins.add(asin)
                extracted_data.append(parsed_item)

            if current_page < max_pages:
                # Etsy 下一页按钮包含 "Next" 文本或特定的 icon
                next_btn = page.ele('text:Next', timeout=2) or page.ele('.wt-action-group__item-container', timeout=2)
                if next_btn:
                    next_btn.click()
                    page.wait.load_start()
                else:
                    break

        print_log("Task Status: completed")
        print("\n--- Extracted Product Data ---")
        print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: Etsy automation failed. Details: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()