from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
import xml.etree.ElementTree as ET
# Đọc lần lượt excel đầu vào(mã số thuế, mã hoá đơn, URL)
def input_excel(file_path):
    df = pd.read_excel(file_path, dtype=str)
    data = []
    for _, row in df.iterrows():
        mst = str(row['MST']).strip() if pd.notna(row['MST']) else ''
        ma_tra_cuu = str(row['MaTraCuu']).strip() if pd.notna(row['MaTraCuu']) else ''
        url = str(row['URL']).strip() if pd.notna(row['URL']) else ''
        if url:
            data.append((mst, ma_tra_cuu, url))
    return data
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("log_hoa_don.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
# lần lượt tra cứu
# Bước 1: Truy cập trang web tra cứu hoá đơn
def open_chome(url):
    chrome_options = Options()
    # Chỉ hiển thị lỗi nghiêm trọng
    chrome_options.add_argument('--log-level=3')
    # Tắt logging
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {
        "download.default_directory": r"D:\Python_Code\Save_HD",
        "download.prompt_for_download": False,        
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver
# Bước 2: Nhập thông tin tra cứu
# FPT
def nhap_thong_tin_fpt(driver, mst, ma_tra_cuu):
    xpath_ma_so_thue = '//input[@placeholder="MST bên bán"]'
    xpath_ma_tra_cuu = '//input[@placeholder="Mã tra cứu hóa đơn"]'
    element_mst = driver.find_element(By.XPATH, xpath_ma_so_thue)
    element_mst.clear()
    element_mst.send_keys(mst)
    element_ma_tra_cuu = driver.find_element(By.XPATH, xpath_ma_tra_cuu)
    element_ma_tra_cuu.clear()
    element_ma_tra_cuu.send_keys(ma_tra_cuu)
# Meinvoice
def nhap_thong_tin_meinvoice(driver, ma_tra_cuu):
    xpath_ma_tra_cuu = '//*[@id="txtCode"]'
    element_ma_tra_cuu = driver.find_element(By.XPATH, xpath_ma_tra_cuu)
    element_ma_tra_cuu.clear()
    element_ma_tra_cuu.send_keys(ma_tra_cuu)
# EhoaDon
def nhap_thong_tin_ehoadon(driver, ma_tra_cuu):
    xpath_ma_tra_cuu = '//*[@id="txtInvoiceCode"]'
    element_ma_tra_cuu = driver.find_element(By.XPATH, xpath_ma_tra_cuu)
    element_ma_tra_cuu.clear()
    element_ma_tra_cuu.send_keys(ma_tra_cuu)
# Bước 3: Thực hiện tra cứu
def xu_ly_submit_fpt(driver):
    xpath_submit = '//div[@view_id="search:btnsearch"]//button'
    element_submit = driver.find_element(By.XPATH, xpath_submit)
    element_submit.click()
    
def xu_ly_submit_meinvoice(driver):
    xpath_submit = '//*[@id="btnSearchInvoice"]'
    element_submit = driver.find_element(By.XPATH, xpath_submit)
    element_submit.click()
    
def xu_ly_submit_ehoadon(driver):
    xpath_submit = '//*[@id="Button1"]'
    element_submit = driver.find_element(By.XPATH, xpath_submit)
    element_submit.click()
# Bước 4: Xem và tải hoá đơn
#--mã tra cứu sai: xuất hiện màn hình thông báo lỗi
#--mã tra cứu đúng: xuất hiện màn hình tải hoá đơn
def kiem_tra_ket_qua_fpt(driver):
    xpath_ket_qua = '//span[@class="igreen"]'
    xpath_hien_thi = '//div[@class="webix_inp_bottom_label"]'
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_ket_qua))
        )
        return True
    except:
        try:
            element_hien_thi = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_hien_thi))
            )
            logging.warning(element_hien_thi.text)
        except:
            logging.warning("Không tìm thấy lỗi rõ ràng!")
    return False
def kiem_tra_ket_qua_meinvoice(driver):
    xpath_ket_qua = '//*[@id="e-infomation"]'
    xpath_hien_thi = '//div[@id="popup-invoicnotexist-content"]/div'
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_ket_qua))
        )
        return True
    except:
        try:
            element_hien_thi = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_hien_thi))
            )
            logging.warning(element_hien_thi.text)
        except:
            logging.warning("Không tìm thấy lỗi rõ ràng!")
    return False
