import os
import shutil
import sys
import traceback

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def find_chromedriver():
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        return chromedriver_path

    possible_paths = [
        "/opt/homebrew/bin/chromedriver",
        "/usr/local/bin/chromedriver",
        "/opt/homebrew/Caskroom/chromedriver/latest/chromedriver-mac-arm64/chromedriver",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


chrome_options = Options()
chrome_binary = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if os.path.exists(chrome_binary):
    chrome_options.binary_location = chrome_binary

print("Python executable:", sys.executable)
print("Selenium version:", selenium.__version__)
print("PATH chromedriver:", find_chromedriver())
print("Chrome binary exists:", os.path.exists(chrome_binary))

driver = None

try:
    # Selenium 4 can manage the driver automatically, which is usually more
    # reliable across IDEs than hard-coding a local chromedriver path.
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://m.anjuke.com/jn/sale/")
    elements = driver.find_elements(By.CLASS_NAME, "item-wrap")
    for index, element in enumerate(elements):
        title = element.find_element(By.CLASS_NAME, "content-title")
        print(f"第{index + 1}个条目的标题是：{title.text}")
        price = element.find_element(By.CLASS_NAME, "content-price")
        print(f"第{index + 1}个条目的价格是：{price.text}")
except Exception as exc:
    print("Chrome 启动失败，完整报错如下：")
    print(type(exc).__name__, exc)
    traceback.print_exc()
finally:
    if driver is not None:
        driver.quit()

