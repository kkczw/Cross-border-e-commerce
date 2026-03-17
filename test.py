from DrissionPage import ChromiumPage
from DataRecorder import Recorder
import time

def main():
    # 1. 初始化写入工具（直接指定生成的 Excel 文件名）
    # DataRecorder 会自动帮你建表、写表头、保存，完全不需要理会 openpyxl 的底层逻辑
    recorder = Recorder('亚马逊商品数据.xlsx')
    recorder.add_data(['商品标题', '价格', '商品链接', 'ASIN']) # 写入表头

    # 2. 启动/接管浏览器
    print("🚀 正在启动浏览器...")
    page = ChromiumPage()
    
    # 3. 访问亚马逊主页
    page.get('https://www.amazon.com')
    print("⏳ 等待页面加载...")
    page.wait.load_start() 

    # 4. 输入关键词 -> 点击搜索
    keyword = 'laptop'
    print(f"🔍 正在搜索关键词: {keyword}")
    # 定位搜索框并输入
    page.ele('#twotabsearchtextbox').input(keyword)
    # 定位搜索按钮并点击
    page.ele('#nav-search-submit-button').click()
    page.wait.load_start()

    # 5. 设定你要抓取的页数（这里以 3 页为例，防止一直跑被封）
    target_pages = 3

    for current_page in range(1, target_pages + 1):
        print(f"\n📄 正在抓取第 {current_page} 页...")
        
        # 页面防爬缓冲：稍微等待一下，模拟人类看网页
        time.sleep(2)
        
        # 提取列表：找到当前页所有的“商品卡片”块
        # 亚马逊的商品卡片通常带有 data-component-type="s-search-result" 属性
        items = page.eles('@data-component-type=s-search-result')
        
        for item in items:
            # 6. 获取指定商品相关信息 (加 timeout 防止某个商品没价格导致卡死)
            # 获取标题
            title_ele = item.ele('tag:h2', timeout=1)
            title = title_ele.text if title_ele else '无标题'
            
            # 获取价格 (获取整数部分)
            price_ele = item.ele('.a-price-whole', timeout=1)
            price = price_ele.text if price_ele else '无价格/缺货'
            
            # 获取商品详情页链接
            link_ele = item.ele('tag:a', timeout=1)
            link = link_ele.attr('href') if link_ele else '无链接'
            
            # 获取 ASIN (隐藏在卡片的 data-asin 属性中)
            asin = item.attr('data-asin') or '无ASIN'

            # 7. 写入 Excel
            # 直接传入一个列表，DataRecorder 会自动追加一行并实时保存
            recorder.add_data([title, price, link, asin])
            
        print(f"✅ 第 {current_page} 页抓取完成，已实时写入 Excel。")

        # 8. 点击下一页
        if current_page < target_pages:
            # 寻找“下一页”按钮，亚马逊经常变动，通常类名包含 s-pagination-next
            next_btn = page.ele('.s-pagination-next', timeout=3)
            
            # 检查按钮是否存在，以及是否变成了不可点击状态（最后一页）
            if next_btn and 's-pagination-disabled' not in next_btn.attr('class'):
                print("👉 点击进入下一页...")
                next_btn.click()
                page.wait.load_start()
            else:
                print("🛑 已经到达最后一页或找不到下一页按钮，结束抓取。")
                break

    # 释放资源
    recorder.record()
    print("\n🎉 全部任务执行完毕！请查看当前目录下的 亚马逊商品数据.xlsx")

if __name__ == '__main__':
    main()