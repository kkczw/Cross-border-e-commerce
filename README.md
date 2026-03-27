\# Cross-Platform E-commerce RPA Skill 🌐



\[!\[Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

\[!\[RPA](https://img.shields.io/badge/Automation-RPA-orange.svg)]()

\[!\[E-commerce](https://img.shields.io/badge/Market-Research-green.svg)]()



这是一个强大的跨平台电商数据采集工具（Skill），专门用于从 \*\*Amazon, Etsy, Temu\*\* 和 \*\*TikTok Shop\*\* 提取结构化的商品数据。它通过 RPA 流程解决了传统爬虫容易遇到的验证码、IP 封禁及数据幻觉问题。

\*This skill is optimized for OpenClaw and AI Agent workflows.\*


\## ✨ 核心优势



\- \*\*零数据幻觉\*\*：基于预设工作流，确保提取的 ASIN、价格和评分 100% 真实可靠。

\- \*\*反爬技术避让\*\*：内置逻辑有效规避 reCAPTCHA 验证及地域 IP 限制。

\- \*\*高性能执行\*\*：相比纯 AI 浏览器自动化方案，任务执行速度更快，Token 消耗更低。

\- \*\*状态实时监控\*\*：支持连续状态日志输出，方便在长时任务中监控执行进度。



\## 🛠️ 支持平台与功能



| 平台 | 数据维度 | 主要用途 |

| :--- | :--- | :--- |

| \*\*Amazon\*\* | 标题, ASIN, 价格, 评分, 规格 | 竞品分析、价格监控 |

| \*\*Etsy\*\* | 商品名, 价格, 材质, 品牌 | 手工艺品市场研究 |

| \*\*Temu\*\* | 商品详情, 优惠信息, 评分 | 跨境选品、低价策略分析 |

| \*\*TikTok\*\* | 流行趋势数据, 规格, 品牌 | 社交电商爆款追踪 |



\## 🚀 快速开始



\### 环境要求

\- Python 3.8+

\- 已安装相关 RPA 驱动（详见 `/docs/setup.md`）



\### 使用示例

你可以通过简单的命令行参数调用各平台的脚本：



```bash

\# 搜索 Amazon 上的笔记本电脑 (Apple 品牌, 前 2 页, 英文界面)

python -u ./scripts/amazon\_product\_api.py "laptop" "Apple" 2 "en"



\# 同时对比多个平台的搜索结果

python -u ./scripts/multi\_platform\_search.py "wireless earbuds" "Samsung" 1 "en"



```



\## 📊 输入与输出



\### 输入参数



\* `KeyWords`: 搜索关键词（必填）

\* `Brand`: 品牌过滤（默认: Apple）

\* `Max\_Pages`: 翻页深度（默认: 1）

\* `Language`: 界面语言（默认: en）



\### 输出数据结构



执行成功后，你将获得如下结构化 JSON 数据：



\* `platform`: 来源平台

\* `product\_title`: 商品全名

\* `asin/id`: 唯一识别码

\* `price\_current\_amount`: 当前价格

\* `featured`: 标签（如 "Best Seller"）

\* `attributes`: 材质、颜色等详细规格



\## ⚠️ 异常处理



项目内置了自动重试机制：



1\. \*\*自动重试\*\*：脚本运行失败或返回空结果时，会自动发起一次重试。

2\. \*\*平滑降级\*\*：在多平台对比模式下，若单一平台失效，系统会跳过该平台并整合其余成功数据生成报表。



\## 🌟 应用场景



\* \*\*市场调研\*\*：分析特定类目下的头部品类与定价趋势。

\* \*\*跨境套利\*\*：对比 Temu 与 Amazon 同款商品的价差。

\* \*\*自动补货/调价\*\*：对接 BI 工具，实现自动化的电商运营监控。



---



\*本项目由 \[你的名字/GitHub ID] 开发，专注于 AI Agent 技能集成与自动化流。\*



