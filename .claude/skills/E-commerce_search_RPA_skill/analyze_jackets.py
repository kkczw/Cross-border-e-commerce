import json, re, sys

def load_amazon_data():
    """Load Amazon data from file"""
    try:
        with open(r'C:\Users\zhoub\.claude\projects\e--zb-888888-dianshang\bc3604cc-7c15-4378-ad37-f85fccbb8763\tool-results\b3veohtft.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == '--- Extracted Product Data ---':
                json_str = ''.join(lines[i+1:])
                break
        return json.loads(json_str)
    except Exception as e:
        print(f"Error loading Amazon data: {e}")
        return []

def load_temu_data():
    """Load Temu data from recent output"""
    temu_data = [
        {
            'platform': 'Temu',
            'product_title': '千鸟格开襟外套，春秋百搭长袖外套，女装',
            'price_current_amount': '$10.76',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '女士休闲工装外套，宽松版型，轻薄面料，街头风，翻领，长袖，纽扣设计，非常适合通勤和多种场合穿搭',
            'price_current_amount': '$16.12',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '时尚优雅2025秋冬新款纯色质感拉链长袖棒球领女士夹克',
            'price_current_amount': '$11.50',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '女士牛仔拼接中长款外套翻领长袖宽松款早春新款 休闲出街时尚百搭上衣',
            'price_current_amount': '$14.90',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '韩版春秋爆款连帽拉链外套韩版灯芯绒宽松拉链开衫百搭显瘦大码上衣',
            'price_current_amount': '$17.31',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '2025新款时尚优雅纯色休闲夹克，带拉链抽绳长袖女士开襟连帽衫',
            'price_current_amount': '$16.01',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '大码女士纯色优雅长袖纽扣人造麂皮绒夹克',
            'price_current_amount': '$19.53',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '秋冬新款复古棒球立领夹棉菱宽松外套上衣薄款棉衣棉服',
            'price_current_amount': '$18.80',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '秋冬保暖毛绒拼布拉链口袋连帽宽松外套女',
            'price_current_amount': '$17.02',
            'rating_average': None,
            'featured': None
        },
        {
            'platform': 'Temu',
            'product_title': '女式风衣颜色混合雨衣轻便防水外套连帽风衣',
            'price_current_amount': '$9.95',
            'rating_average': None,
            'featured': None
        }
    ]
    return temu_data

def calculate_score(item):
    """Calculate popularity score for a jacket"""
    brand = item.get('product_title', '')
    price_str = item.get('price_current_amount', '')
    rating_str = item.get('rating_average', '')
    featured = item.get('featured', '')
    platform = item.get('platform', '')

    score = 0

    # Price analysis
    price = None
    if price_str:
        match = re.search(r'[\d.]+', price_str)
        if match:
            price = float(match.group())
            # Youth women likely prefer affordable fashion
            if 15 <= price <= 40:  # Best price range for youth
                score += 4
            elif price < 15:
                score += 3  # Very affordable
            elif price < 60:
                score += 2  # Moderate
            else:
                score += 1  # Premium

    # Rating analysis
    rating = None
    if rating_str:
        match = re.search(r'(\d+(\.\d+)?)', str(rating_str))
        if match:
            rating = float(match.group(1))
            if rating >= 4.5:
                score += 4
            elif rating >= 4.0:
                score += 3
            elif rating >= 3.5:
                score += 2
            else:
                score += 1

    # Featured status (strong sales indicator)
    if featured:
        featured_lower = str(featured).lower()
        if 'best seller' in featured_lower:
            score += 6  # Strongest indicator
        elif 'overall pick' in featured_lower:
            score += 5
        elif 'limited' in featured_lower:
            score += 4  # Limited time drives urgency
        elif 'save' in featured_lower:
            score += 3  # Discounts attract buyers
        elif 'amazon' in featured_lower:
            score += 2  # Amazon's choice

    # Platform weight (Amazon has better sales data reliability)
    if platform == 'Amazon':
        score += 3
    elif platform == 'Temu':
        score += 1  # Temu is popular for affordable fashion

    # Brand appeal for youth women
    brand_lower = brand.lower()
    youth_fashion_brands = [
        'amazon essentials', 'dokotoo', 'reebok', 'columbia',
        'nike', 'adidas', 'puma', 'vans', 'converse', 'h&m',
        'zara', 'forever 21', 'shein', 'fashion nova'
    ]
    for yb in youth_fashion_brands:
        if yb in brand_lower:
            score += 3
            break

    # Product title keywords for youth fashion
    title = brand.lower()  # In Amazon data, this is actually brand
    # For Temu, we have full titles
    if 'temu' in platform.lower() and 'product_title' in item:
        title = item['product_title'].lower()

    youth_keywords = [
        'fashion', 'stylish', 'trendy', 'chic', 'modern',
        'young', 'youth', 'teen', 'college', 'student',
        'casual', 'street', 'streetwear', 'urban',
        'denim', 'jacket', 'hoodie', 'bomber', 'windbreaker',
        '韩版', '爆款', '时尚', '休闲', '新款'  # Chinese keywords
    ]

    for keyword in youth_keywords:
        if keyword in title:
            score += 1

    return score, price, rating

def main():
    print("Analyzing youth women jackets for popularity ranking...")
    print("=" * 100)

    # Load data
    amazon_items = load_amazon_data()
    temu_items = load_temu_data()

    # Prepare all items
    all_items = []
    for item in amazon_items:
        item['platform'] = 'Amazon'
        all_items.append(item)

    for item in temu_items:
        item['platform'] = 'Temu'
        all_items.append(item)

    print(f"Total items to analyze: {len(all_items)}")

    # Calculate scores
    scored_items = []
    for item in all_items:
        score, price, rating = calculate_score(item)
        scored_items.append({
            'item': item,
            'score': score,
            'price': price,
            'rating': rating
        })

    # Sort by score
    scored_items.sort(key=lambda x: x['score'], reverse=True)

    print("\n🏆 TOP 10 YOUTH WOMEN JACKETS (Inferred Popularity Ranking)")
    print("=" * 100)
    print("Note: Ranking based on price appeal, ratings, featured status,")
    print("      brand relevance, and platform reliability for youth women.")
    print("=" * 100)

    for i, scored in enumerate(scored_items[:10]):
        item = scored['item']
        score = scored['score']
        price = scored['price']
        rating = scored['rating']

        brand = item.get('product_title', 'Unknown')
        platform = item.get('platform', 'Unknown')
        featured = item.get('featured', 'None')

        # For Temu items, show full title
        if platform == 'Temu':
            title = item.get('product_title', brand)
        else:
            # For Amazon, try to get more info from URL
            title = brand
            url = item.get('product_url', '')
            if url and '/dp/' in url:
                # Extract product name from URL
                try:
                    # Amazon URLs often have format: /product-name/dp/ASIN
                    parts = url.split('/dp/')[0].split('/')
                    if len(parts) > 1:
                        product_name = parts[-1].replace('-', ' ').title()
                        title = f"{brand} - {product_name}"
                except:
                    pass

        print(f"\n{i+1}. {title}")
        print(f"   📊 Score: {score:.1f} | 💰 Price: ${price if price else 'N/A'} | ⭐ Rating: {rating if rating else 'N/A'}")
        print(f"   🏪 Platform: {platform} | 🏷️ Featured: {featured}")

        # Show ASIN for Amazon
        if platform == 'Amazon' and 'asin' in item:
            print(f"   🔗 ASIN: {item['asin']}")

        # Show URL if available
        url = item.get('product_url', '')
        if url:
            if len(url) > 70:
                short_url = url[:67] + '...'
            else:
                short_url = url
            print(f"   🌐 URL: {short_url}")

    print("\n" + "=" * 100)
    print("💡 Analysis Methodology:")
    print("1. Price Appeal (15-40 USD range scores highest for youth budget)")
    print("2. Customer Ratings (4.5+ scores highest)")
    print("3. Featured Status ('Best Seller', 'Overall Pick' indicate popularity)")
    print("4. Brand Relevance (Youth fashion brands score higher)")
    print("5. Platform Reliability (Amazon data more reliable than Temu)")
    print("=" * 100)

if __name__ == '__main__':
    main()