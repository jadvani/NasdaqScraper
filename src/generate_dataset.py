import logging

import pandas as pd
from datetime import datetime

from src.nasdaq_scrapper import NasdaqScrapper, get_path, get_driver_from_url, read_all_symbols_from_file, \
    export_symbols_as_txt

nasdaq_scrapper = NasdaqScrapper()

driver = get_driver_from_url(nasdaq_scrapper.paths['screener_url'])
# scrape all symbols (about 6 min)
# symbols = get_all_symbols(driver)
# export_symbols_as_txt(symbols)

# read symbols from file

symbols = read_all_symbols_from_file(get_path() + '\\execution_results\\symbols.txt')
symbols = symbols[0:5]
nasdaq_companies = pd.DataFrame()
errors = []


# about 3 secs per symbol
def insert_new_symbol_in_df(df):
    symbol_row = pd.DataFrame(nasdaq_scrapper.get_symbol_row(driver, symbols[i]), index=[i])
    df_updated = pd.concat([df, symbol_row], axis=0)
    return df_updated


for i in range(0, len(symbols)):
    print(symbols[i])
    try:
        nasdaq_companies = insert_new_symbol_in_df(nasdaq_companies)
    except Exception as e:
        print("error in " + symbols[i])
        logging.exception(e)
        errors.append(symbols[i])
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
nasdaq_companies.to_csv(get_path() + '\\execution_results\\' + timestamp + '_nasdaq.csv')
export_symbols_as_txt(errors, filename=timestamp + "_errors")
