import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()

def check_valid_stock(ticker) -> bool:
    data = pdr.get_data_yahoo(ticker)
    check_existance = data.index.values.size
    if(check_existance == 0):
        return False
    else:
        return True
