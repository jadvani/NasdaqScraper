import logging
import time
import yaml
import ast
import os
from pathlib import Path

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome, ChromeOptions


def get_path():
    """
    Obtain the parent folder to reference other files
    :return: the parent folder as string
    """
    return os.getcwd().strip("src")


def export_symbols_as_txt(symbols, filename="symbols"):
    """
    Once the symbols have been scrapped, export them as a .txt file
    :param symbols: a List of strings containing the symbols found
    :param filename: the file name to store the symbols.
    """
    with open(Path(get_path() + "\\execution_results\\" +
                   filename + ".txt"), "w") as output:
        output.write(str(symbols))


def get_config(yaml_path):
    """
    Config file containing the identifiers for the different scrapping functionalities
    :param yaml_path: the path of the YAML file
    :return: the config dictionary to search by keys the web element identifiers
    """
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def get_xpath_text(driver, xpath):
    """
    Wrapper method to avoid long lines while calling the find_element functionality
    :param driver: the driver used
    :param xpath: the xpath to be found
    :return: the text from the element
    """
    return driver.find_element(By.XPATH, xpath).text


def read_all_symbols_from_file(filepath):
    """
    In case we do not want to scrape the symbols again, we can read them from a file
    :param filepath: the filepath for the symbols
    :return: the symbols as list of strings
    """
    with open(filepath, 'r') as f:
        symbols = ast.literal_eval(f.read())
    return symbols


def get_driver_from_url(url):
    """
    This method creates the driver to interact with the different elements in the website. Due to the high volume of
    elements being scrapped and webs to visit, some additional options added avoid the script to be blocked.
    :param url: The url to navigate.
    :return: The driver to interact with the website.
    """
    # adding options to avoid errors during intensive search loops
    options = ChromeOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-certificate-errors')
    s = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = Chrome(executable_path=s.path, desired_capabilities=options.to_capabilities())
    driver.get(url)
    driver.implicitly_wait(1)

    return driver


class NasdaqScrapper:
    paths = get_config(get_path() + '\\config\\config.yaml')

    def get_total_number_of_symbol_pages(self, driver):
        """
        This method get the last page number value
        :param driver: The driver being used for nasdaq screener site
        :return: the number (int) of pages in screener table
        """
        return int(get_xpath_text(driver, self.paths['total_pages_xpath']))

    def click_next_symbols_page(self, driver):
        """
        Once the elements from table page have been grabbed, we need to go to the next page,
        in order to keep grabbing the rest of the elements.
        :param driver: The driver to interact with Nasdaq screener website.
        """
        next_page_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.paths['next_page_button_xpath'])))
        # The web struggles to find the button if it is not visible.
        # A simple scroll down was not working always, but placing the web near to the banner actually works
        see_also_banner = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.paths['see_also_banner_xpath'])))
        actions = ActionChains(driver)
        actions.move_to_element(see_also_banner).perform()
        next_page_button.click()

    def get_symbols_in_page(self, driver):
        """
        Given the "screener" site, retrieve all symbols (1st column) from table.
        :param driver: The driver to interact with Nasdaq screener website.
        :return: The table symbols in page as a text list.
        """
        symbols = []
        symbols_in_page = len(driver.find_elements(By.XPATH, "//table/tbody/tr"))
        for index in range(1, symbols_in_page + 1):
            symbol = get_xpath_text(driver, self.paths['symbols_in_page_xpath'] + str(index) + ']' + '/th/a')
            symbols.append(symbol)
        return symbols

    def get_all_symbols(self, driver):
        """
        This method retrieves the whole list of symbols in table, passing the pages through.
        :param driver: The driver to interact with Nasdaq screener website
        :return: The table symbols from all pages as a text list.
        """
        symbol_pages = self.get_total_number_of_symbol_pages(driver)
        symbols = []
        print("número de páginas: " + str(symbol_pages))
        print("Obteniendo páginas. Por favor, espere...")
        for page in range(0, symbol_pages):
            symbols.append(self.get_symbols_in_page(driver))
            if page < 335:
                self.click_next_symbols_page(driver)
            time.sleep(1)
        return [j for i in symbols for j in i]

    # scrape each symbol

    def go_to_key_data(self, driver):
        """
        When retrieving an exact symbol information, place the visible screen over the key data info
        :param driver: The driver to interact with Nasdaq website
        """
        key_data_header = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.paths['key_data_header_xpath'])))
        actions = ActionChains(driver)
        actions.move_to_element(key_data_header).perform()

    def get_symbol_row(self, driver, symbol):
        """
        Given a symbol name, the method retrieves all the information details (row from our dataset)
        :param driver: The driver to interact with Nasdaq website
        :param symbol: The company symbol, as text (example: 'AAPL')
        :return:
        """
        driver.get(self.paths['stocks_url'] + symbol)
        name = get_xpath_text(driver, self.paths['name_xpath']).split(" (")[0]
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.paths['price_xpath'])))
        price = float(get_xpath_text(driver, self.paths['price_xpath']).strip('$'))
        pricing_changes = get_xpath_text(driver, self.paths['pricing_changes_xpath'])
        pricing_percentage_changes = get_xpath_text(driver, self.paths['pricing_change_percentage_xpath'])
        self.go_to_key_data(driver)
        sector = get_xpath_text(driver, self.paths['sector_xpath'])
        industry = get_xpath_text(driver, self.paths['industry_xpath'])
        market_cap = get_xpath_text(driver, self.paths['market_cap_xpath'])
        share_volume = get_xpath_text(driver, self.paths['share_volume_xpath'])
        earnings_per_share = get_xpath_text(driver, self.paths['earnings_per_share_xpath'])
        annualized_dividend = get_xpath_text(driver, self.paths['annualized_dividend_xpath'])
        dividend_pay_date = get_xpath_text(driver, self.paths['dividend_pay_date_xpath'])
        symbol_yield = get_xpath_text(driver, self.paths['yield_xpath'])
        errors = True
        try:
            beta = get_xpath_text(driver, self.paths['beta_xpath'])
            errors = False

        except Exception as e:
            logging.exception(e)
            beta = ''
        return {"name": name, "price": price, "pricing_changes": pricing_changes,
                "pricing_percentage_changes": pricing_percentage_changes, "sector": sector, "industry": industry,
                "market_cap": market_cap, "share_volume": share_volume, "earnings_per_share": earnings_per_share,
                "annualized_dividend": annualized_dividend, "dividend_pay_date": dividend_pay_date,
                "symbol_yield": symbol_yield, "beta": beta, "errors": errors}
