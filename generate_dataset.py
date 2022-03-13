from scrape_symbols import get_driver_from_url, get_all_symbols
import pandas as pd



driver = get_driver_from_url("https://www.nasdaq.com/market-activity/stocks/screener")
symbols = get_all_symbols(driver)

nasdaq_companies = pd.DataFrame({'symbol': symbols})