def kiem_tra_ket_qua_ehoadon(driver):
    xpath_ket_qua = '//*[@id="ui-id-1"]'
    xpath_sai = '//div[@id="Bkav_alert_dialog"]'
    xpath_dung = '//*[@id="ViewInvoice"]'
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_ket_qua))
        )
        try:
            element_sai = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_sai))
            )
            if "không đúng" in element_sai.text.lower():
                logging.warning(element_sai.text)
                return False
        except:
            pass
        try:
            element_dung = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_dung))
            )
            if element_dung.is_displayed():
                logging.info("Thông tin hóa đơn đã được tìm thấy.")
                return True
        except:
            pass
        logging.warning("Không xác định")
        return False
    except Exception as e:
        logging.error(f"Lỗi khi kiểm tra kết quả: {e}")
        return False
#--Xử lý download
def xu_ly_download_fpt(driver):
    xpath_download = '//div[@view_id="search:btnxml"]//button'
    wait = WebDriverWait(driver, 10)
    element_download = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath_download))
    )
    element_download.click()
    logging.info("Đã nhấn nút 'Tải hóa đơn'.")
def xu_ly_download_meinvoice(driver):
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
        
        xml_button = menu.find_element(By.CLASS_NAME, "txt-download-xml")
        driver.execute_script("arguments[0].click();", xml_button)
        logging.info("Đã chọn tải hóa đơn dạng XML.")
        
        time.sleep(2)
        
    except Exception as e:
        logging.error(f"Lỗi khi tải hóa đơn PDF: {str(e)}")
def xu_ly_download_ehoadon(driver):
    xpath_iframe = '//*[@id="frameViewInvoice"]'
    xpath_menu = '//*[@id="btnDownload"]'
    xpath_download_XML = '//*[@id="LinkDownXML"]'
    try:
        wait = WebDriverWait(driver, 10)
        element_iframe = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath_iframe))
        )
        driver.switch_to.frame(element_iframe)
        logging.info("Đã chuyển sang iframe chứa hóa đơn.")

        element_menu = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath_menu))
        )
        element_menu.click()
        logging.info("Đã nhấn nút 'Tải hóa đơn'.")

        element_XML = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath_download_XML))
        )
        element_XML.click()
        logging.info("Đã chọn tải hóa đơn dạng XML.")
    except Exception as e:
        logging.error(f"Lỗi khi tải hóa đơn XML: {str(e)}")
    finally:
        driver.switch_to.default_content()

# Bước 5: Đọc file hoá đơn
def read_xml_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Lỗi đọc file {file_path}: {e}")
        return None

