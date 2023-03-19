
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://pool.pm/asset1l5a64k0jwrr3es6njjuxy202x7t07cd4lw55zz")
soup = BeautifulSoup(driver.page_source, 'lxml')
divs = soup.findAll('div')
print(divs)

driver.close()