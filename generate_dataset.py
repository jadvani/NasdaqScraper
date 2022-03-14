from scrape_symbols import get_driver_from_url, read_all_symbols_from_file, get_symbol_row, export_symbols_as_txt
import pandas as pd
from datetime import datetime

driver = get_driver_from_url("https://www.nasdaq.com/market-activity/stocks/screener")
# scrape all symbols (about 6 min)
# symbols = get_all_symbols(driver)
# export_symbols_as_txt(symbols)

# read symbols from file
symbols = read_all_symbols_from_file('symbols.txt')

# create dataset with the first 1000 rows
symbols_1000 = symbols[1000:1500]
nasdaq_companies = pd.DataFrame()
errors = []


# about 3 secs per symbol
def insert_new_symbol_in_df(df):
    symbol_row = pd.DataFrame(get_symbol_row(driver, symbols_1000[i]), index=[i])
    df_updated = pd.concat([df, symbol_row], axis=0)
    return df_updated


for i in range(0, len(symbols_1000)):
    print(symbols_1000[i])
    try:
        nasdaq_companies = insert_new_symbol_in_df(nasdaq_companies)
    except:
        print("error in " + symbols_1000[i])
        errors.append(symbols_1000[i])
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
nasdaq_companies.to_csv(timestamp + '_nasdaq.csv')
export_symbols_as_txt(errors, filename=timestamp + "_errors")
