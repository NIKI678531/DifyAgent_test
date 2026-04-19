from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil
import os

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
driver.get("https://www.openrice.com/en/hongkong/")
elements = driver.find_elements(By.CLASS_NAME, "pois-closed-restaurants-content")
for index, element in enumerate(elements):
    title = element.find_element(By.CLASS_NAME, "title")
    print(f"第{index+1}个条目的餐厅名字是：{title.text}")
    price = element.find_element(By.CLASS_NAME, "address")
    print(f"第{index+1}个条目的地址是：{price.text}")
driver.close()
