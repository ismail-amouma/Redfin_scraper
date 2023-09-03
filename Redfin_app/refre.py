from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
def refresh ():
    chrome_options = Options()

	
    chrome_options.add_argument("--profaile-directory=Default")
    chrome_options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("Your link or the sheet here ")

    button=driver.find_element(By.XPATH,'(//div[@aria-label="coeff__onsheetRunDataImport "])[1]')
    button.click()
    time.sleep(3)
    print("refreshed")
    driver.quit()
    return None

