from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import logging

def open_chome():
    # Tạo Chrome options
    chrome_options = Options()
    # Chỉ hiển thị lỗi nghiêm trọng
    chrome_options.add_argument('--log-level=3')
    # Tắt logging
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Thiết lập lưu
    prefs = {
        "download.default_directory": r"D:\Python_Code\Save_HD",
        "download.prompt_for_download": False,        
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Khởi tạo
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.meinvoice.vn/tra-cuu')
    return driver

def lay_ma_hoa_don_tu_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readline().strip()

def lay_danh_sach_ma_hoa_don_tu_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("log_hoa_don.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def xu_ly_tra_cuu(driver, ma_hoa_don):
    """Xử lý tra cứu, Nhập mã hoá đơn"""
    xpath_input = '//*[@id="txtCode"]'
    element = driver.find_element(By.XPATH, xpath_input)
    element.send_keys(ma_hoa_don)
    logging.info(f"Đã nhập mã hóa đơn")

def xu_ly_submit(driver):
    """Xử lý submit"""
    xpath_submit = '//*[@id="btnSearchInvoice"]'
    element = driver.find_element(By.XPATH, xpath_submit)
    element.click()
    logging.info("Đã nhấn nút Tìm kiếm")

def kiem_tra_ket_qua(driver):
    """Kiểm tra kết quả"""
    xpath_ket_qua = '//*[@id="e-infomation"]'
    xpath_hien_thi = '//*[@id="popup-invoicnotexist-content"]/div'
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_ket_qua))
        )
        logging.info("Đã tìm thấy thông tin hóa đơn.")
        return True
    except:
        try:
            element_hien_thi = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_hien_thi))
            )
            logging.warning(element_hien_thi.text)
        except:
            logging.error("Không tìm thấy lỗi rõ ràng!")


def tai_hoa_don(driver):
    """Tải hoá đơn"""
    try:
        wait = WebDriverWait(driver, 10)
        
        
        download_button = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "download-invoice"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        time.sleep(1)  
        
        driver.execute_script("arguments[0].click();", download_button)
        logging.info("Đã nhấn nút 'Tải hóa đơn'.")
        
        # Chờ menu
        menu = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "download-menu"))
        )
        
        pdf_button = menu.find_element(By.CLASS_NAME, "txt-download-pdf")
        driver.execute_script("arguments[0].click();", pdf_button)
        logging.info("Đã chọn tải hóa đơn dạng PDF.")
        
        time.sleep(2)
        
    except Exception as e:
        logging.error(f"Lỗi khi tải hóa đơn PDF: {str(e)}")


def main():
    setup_logging()
    driver = open_chome()
    danh_sach_ma = lay_danh_sach_ma_hoa_don_tu_txt('ma_hoa_don.txt')
    for ma_hoa_don in danh_sach_ma:
        xu_ly_tra_cuu(driver, ma_hoa_don)
        xu_ly_submit(driver)
        if kiem_tra_ket_qua(driver):
            tai_hoa_don(driver)
        else:
            logging.info(f"Không có thông tin hóa đơn")
        driver.get('https://www.meinvoice.vn/tra-cuu')
        time.sleep(1)
    driver.quit()

main()