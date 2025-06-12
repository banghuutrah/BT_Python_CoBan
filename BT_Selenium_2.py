from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def Collect_Data():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # Truy cập trang đầu để lấy số trang
    driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
    time.sleep(2)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination a")))
    page_links = driver.find_elements(By.CSS_SELECTOR, ".pagination a")

    total_pages = 1
    for link in page_links:
        text = link.text.strip()
        if text.isdigit():
            total_pages = max(total_pages, int(text))

    print(f"Tổng số trang tìm được là: {total_pages}")

    # Thu thập tên doanh nghiệp, mã số thuế, ngày cấp của tất cả các trang
    all_data = {}
    base_url = "https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep?page={}"

    for page_num in range(1, total_pages + 1):
        print(f"Trang {page_num} / {total_pages}")
        driver.get(base_url.format(page_num))
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        page_data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 4:
                mst = cols[1].text.strip()
                ten_dn = cols[2].text.strip()
                ngay_cap = cols[3].text.strip()
                page_data.append({
                    "Mã số thuế": mst,
                    "Tên doanh nghiệp": ten_dn,
                    "Ngày cấp": ngay_cap
                })

        all_data[f"Trang_{page_num}"] = pd.DataFrame(page_data)

    driver.quit()
    return all_data

def Save_To_Excel(data, ten_file):
    with pd.ExcelWriter(ten_file, engine="xlsxwriter") as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Đã lưu vào file: {ten_file}")

def main():
    data = Collect_Data()
    Save_To_Excel(data, "Thongtin.xlsx")

main()  

