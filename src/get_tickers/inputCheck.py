import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()

def check_valid_stock(portfolio) -> bool:
    for stock in portfolio:
        data = pdr.get_data_yahoo(stock)
        check_existance = data.index.values.size
        if(check_existance == 0):
            return False

    return True

