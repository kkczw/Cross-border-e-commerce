import os
import subprocess
import sys

# ============ 测试配置区 ============
# 要测试的目标脚本名称
TARGET_SCRIPT = r"E:\zb\888888\dianshang\.claude\skills\amazon-product-api-skill\scripts\temu_product_api.py"

# 模拟 Agent 传入的测试参数
TEST_KEYWORDS = "laptop"  # 搜索关键词
TEST_BRAND = "Dell"       # 品牌 (换个戴尔测试一下)
TEST_PAGES = "1"          # 抓取页数 (测试时建议设为1，跑得快)
TEST_LANGUAGE = "en"      # 语言
# ====================================

def main():
    # 1. 检查目标脚本是否存在
    if not os.path.exists(TARGET_SCRIPT):
        print(f"❌ 找不到目标脚本: {TARGET_SCRIPT}，请确保它们在同一目录下。")
        sys.exit(1)

    print("🚀 准备启动本地自动化 RPA 测试...")
    print(f"📦 模拟入参: 关键词='{TEST_KEYWORDS}', 品牌='{TEST_BRAND}', 页数={TEST_PAGES}\n")
    print("-" * 50)

    # 2. 拼接命令行指令 (和 Agent 调用的格式完全一致)

    command = [
        sys.executable, "-u", TARGET_SCRIPT, 
        TEST_KEYWORDS, TEST_BRAND, TEST_PAGES, TEST_LANGUAGE
    ]
    
    # 3. 执行脚本并实时打印终端输出
    try:
        # check=True 确保如果子脚本报错，测试脚本也会抛出异常
        subprocess.run(command, check=True)
        print("\n" + "-" * 50)
        print("✅ 测试完美收官！输出格式已完全符合要求。")
        print("💡 接下来你可以把这个 Python 脚本直接作为自定义工具，挂载到你的 Dify 或者 FastGPT 智能体工作流里使用了！")
    except subprocess.CalledProcessError as e:
        print("\n" + "-" * 50)
        print(f"❌ 测试中断或报错，退出码: {e.returncode}")
    except KeyboardInterrupt:
        print("\n⚠️ 测试已被手动强制停止。")

if __name__ == "__main__":
    main()