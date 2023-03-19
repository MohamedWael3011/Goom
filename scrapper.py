from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
options = Options()
options.add_argument('--allow-insecure-localhost')
options.add_argument('--headless')
options.add_argument("--incognito")
options.add_argument("--nogpu")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,1280")
options.add_argument("--no-sandbox")
options.add_argument("--enable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

def GetTraits(url): #['Goomble #2620', '', 'back / None', 'background / Banana', 'body / Round', 'clothes / None', 'eyes / Angry', 'flavor / Powdered Sugar Blue', 'headwear / Troll Horns', 'left hand / Wrench', 'mouth / Fangs', 'right hand / None', 'Goombles', 'www.goombles.io']
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    elements = driver.find_elements(By.XPATH, '//div[@class="s t wc hc"]')
    traits = {}
    for element in elements:
        val = element.text
        if '/' in val:
            AttVal = val.split('/')
            traits[AttVal[0]] = AttVal[1]
    
    GoombleID = elements[0].text
        
    driver.quit()
    
    return traits,GoombleID




    
    
    
    
    
    
    
    
     
    