def get_latest_xml_file(folder_path, before_files):
    xml_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.xml')]
    new_files = list(set(xml_files) - set(before_files))
    if not new_files:
        return None
    new_files = sorted(new_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    return os.path.join(folder_path, new_files[0])
# Bước 6: Trích xuất thông tin hoá đơn và lưu vào file excel
# Lấy nội dung file xml
# Trích xuất
def extract_fpt(xml_content):
    # Trích xuất thông tin từ XML FPT
    try:
        root = ET.fromstring(xml_content)

        # Vào đúng nhánh HDon
        hdon = root.find('.//DLieu/HDon')
        ttchung = hdon.find('.//DLHDon/TTChung')
        nban = hdon.find('.//DLHDon/NDHDon/NBan')
        nmua = hdon.find('.//DLHDon/NDHDon/NMua')

        data = {
            'Số hóa đơn': ttchung.findtext('SHDon', ''),
            'Đơn vị bán hàng': nban.findtext('Ten', ''),
            'Mã số thuế bán': nban.findtext('MST', ''),
            'Địa chỉ bán': nban.findtext('DChi', ''),
            'Số tài khoản bán': '',  # Không có thông tin STK trong XML này
            'Họ tên người mua hàng': nmua.findtext('HVTNMHang', '') or nmua.findtext('Ten', ''),
            'Địa chỉ mua': nmua.findtext('DChi', ''),
            'Mã số thuế mua': nmua.findtext('MST', '')
        }

        return data

    except Exception as e:
        logging.error(f"Lỗi FPT: {e}")
        return {}

def extract_meinvoice(xml_content):
    try:
        root = ET.fromstring(xml_content)

        # Truy cập các phần tử chính xác không dùng namespace
        ttchung = root.find('.//DLHDon/TTChung')
        nban = root.find('.//DLHDon/NDHDon/NBan')
        nmua = root.find('.//DLHDon/NDHDon/NMua')

        data = {
            'Số hóa đơn': ttchung.findtext('SHDon', ''),
            'Đơn vị bán hàng': nban.findtext('Ten', ''),
            'Mã số thuế bán': nban.findtext('MST', ''),
            'Địa chỉ bán': nban.findtext('DChi', ''),
            'Số tài khoản bán': nban.findtext('STKNHang', ''),
            'Họ tên người mua hàng': nmua.findtext('HVTNMHang', '') or nmua.findtext('Ten', ''),
            'Địa chỉ mua': nmua.findtext('DChi', ''),
            'Mã số thuế mua': nmua.findtext('MST', '')
        }

        return data

    except Exception as e:
        logging.error(f"Lỗi Meinvoice: {e}")
        return {}

def extract_ehoadon(xml_content):
    try:
        root = ET.fromstring(xml_content)

        # Tìm các node chính
        ttchung = root.find('.//DLHDon/TTChung')
        nban = root.find('.//DLHDon/NDHDon/NBan')
        nmua = root.find('.//DLHDon/NDHDon/NMua')

        data = {
            'Số hóa đơn': ttchung.findtext('SHDon', ''),
            'Đơn vị bán hàng': nban.findtext('Ten', ''),
            'Mã số thuế bán': nban.findtext('MST', ''),
            'Địa chỉ bán': nban.findtext('DChi', ''),
            'Số tài khoản bán': '',  # Không có trường STK trong file
            'Họ tên người mua hàng': nmua.findtext('HVTNMHang', '') or nmua.findtext('Ten', ''),
            'Địa chỉ mua': nmua.findtext('DChi', ''),
            'Mã số thuế mua': nmua.findtext('MST', '')
        }

        return data

    except Exception as e:
        logging.error(f"Lỗi Ehoadon: {e}")
        return {}

def save_to_excel(results, filename):
    """Lưu danh sách kết quả vào file Excel"""
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    logging.info(f"Đã lưu thông tin hóa đơn vào {filename}")

# Main
def main():
    data = input_excel('Du_Lieu_Input.xlsx')  # Đọc file excel đầu vào
    folder_path = r"D:\Python_Code\Save_HD"
    results = []
    for mst, ma_tra_cuu, url in data:
        before_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.xml')]
        driver = open_chome(url)
        if 'fpt' in url:
            nhap_thong_tin_fpt(driver, mst, ma_tra_cuu)
            xu_ly_submit_fpt(driver)
            if kiem_tra_ket_qua_fpt(driver):
                xu_ly_download_fpt(driver)
            time.sleep(5)
        elif 'meinvoice' in url:
            nhap_thong_tin_meinvoice(driver, ma_tra_cuu)
            xu_ly_submit_meinvoice(driver)
            if kiem_tra_ket_qua_meinvoice(driver):
                xu_ly_download_meinvoice(driver)
            time.sleep(5)
        elif 'ehoadon' in url:
            nhap_thong_tin_ehoadon(driver, ma_tra_cuu)
            xu_ly_submit_ehoadon(driver)
            if kiem_tra_ket_qua_ehoadon(driver):
                xu_ly_download_ehoadon(driver)
            time.sleep(5)
        else:
            logging.warning("URL không hợp lệ!")
        time.sleep(2)
        driver.quit()
        # Lấy file XML mới nhất vừa tải về
        xml_path = get_latest_xml_file(folder_path, before_files)
        if xml_path:
            xml_content = read_xml_content(xml_path)
            if 'fpt' in url:
                info = extract_fpt(xml_content)
            elif 'meinvoice' in url:
                info = extract_meinvoice(xml_content)
            elif 'ehoadon' in url:
                info = extract_ehoadon(xml_content)
            else:
                info = {}
        else:
            info = {}
        row = {
            'MST Input': mst,
            'Mã tra cứu Input': ma_tra_cuu,
            'URL Input': url
        }
        row.update(info)
        results.append(row)
    save_to_excel(results, "output_hoadon.xlsx")

main()