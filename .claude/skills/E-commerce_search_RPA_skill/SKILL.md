---
name: cross-platform-ecommerce-rpa-skill
description: "This skill helps users extract structured product listings from Amazon、Etsy、Temu and TikTok Shop, including titles, ASINs, prices, ratings, and specifications. Use this skill when users want to search for products on E-commerce, find the best selling brand products, track price changes for items, get a list of categories with high ratings, compare different brand products on E-commerce, extract E-commerce product data for market research, look for products in a specific language or marketplace, analyze competitor pricing for keywords, find featured products for search terms, get technical specifications like material or color for product lists."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["python"]}}}
---

# Amazon Product Search Skill

## 📖 Introduction
This skill utilizes RPA tool to extract structured product listings from E-commerces search results. It provides detailed information including titles, ASINs, prices, ratings, and product specifications, enabling efficient market research and product monitoring without manual data collection.

## ✨ Features
1. **No Hallucinations**: Pre-set workflows avoid AI generative hallucinations, ensuring stable and precise data extraction.
2. **No Captcha Issues**: No need to handle reCAPTCHA or other verification challenges.
3. **No IP Restrictions**: No need to handle regional IP restrictions or geofencing.
4. **Faster Execution**: Tasks execute faster compared to pure AI-driven browser automation solutions.
5. **Cost-Effective**: Significantly lowers data acquisition costs compared to high-token-consuming AI solutions.


## 🛠️ Input Parameters
The agent should configure the following parameters based on user requirements:

1. **KeyWords**
   - **Type**: `string`
   - **Description**: Search keywords used to find products on Amazon.
   - **Required**: Yes
   - **Example**: `laptop`, `wireless earbuds`

2. **Brand**
   - **Type**: `string`
   - **Description**: Filter products by brand name.
   - **Default**: `Apple`
   - **Example**: `Dell`, `Samsung`

3. **Maximum_number_of_page_turns**
   - **Type**: `number`
   - **Description**: Number of search result pages to paginate through.
   - **Default**: `1`

4. **language**
   - **Type**: `string`
   - **Description**: UI language for the Amazon browsing session.
   - **Default**: `en`
   - **Example**: `zh-CN`, `de`

## 🚀 Usage

### Case 1: When a user asks about Amazon products, the Agent should use the following standalone script to achieve a "one-line command result":

```bash
# Example Usage
python -u ./scripts/amazon_product_api.py "keywords" "brand" pages "language"
```
### Case 2: When a user asks about Etsy products, the Agent should use the following standalone script to achieve a "one-line command result":

```bash
# Example Usage
python -u ./scripts/esty_product_api.py "keywords" "brand" pages "language"
```

### Case 3: When a user asks about temu products, the Agent should use the following standalone script to achieve a "one-line command result":
```bash
python -u ./scripts/temu_product_api.py "keywords" "brand" pages "language"
```
### Case 4: When a user asks about tiktok products, the Agent should use the following standalone script to achieve a "one-line command result":
```bash
python -u ./scripts/tiktok_product_api.py "keywords" "brand" pages "language"
```
### Case 5: When the user does not specify the product on the platform, the Agent should use the following script to achieve "multi-line command results":
The Agent MUST execute multiple scripts sequentially to gather comprehensive data.
```bash
# Example Usage
python -u ./scripts/esty_product_api.py "keywords" "brand" pages "language"
```
```bash
python -u ./scripts/amazon_product_api.py "keywords" "brand" pages "language"
```
```bash
python -u ./scripts/temu_product_api.py "keywords" "brand" pages "language"
```
```bash
python -u ./scripts/tiktok_product_api.py "keywords" "brand" pages "language"
```

### ⏳ Execution Monitoring
Since this task involves automated browser operations, it may take some time (several minutes). The script will **continuously output status logs with timestamps** (e.g., `[14:30:05] Task Status: running`).
**Agent Instructions**:
- While waiting for the script result, keep monitoring the terminal output.
- As long as the terminal is outputting new status logs, the task is running normally; do not mistake it for a deadlock or unresponsiveness.
- Only if the status remains completely unchanged for a long time without logs, or throws an error, consider the task failed.
## 📊 Data Output
Upon success, the script parses and prints the structured product data from the API response, which includes:
- `platform`: The source E-commerce platform.
- `product_title`: Full title of the product.
- `asin`: Standard Identification Number or Listing ID.
- `product_url`: URL of the E-commerce product page.
- `brand`: Brand name.
- `price_current_amount`: Current price.
- `price_original_amount`: Original price (if applicable).
- `rating_average`: Average star rating.
- `rating_count`: Total number of ratings.
- `featured`: Badges like "Best Seller" or "E-commerce's Choice".
- `color`, `material`, `style`: Product attributes (if available).

## ⚠️ Error Handling & Retry
If an error occurs during script execution (e.g., network fluctuations, DOM changes, or task failure), the Agent should follow this logic:

1. **Retry Limit**: 
   - If the output starts with Error: or returns empty [], the Agent should automatically try to re-execute that specific script once.

2. **Graceful Degradation**:
   - During a Multi-Platform Comparison (Case 5), if one platform fails even after a retry, ignore it and build the final comparison report using the successful data from the other platforms.

## 🌟 Typical Use Cases
1. **Market Research**: Search for a specific product category to analyze top brands and pricing.
2. **Competitor Monitoring**: Track product listings and price changes for specific competitor brands.
3. **Product Catalog Enrichment**: Extract structured details like ASINs and specifications to build or update a product database.
4. **Rating Analysis**: Find high-rated products for specific keywords to identify market leaders.
5. **Localized Research**: Search E-commerce in different languages to analyze international markets.
6. **Price Tracking**: Monitor current and original prices to identify discount trends.
7. **Brand Performance**: Evaluate the presence of a specific brand in search results across multiple pages.
8. **Attribute Extraction**: Gather technical specifications like material or color for a list of products.
9. **Lead Generation**: Identify popular products and their manufacturers for business outreach.
10. **Automated Data Feed**: Periodically pull E-commerce search results into external BI tools or dashboards.
11. **Cross-Platform Price Comparison**:Find the cheapest purchasing channel for a specific product.
12. **Market Research**: Analyze top brands and pricing across different e-commerce ecosystems.
13. **Dropshipping/Arbitrage Analysis** : Compare generic alternatives on Temu with branded equivalents on Amazon.
14. **Competitor Monitoring**: Track product listings and price changes for specific competitor brands globally.
