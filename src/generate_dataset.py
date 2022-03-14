from src.nasdaq_scrapper import NasdaqScrapper, get_path, read_all_symbols_from_file

# from src.nasdaq_scrapper import export_symbols_as_txt

nasdaq_scrapper = NasdaqScrapper()

# scrape all symbols (about 6 min)
# symbols = nasdaq_scrapper.get_all_symbols()
# export_symbols_as_txt(symbols)

# read symbols from file
symbols = read_all_symbols_from_file(get_path() + '\\execution_results\\symbols.txt')
# grab first 5 symbols as example (comment or modify this line as desired)
symbols = symbols[0:5]
# scrape symbol details and export as CSV with current timestamp
nasdaq_scrapper.scrape_details_from_symbols(symbols)
nasdaq_scrapper.driver.close()
