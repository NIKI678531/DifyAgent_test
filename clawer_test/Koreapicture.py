import os
import re
import time
from urllib.parse import quote

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

STAR_NAMES = [
    "玄彬", "李钟硕", "金秀贤", "朴叙俊", "车银优", "李敏镐", "孔刘", "宋仲基", "池昌旭", "丁海寅",
    "南柱赫", "朴炯植", "徐康俊", "玉泽演", "李栋旭", "金宇彬", "刘亚仁", "任时完", "李准基", "姜河那",
    "柳俊烈", "安孝燮", "边佑锡", "俞承豪", "禹棹焕", "金宣虎", "路云", "李洙赫", "李到晛", "黄旼炫",
    "邕圣祐", "朴宝剑", "尹施允", "张基龙", "吕珍九", "都敬秀", "EXO世勋", "金珉奎", "金英光", "郑容和",
    "崔振赫", "金南佶", "苏志燮", "赵寅成", "张东健", "元斌", "李阵郁", "柳演锡", "姜栋元", "郑雨盛",
]

OUTPUT_DIR = "/Users/lkq/Desktop/男韩国"
MIN_WIDTH = 800
MIN_HEIGHT = 1000
REQUEST_TIMEOUT = 20
SEARCH_DELAY = 1


def sanitize_filename(name):
    return re.sub(r'[\\\\/:*?"<>|]+', "_", name).strip()


def build_search_url(star_name):
    query = quote(f"{star_name} 韩国男明星 高清 人像")
    return f"https://www.google.com/search?tbm=isch&hl=zh-CN&q={query}"


def init_driver():
    options = Options()
    chrome_binary = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(chrome_binary):
        options.binary_location = chrome_binary

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=zh-CN")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )
    return driver


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def print_overall_progress(current_index, total_count, star_name, status):
    percent = current_index / total_count * 100
    print(f"[{current_index}/{total_count}] {percent:6.2f}% {star_name} - {status}")


def print_download_progress(star_name, downloaded, total):
    if total <= 0:
        print(f"    {star_name} 下载中: {downloaded / 1024:.1f} KB", end="\r", flush=True)
        return

    percent = downloaded / total * 100
    total_kb = total / 1024
    downloaded_kb = downloaded / 1024
    print(
        f"    {star_name} 下载中: {percent:6.2f}% ({downloaded_kb:.1f}KB/{total_kb:.1f}KB)",
        end="\r",
        flush=True,
    )


def guess_extension(content_type, img_url):
    content_type = (content_type or "").lower()
    if "jpeg" in content_type or "jpg" in content_type:
        return ".jpg"
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    if ".png" in img_url.lower():
        return ".png"
    if ".webp" in img_url.lower():
        return ".webp"
    return ".jpg"


def download_image(img_url, save_base_path, star_name):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.google.com/",
        }
        with requests.get(img_url, headers=headers, stream=True, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            downloaded = 0
            extension = guess_extension(response.headers.get("content-type"), img_url)
            final_path = f"{save_base_path}{extension}"

            with open(final_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    file.write(chunk)
                    downloaded += len(chunk)
                    print_download_progress(star_name, downloaded, total)

        print(" " * 100, end="\r")
        print(f"    {star_name} 下载完成: {final_path}")
        return final_path
    except Exception as exc:
        for extension in (".jpg", ".png", ".webp", ".gif"):
            maybe_path = f"{save_base_path}{extension}"
            if os.path.exists(maybe_path):
                os.remove(maybe_path)
        print(" " * 100, end="\r")
        print(f"    {star_name} 下载失败: {exc}")
        return None


def collect_large_image_candidates(driver):
    return driver.execute_script(
        """
        return Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.currentSrc || img.src || '',
            width: img.naturalWidth || 0,
            height: img.naturalHeight || 0
        }));
        """
    )


def pick_best_image_url(driver):
    candidates = collect_large_image_candidates(driver)
    valid_candidates = []

    for candidate in candidates:
        src = candidate.get("src", "")
        width = candidate.get("width", 0)
        height = candidate.get("height", 0)

        if not src.startswith("http"):
            continue
        if "gstatic.com" in src or "googleusercontent.com" in src:
            continue
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            continue
        valid_candidates.append((width * height, src))

    if not valid_candidates:
        return None

    valid_candidates.sort(reverse=True)
    return valid_candidates[0][1]


def open_google_images(driver, star_name):
    driver.get(build_search_url(star_name))
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img"))
    )
    time.sleep(SEARCH_DELAY)


def find_image_url_for_star(driver, star_name):
    open_google_images(driver, star_name)
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "img")

    for index, thumbnail in enumerate(thumbnails, start=1):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumbnail)
            time.sleep(0.4)
            thumbnail.click()
            time.sleep(1.2)

            img_url = pick_best_image_url(driver)
            if img_url:
                print(f"    {star_name} 已定位高清图片，来源候选序号: {index}")
                return img_url
        except Exception:
            continue

    return None


def crawl_star_image(driver, star_name, current_index, total_count):
    print_overall_progress(current_index, total_count, star_name, "开始搜索")

    img_url = find_image_url_for_star(driver, star_name)
    if not img_url:
        print_overall_progress(current_index, total_count, star_name, "未找到符合要求的高清图片")
        return False

    save_base_path = os.path.join(OUTPUT_DIR, sanitize_filename(star_name))

    print_overall_progress(current_index, total_count, star_name, "开始下载")
    saved_path = download_image(img_url, save_base_path, star_name)
    if saved_path:
        print_overall_progress(current_index, total_count, star_name, "完成")
        return True

    print_overall_progress(current_index, total_count, star_name, "下载失败")
    return False


def main():
    ensure_output_dir()
    driver = init_driver()
    success_count = 0
    total_count = len(STAR_NAMES)

    try:
        for index, star_name in enumerate(STAR_NAMES, start=1):
            try:
                if crawl_star_image(driver, star_name, index, total_count):
                    success_count += 1
            except TimeoutException:
                print_overall_progress(index, total_count, star_name, "页面加载超时，已跳过")
            except Exception as exc:
                print_overall_progress(index, total_count, star_name, f"发生异常，已跳过: {exc}")
    finally:
        driver.quit()

    print(f"\n全部任务结束: 成功下载 {success_count}/{total_count} 张图片")
    print(f"图片保存目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
