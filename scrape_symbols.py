import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec


def get_total_number_of_symbol_pages(driver):
    return int(driver.find_element(By.XPATH,
                                   '/html/body/div[2]/div/main/div[2]/article/div[3]/div[1]/div/div/div[3]/div[5]/div/button[8]').text)


def get_driver_from_url(url):
    s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(executable_path=s.path)
    driver.get(url)
    driver.implicitly_wait(1)
    return driver


def click_next_symbols_page(driver):
    next_page_button_xpath = '/html/body/div[2]/div/main/div[2]/article/div[3]/div[1]/div/div/div[3]/div[5]/button[2]'
    next_page_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, next_page_button_xpath)))
    see_also_banner_xpath = '/html/body/div[2]/div/main/div[2]/article/div[3]/div[1]/aside/div'
    see_also_banner = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, see_also_banner_xpath)))
    actions = ActionChains(driver)
    actions.move_to_element(see_also_banner).perform()
    next_page_button.click()


def get_symbols_in_page(driver):
    symbols = []
    symbols_in_page = len(driver.find_elements(By.XPATH, "//table/tbody/tr"))
    for index in range(1, symbols_in_page + 1):
        symbol = driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div/main/div[2]/article/div[3]/div[1]/div/div/div[3]/div[3]/table/tbody/tr[' + str(
                                         index) + ']' + '/th/a')
        symbols.append(symbol.text)
    return symbols


def get_all_symbols(driver):
    symbol_pages = get_total_number_of_symbol_pages(driver)
    symbols = []
    print("número de páginas: " + str(symbol_pages))
    print("Obteniendo páginas. Por favor, espere...")
    for page in range(0, symbol_pages):
        symbols.append(get_symbols_in_page(driver))
        if page < 335:
            click_next_symbols_page(driver)
        time.sleep(0.5)
    return [j for i in symbols for j in i]
###### scrape each symbol ######

def go_to_key_data(driver):
    key_data_header_xpath = '/html/body/div[2]/div/main/div[2]/div[6]/div/div[1]/div/div[1]/h2'
    key_data_header = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, key_data_header_xpath)))
    actions = ActionChains(driver)
    actions.move_to_element(key_data_header).perform()

