import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
import yaml
import ast


def get_xpath_text(driver, xpath):
    return driver.find_element(By.XPATH, xpath).text


def export_symbols_as_txt(symbols, filename="symbols"):
    with open(filename+".txt", "w") as output:
        output.write(str(symbols))


def read_all_symbols_from_file(filepath):
    with open(filepath, 'r') as f:
        symbols = ast.literal_eval(f.read())
    return symbols


def get_config(yaml_path):
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


paths = get_config(r'config.yaml')


def get_total_number_of_symbol_pages(driver):
    return int(get_xpath_text(driver, paths['total_pages_xpath']))


def get_driver_from_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-certificate-errors')
    s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(executable_path=s.path, desired_capabilities=options.to_capabilities())
    driver.get(url)
    driver.implicitly_wait(1)

    return driver


def click_next_symbols_page(driver):
    next_page_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, paths['next_page_button_xpath'])))

    see_also_banner = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, paths['see_also_banner_xpath'])))
    actions = ActionChains(driver)
    actions.move_to_element(see_also_banner).perform()
    next_page_button.click()


def get_symbols_in_page(driver):
    symbols = []
    symbols_in_page = len(driver.find_elements(By.XPATH, "//table/tbody/tr"))
    for index in range(1, symbols_in_page + 1):
        symbol = get_xpath_text(driver, paths['symbols_in_page_xpath'] + str(index) + ']' + '/th/a')
        symbols.append(symbol)
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
        time.sleep(1)
    return [j for i in symbols for j in i]


# scrape each symbol

def go_to_key_data(driver):
    key_data_header_xpath = '/html/body/div[2]/div/main/div[2]/div[6]/div/div[1]/div/div[1]/h2'
    key_data_header = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, key_data_header_xpath)))
    actions = ActionChains(driver)
    actions.move_to_element(key_data_header).perform()


def get_symbol_row(driver, symbol):
    driver.get('https://www.nasdaq.com/market-activity/stocks/' + symbol)
    name = get_xpath_text(driver, paths['name_xpath']).split(" (")[0]
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, paths['price_xpath'])))
    price = float(get_xpath_text(driver, paths['price_xpath']).strip('$'))
    pricing_changes = get_xpath_text(driver, paths['pricing_changes_xpath'])
    pricing_percentage_changes = get_xpath_text(driver, paths['pricing_change_percentage_xpath'])
    go_to_key_data(driver)
    sector = get_xpath_text(driver, paths['sector_xpath'])
    industry = get_xpath_text(driver, paths['industry_xpath'])
    market_cap = get_xpath_text(driver, paths['market_cap_xpath'])
    share_volume = get_xpath_text(driver, paths['share_volume_xpath'])
    earnings_per_share = get_xpath_text(driver, paths['earnings_per_share_xpath'])
    annualized_dividend = get_xpath_text(driver, paths['annualized_dividend_xpath'])
    dividend_pay_date = get_xpath_text(driver, paths['dividend_pay_date_xpath'])
    symbol_yield = get_xpath_text(driver, paths['yield_xpath'])
    beta = get_xpath_text(driver, paths['beta_xpath'])

    return {"name": name, "price": price, "pricing_changes": pricing_changes,
            "pricing_percentage_changes": pricing_percentage_changes, "sector": sector, "industry": industry,
            "market_cap": market_cap, "share_volume": share_volume, "earnings_per_share": earnings_per_share,
            "annualized_dividend": annualized_dividend, "dividend_pay_date": dividend_pay_date,
            "symbol_yield": symbol_yield, "beta": beta}
