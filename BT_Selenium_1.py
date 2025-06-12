from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
import time

# Tắt Thông báo popup Chomre
options = Options()
options.add_argument("--incognito")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})
options.add_argument("--user-data-dir=C:/Selenium/ChromeProfile")  

driver = webdriver.Chrome(options=options)

# Danh sách tài khoản và mật khẩu
usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]
password = "secret_sauce"

# Đăng nhập lần lượt cho tất cả username, password và nhấn Login.
def Login_Get_Product(driver, username, password):
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # Kiểm tra đăng nhập thành công và lấy sản phẩm và giá
    product_list = []
    if "inventory.html" in driver.current_url:
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            product_list.append((username, name, price))

        # Đăng xuất
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "logout_sidebar_link")))
        logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
        logout_button.click()

    return product_list

# Hàm lưu file Excel
def Save_To_Excel(data):
    workbook = xlsxwriter.Workbook('products.xlsx')
    worksheet = workbook.add_worksheet("Sauce Products")
    worksheet.write(0, 0, "Username")
    worksheet.write(0, 1, "Product Name")
    worksheet.write(0, 2, "Price")

    for row, (username, name, price) in enumerate(data, start=1):
        worksheet.write(row, 0, username)
        worksheet.write(row, 1, name)
        worksheet.write(row, 2, price)

    workbook.close()

# 
all_products = []
for username in usernames:
    result = Login_Get_Product(driver, username, password)
    all_products.extend(result)

driver.quit()
Save_To_Excel(all_products)



