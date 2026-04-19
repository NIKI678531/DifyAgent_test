import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import urllib3
import re
import os
import shutil
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===================== 【你只需要确认文件名】 =====================
# INPUT_CSV = "你的餐厅名单.csv"       # 你的CSV文件名
# OUTPUT_EXCEL = "OpenRice_最终查询结果.xlsx"# ===================== 【你只需要确认文件名】 =====================
INPUT_EXCEL = "/Users/lkq/Downloads/20251106_Closed status check.xlsx"  # 你的 Excel 文件路径
OUTPUT_EXCEL = "OpenRice_最终查询结果.xlsx"
# =================================================================

# =================================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
    "Referer": "https://www.openrice.com/en/hongkong/"
}

def clean_text(s):
    return s.strip() if s else ""

BASE_URL = "https://www.openrice.com"

def get_correct_restaurant_status(shop_name, area, address):
    """
    核心功能：根据 名称 + 地区 + 地址 精准查找店铺
    使用 Selenium 模拟浏览器获取完整搜索结果
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 添加防检测参数
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None

    # 自动查找 chromedriver 路径
    chromedriver_path = shutil.which('chromedriver')
    if not chromedriver_path:
        # 尝试常见的 macOS 路径
        possible_paths = [
            "/opt/homebrew/bin/chromedriver",
            "/usr/local/bin/chromedriver",
            "/opt/homebrew/Caskroom/chromedriver/latest/chromedriver-mac-arm64/chromedriver"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                chromedriver_path = path
                break

    s = Service(chromedriver_path)
    chrome_options = Options()
    # macOS 不需要指定 binary_location，除非 Chrome 不在默认路径
    driver = webdriver.Chrome(service=s, options=chrome_options)

    try:
        # 构建搜索 URL - 只搜索餐厅名字
        search_url = f"https://www.openrice.com/en/hongkong/restaurants?what={shop_name}"
        print(f"   → 访问 URL: {search_url}")
        driver.get(search_url)
        time.sleep(2)  # 增加等待时间
            
        # 【关键调试】检查是否成功加载页面
        current_url = driver.current_url
        page_source = driver.page_source
        print(f"   → 当前 URL: {current_url}")
        print(f"   → 页面源码长度：{len(page_source)} 字符")
        
        # 检查是否包含关键内容
        if "pois-closed-restaurants" in page_source:
            print(f"   ✓ 页面包含 'pois-closed-restaurants' 关键字")
        else:
            print(f"   ✗ 页面 NOT 包含 'pois-closed-restaurants' 关键字")
        
        if "support.google.com" in current_url or "error" in current_url.lower():
            print(f"   ✗ 无法访问 OpenRice，当前 URL: {current_url}")
            return "无法访问网站", search_url
            
        # 向下滚动以加载所有结果
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        max_scroll = 20
            
        while scroll_count < max_scroll:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1
        
        # 获取所有餐厅结果 - 使用 class name 定位
        print(f"   → 开始查找餐厅元素...")
        
        # 尝试直接使用 CSS 选择器匹配你提供的 HTML 结构
        elements = driver.find_elements(By.CSS_SELECTOR, "div.pois-closed-restaurants-content")
        print(f"   → 使用 'div.pois-closed-restaurants-content' 找到 {len(elements)} 个结果")
        
        # 如果没有找到，尝试其他可能的 class
        if not elements:
            elements = driver.find_elements(By.CLASS_NAME, "pois-closed-restaurants-container")
            print(f"   → 使用 'pois-closed-restaurants-container' 找到 {len(elements)} 个结果")
        
        # 如果还是没有，尝试查找包含 title class 的元素
        if not elements:
            # 查找所有包含 title 类的 div
            title_divs = driver.find_elements(By.CLASS_NAME, "title")
            print(f"   → 使用 '.title' 找到 {len(title_divs)} 个 title 元素")
            
            # 从 title 元素向上查找父级容器
            elements = []
            for title_div in title_divs:
                try:
                    # 尝试查找包含链接的父级元素
                    parent_link = title_div.find_element(By.XPATH, "./ancestor::a[1]")
                    if parent_link not in elements:
                        elements.append(parent_link)
                except:
                    pass
            
        print(f"   DEBUG: 找到 {len(elements)} 个搜索结果")
        
        # 调试：显示前几个结果的信息
        for i, elem in enumerate(elements[:5], 1):
            try:
                # 查找 title 部分
                title_div = elem.find_element(By.CLASS_NAME, "title")
                spans = title_div.find_elements(By.TAG_NAME, "span")
                
                if len(spans) >= 1:
                    name_text = spans[0].text.strip()
                    status_text = spans[1].text.strip() if len(spans) > 1 else ""
                    is_closed = "Closed" in status_text
                    
                    # 查找地址
                    try:
                        addr_div = elem.find_element(By.CLASS_NAME, "address")
                        addr_text = addr_div.text.strip()[:60]
                    except:
                        addr_text = "N/A"
                    
                    print(f"   [{i}] {name_text} {status_text} -> {addr_text}... | {'已结业' if is_closed else '营业中'}")
            except Exception as e:
                print(f"   [{i}] 读取失败：{e}")
            
        target_url = None
        best_match_score = 0
        best_match_element = None
            
        # 遍历所有结果，计算地址匹配度
        for element in elements:
            try:
                # 查找 title 部分获取名称和状态
                title_div = element.find_element(By.CLASS_NAME, "title")
                spans = title_div.find_elements(By.TAG_NAME, "span")
                
                if len(spans) >= 1:
                    restaurant_name = spans[0].text.strip()
                    status_text = spans[1].text.strip() if len(spans) > 1 else ""
                    is_closed = "Closed" in status_text
                else:
                    continue
                    
                # 查找地址
                try:
                    addr_div = element.find_element(By.CLASS_NAME, "address")
                    restaurant_address = addr_div.text.strip()
                except:
                    restaurant_address = ""
                    
                # 获取链接
                href = element.get_attribute("href") if element.tag_name == "a" else None
                if not href:
                    # 如果当前元素不是 a 标签，查找父级 a 标签
                    try:
                        parent_link = element.find_element(By.XPATH, ".//a")
                        href = parent_link.get_attribute("href")
                    except:
                        continue
                
                if not href or href.startswith("https://support.google.com"):
                    continue
                    
                # 计算地址匹配分数
                match_score = calculate_address_match(address, restaurant_address)
                    
                print(f"   → 匹配度 {match_score:.1f}%: {restaurant_name} | {restaurant_address[:50]}... | {'已结业' if is_closed else '营业中'}")
                    
                # 如果匹配度超过阈值（比如 70%），认为找到了目标
                if match_score > best_match_score:
                    best_match_score = match_score
                    best_match_element = element
                    if href.startswith("/"):
                        target_url = BASE_URL + href
                    else:
                        target_url = href
                        
                    # 保存状态信息
                    target_is_closed = is_closed
                        
            except Exception as e:
                print(f"   ✗ 处理元素失败：{e}")
                continue
            
        driver.quit()
            
        if not target_url or best_match_score < 30:  # 最低匹配度要求
            return "未找到匹配店铺", search_url
            
        # 根据找到的结果返回状态
        if target_is_closed:
            status = "已结业"
        else:
            status = "营业中"
            
        return status, target_url
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"   ✗ 查询过程出错 [{error_type}]: {error_msg[:100]}")
        return f"查询失败 ({error_type})", ""
    finally:
        # 确保关闭 driver
        if driver:
            try:
                driver.quit()
            except:
                pass

def calculate_address_match(expected_addr, actual_addr):
    """
    计算地址匹配度（0-100 分）
    不需要百分百匹配，主要内容大部分匹配即可
    """
    # 转换为小写进行比较
    expected = expected_addr.lower().strip()
    actual = actual_addr.lower().strip()
    
    # 如果完全相同，直接返回 100
    if expected == actual:
        return 100.0
    
    # 提取关键地址词汇（去掉常见的后缀词）
    common_words = ['shop', 'g/f', 'f/', 'floor', 'building', 'court', 'terrace', 'street', 'road', 'avenue', 
                   'block', 'phase', 'tower', 'wing', 'house', 'villa', 'garden', 'estate', 'centre', 'center']
    
    # 分割为单词
    expected_words = set(re.findall(r'\b\w+\b', expected))
    actual_words = set(re.findall(r'\b\w+\b', actual))
    
    # 过滤掉常见词
    expected_key = expected_words - set(common_words)
    actual_key = actual_words - set(common_words)
    
    # 计算 Jaccard 相似度
    if len(expected_key.union(actual_key)) == 0:
        return 0.0
    
    intersection = len(expected_key.intersection(actual_key))
    union = len(expected_key.union(actual_key))
    
    similarity = (intersection / union) * 100
    
    # 也考虑包含关系
    if expected in actual or actual in expected:
        similarity = max(similarity, 20.0)
    
    return similarity

def extract_shop_name(local_account):
    """
    从 Local Account Number 中提取店铺名称
    例如："潮興牛腩 Chiu Hing Stewed Beef" -> "潮興牛腩" 或 "Chiu Hing Stewed Beef"
    """
    # 如果包含中文和英文，优先使用中文部分（OpenRice 对中文搜索更准确）
    import re
    # 尝试提取中文部分
    chinese_match = re.match(r'^([\u4e00-\u9fa5]+)', local_account)
    if chinese_match:
        return chinese_match.group(1).strip()
    
    # 如果没有中文，返回英文名称（去掉括号等额外信息）
    # 例如："McDonald's (Yuen Long)" -> "McDonald's"
    name = local_account.split('(')[0].strip()
    return name

def main():
    print("正在读取 Excel 名单...")
    df = pd.read_excel(INPUT_EXCEL)
    
    # 确认必需的列存在
    required_columns = ['Local Account Number', 'Area', 'Address']
    for col in required_columns:
        if col not in df.columns:
            print(f"错误：找不到列 '{col}'")
            return
    
    # 删除空行
    df = df.dropna(subset=['Local Account Number'])
    
    results = []
    total = len(df)
    
    print(f"共 {total} 家店铺，开始批量查询...\n")
    
    for i, (index, row) in enumerate(df.iterrows()):
        shop_name = extract_shop_name(str(row['Local Account Number']).strip())
        area = str(row['Area']).strip()
        address = str(row['Address']).strip()
        
        print(f"({i+1}/{total}) 正在查询：{shop_name} | {area}")
        status, url = get_correct_restaurant_status(shop_name, area, address)
        print(f"  → 结果：{status}")
        
        results.append({
            "原始店名": row['Local Account Number'],
            "提取的店名": shop_name,
            "地区": area,
            "地址": address,
            "OpenRice 状态": status,
            "店铺网址": url
        })
        
        time.sleep(random.uniform(2.5, 4.5))  # 防封

    # 输出 Excel
    df_out = pd.DataFrame(results)
    df_out.to_excel(OUTPUT_EXCEL, index=False)
    print(f"\n✅ 全部完成！结果已保存到：{OUTPUT_EXCEL}")

if __name__ == "__main__":
    main()