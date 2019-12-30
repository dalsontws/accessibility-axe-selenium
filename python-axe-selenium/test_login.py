from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from axe_selenium_python import Axe
import time

driver = webdriver.Chrome()
driver.maximize_window()
url = 'https://www.cpf.gov.sg/eSvc/Web/PortalServices/CpfMemberPortalServices'
driver.get(url)

time.sleep(60)
# WebDriverWait(driver, 400).until(
#     driver.find_element_by_class_name("page-title").text == "My cpf Homepage")

print('completed')
