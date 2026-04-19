import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.openrice.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
    "Referer": "https://www.openrice.com/en/hongkong/"
}

URLS = [
    "https://www.openrice.com/en/hongkong/restaurants/district/sheung-wan?poiType=1&sortBy=ORScoreDesc&categoryGroupId=10002",
    "https://www.openrice.com/en/hongkong/restaurants/district/sheung-wan?poiType=1&sortBy=ORScoreDesc&cuisineId=6000&cuisineId=3010&categoryGroupId=10012&categoryGroupId=10013",
    "https://www.openrice.com/en/hongkong/restaurants/cuisine/hong-kong-style?categoryGroupId=10008&districtId=1001&poiType=1&sortBy=ORScoreDesc",
    "https://www.openrice.com/en/hongkong/restaurants/cuisine/western?poiType=1&sortBy=ORScoreDesc&districtId=1001",

    # jap hk
]

def get_all_restaurant_links(listing_url, limit=None):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment if you want headless scraping
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(listing_url)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    max_scroll = 150
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or (limit and len(driver.find_elements(By.CLASS_NAME, "poi-list-cell-desktop-right-link-overlay")) >= limit):
            break
        last_height = new_height
        scroll_count += 1
        if scroll_count >= max_scroll:
            print("Max scroll limit reached.")
            break

    elements = driver.find_elements(By.CLASS_NAME, "poi-list-cell-desktop-right-link-overlay")
    print(f"DEBUG: {listing_url} -- Found {len(elements)} elements")
    links = []
    for a in elements:
        href = a.get_attribute("href")
        if href and href.startswith("/"):
            links.append(BASE_URL + href)
        elif href:
            links.append(href)
        if limit and len(links) >= limit:
            break
    driver.quit()
    return links

def get_brand_name(outlet_name):
    match = re.match(r"^(.*?)\s*[\(\（]", outlet_name)
    if match:
        return match.group(1).strip()
    return outlet_name.strip()

def get_restaurant_info(url):
    resp = requests.get(url, headers=HEADERS, verify=False)
    soup = BeautifulSoup(resp.text, "lxml")
    # Chinese name
    name_tag = soup.find("span", class_="name")
    name = name_tag.get_text(strip=True) if name_tag else ""
    # English name (may be missing)
    en_tag = soup.find("div", class_="smaller-font-name")
    english_name = en_tag.get_text(strip=True) if en_tag else ""
    # Address
    address_tag = soup.find("a", attrs={"data-href": "#map"})
    address = address_tag.get_text(strip=True) if address_tag else ""
    return name, english_name, address

if __name__ == "__main__":
    limit = None
    all_links = set()
    for url in URLS:
        links = get_all_restaurant_links(url, limit=limit)
        all_links.update(links)
    all_links = list(all_links)
    print(f"Total unique restaurants after all URLs: {len(all_links)}")

    results = []
    for i, url in enumerate(all_links, 1):
        try:
            name, english_name, address = get_restaurant_info(url)
            print(f"{i}. {name} | {english_name} | {address}")
            brand_name = get_brand_name(english_name) if english_name else get_brand_name(name)
            results.append({
                "Brand Name": brand_name,
                "Outlet Name": name,
                "Outlet English Name": english_name,
                "Address": address,
                "Source": "OpenRice"
            })
            time.sleep(1)
        except Exception as e:
            print(f"Error on {url}: {e}")

    with open("results.csv", "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Brand Name", "Outlet Name", "Outlet English Name", "Address", "Source"]
        )
        writer.writeheader()
        writer.writerows(results)

    print("Done! Saved to results.csv")