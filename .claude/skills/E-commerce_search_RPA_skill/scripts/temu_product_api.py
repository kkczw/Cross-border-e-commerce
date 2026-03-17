#!/usr/bin/env python3
import sys, time, json, re
from datetime import datetime
from DrissionPage import ChromiumPage,ChromiumOptions

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
        co =ChromiumOptions()
        co.set_proxy('http://127.0.0.1:10792')
        page = ChromiumPage(co)
        search_term = f"{brand} {keywords}".strip()
        
        # 访问 Temu 搜索页
        page.get(f'https://www.temu.com/search_result.html?search_key={search_term}')
       
        print_log("等待页面加载并尝试处理弹窗...")
        page.wait.load_start()
        time.sleep(4)
        
        # 盲按 ESC 键，尝试关闭可能存在的转盘/注册弹窗
        page.actions.key_down('ESCAPE').key_up('ESCAPE')
        time.sleep(1)

        extracted_data = []

        for current_page in range(1, max_pages + 1):
            print_log(f"Task Status: running (Scraping Temu page {current_page})")
            
            # 必须多次向下滚动，强制 Temu 加载图片和价格数据
            for _ in range(5):
                page.scroll.down(600)
                time.sleep(1.5)
            
            # 【核心战术：先找图片，再找链接，最后正则挖价格】
            imgs = page.eles('tag:img')
            print_log(f"扫描到 {len(imgs)} 张图片，开始深度分析...")
            
            for img in imgs:
                # 1. 过滤垃圾小图：商品主图通常比较大，宽度小于 100 像素的直接过滤掉（如支付图标、星级图标）
                try:
                    size = img.rect.size
                    if not size or size[0] < 100:
                        continue
                except Exception:
                    continue
                
                # 2. 向上找 5 层父容器，试图把整个商品卡片框起来
                card = img.parent(5)
                if not card:
                    continue
                    
                card_text = card.text
                # 如果这 5 层容器里连 $ 符号都没有，可能找的层级不够，再往上找 2 层
                if '$' not in card_text and 'US$' not in card_text:
                    card = img.parent(7)
                    if not card: continue
                    card_text = card.text
                    if '$' not in card_text and 'US$' not in card_text:
                        continue # 如果还是没有价格符号，说明真不是商品卡片，跳过
                
                # 3. 在大容器里找链接
                link_ele = card.ele('tag:a', timeout=0.1)
                if not link_ele:
                    continue
                
                raw_link = link_ele.attr('href')
                product_url = None
                if raw_link:
                    product_url = raw_link if raw_link.startswith('http') else f"https://www.temu.com{raw_link}"
                
                # 4. 提取标题：优先取图片的 alt，如果没有，就取卡片里最长的那段文字
                title = img.attr('alt')
                if not title or len(title) < 10:
                    # 把卡片文字按换行符劈开，找长度大于 10 的句子作为兜底标题
                    lines = [line.strip() for line in card_text.split('\n') if len(line.strip()) > 10]
                    title = lines[0] if lines else "未知商品"
                
                # 5. 提取价格：用正则在大容器的纯文本里，强行匹配 "$ 19.99" 或 "US$19.99" 这样的格式
                price_match = re.search(r'(?:US)?\$\s*\d+(?:\.\d+)?', card_text)
                price = price_match.group(0) if price_match else None
                
                if product_url and price:
                    parsed_item = {
                        "platform": "Temu",
                        "product_title": title.strip(),
                        "asin": None, 
                        "product_url": product_url,
                        "brand": brand,
                        "price_current_amount": price,
                        "price_original_amount": None,
                        "rating_average": None,
                        "rating_count": None,
                        "featured": None,
                        "color": None, "material": None, "style": None
                    }
                    # 去重处理：避免抓到同一个 URL
                    if not any(item['product_url'] == product_url for item in extracted_data):
                        extracted_data.append(parsed_item)

            break # 瀑布流暂不翻页

         

        # ！！核心排查工具：如果依然没抓到数据，强制截图取证！！
        if len(extracted_data) == 0:
            print_log("⚠️ 警告：未能提取到任何商品数据！")
            screenshot_name = 'temu_error_debug.png'
            page.get_screenshot(path=screenshot_name)
            print_log(f"📸 截图已保存为当前目录下的 {screenshot_name}，快去看看页面被什么挡住了！")

        print_log("Task Status: completed")
        print("\n--- Extracted Product Data ---")
        print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: Temu automation failed. Details: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()