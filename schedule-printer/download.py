import os
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ROOT = os.getcwd()
ASSETS_FOLDER = os.path.join(ROOT, 'assets')
CHROME_FOLDER = os.path.join(ROOT, 'chrome')
USERNAME = 'ryoung'
PASSWORD = '980parkave'
AUTH = {'username': USERNAME, 'value': PASSWORD}


def make_driver() -> webdriver.Chrome:
    """return browser object"""
    service = Service(os.path.join(CHROME_FOLDER, 'chromedriver.exe'))
    options = ChromeOptions()
    options.binary_location = os.path.join(CHROME_FOLDER, 'chrome.exe')
    options.add_argument('--headless')
    return webdriver.Chrome(service=service, options=options)


def login(driver: webdriver.Chrome) -> webdriver.Chrome:
    """log into the homepage using username/password found above in AUTH, and return browser object"""
    driver.get('https://secure.rotundasoftware.com/29/msp/web-terminal/home?user=StIgnatiusLoyolaNYC')
    for key, value in AUTH.items():
        cond = EC.element_to_be_clickable(driver.find_element(By.NAME, key))
        field = WebDriverWait(driver, 20).until(cond)
        field.send_keys(value)
    cond = EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, 'button.button'))
    submit = WebDriverWait(driver, 20).until(cond)
    submit.click()
    return driver


def select_schedule(driver: webdriver.Chrome) -> webdriver.Chrome:
    """navigate to schedule tab, and return browser object"""
    xpath = "html/body/div[@id='page-view']/header/nav/ul/li[3]/a"
    cond = EC.element_to_be_clickable(driver.find_element(By.XPATH, xpath))
    tab = WebDriverWait(driver, 20).until(cond)
    tab.click()
    return driver


def save_schedule(driver: webdriver.Chrome) -> webdriver.Chrome:
    """save schedule to the assets folder for further processing"""
    with open(os.path.join(ASSETS_FOLDER, 'schedule.html'), mode='w+') as fp: 
        fp.write(driver.page_source)
    return driver


def load_schedule() -> str:
    """load last saved schedule from assets folder, returning as raw string"""
    try: 
        with open(os.path.join(ASSETS_FOLDER, 'schedule.html')) as fp: 
            schedule = fp.read()
        return schedule
    except FileNotFoundError:
        raise Exception('No schedule found (tip: run download.py first)')
        

def main():
    """execute each of the above functions sequentially, waiting in between"""
    driver = make_driver()
    driver = login(driver); time.sleep(0.5)
    driver = select_schedule(driver); time.sleep(0.5)
    driver = save_schedule(driver); time.sleep(0.5)
    return driver


if __name__ == '__main__':
    main()
