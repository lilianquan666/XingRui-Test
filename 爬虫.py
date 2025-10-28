from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv


# 配置浏览器和驱动路径
chrome_exe_path = r"C:\迅雷下载\chrome-win64\chrome.exe"
chromedriver_path = r"C:\迅雷下载\chromedriver-win64\chromedriver.exe"

# 初始化浏览器（保持浏览器打开，等待手动筛选）
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_exe_path
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开目标页面
driver.get("https://www.chinamoney.com.cn/english/bdInfo/")
print("请在浏览器中手动筛选：")
print("1. 选择 Bond Type = Treasury Bond")
print("2. 选择 Issue Year = 2023")
print("3. 筛选完成后回到此窗口按 Enter 键继续")
input("按 Enter 键开始提取数据...")  # 等待手动操作完成

try:
    # 提取当前页面已筛选的表格数据
    table = driver.find_element(By.XPATH, '//*[@id="sheet-bond-market"]/div[1]/div/table')
    
    # 提取列名
    columns = [col.text.strip() for col in table.find_elements(By.XPATH, './thead/tr/td')]
    
    # 提取所有行数据（当前页面已筛选的结果）
    rows = []
    for row in table.find_elements(By.XPATH, './tbody/tr'):
        cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, './td')]
        if len(cells) == len(columns) and cells:
            rows.append(dict(zip(columns, cells)))
    
    # 保存数据
    target_columns = ["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]
    valid_columns = [col for col in target_columns if col in columns]
    
    with open("manual_filtered_bonds.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=valid_columns)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"已提取 {len(rows)} 条手动筛选后的数据，保存至 ShuJu.csv")

except Exception as e:
    print(f"提取数据出错：{str(e)}")

finally:
    driver.quit()