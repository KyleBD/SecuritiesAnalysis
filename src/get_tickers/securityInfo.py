import yfinance
import requests
from bs4 import BeautifulSoup
from getTickers import getSPFhundered

class stockData:
    def __init__(self) -> None:
        pass
        
    def get_info(self, ticker):
        data = yfinance.Ticker(ticker)
        data = data.info
        self.param =  {
            "previousClose": data['previousClose'],
            "open": data['open'],
            "dayLow": data['dayLow'],
            "dayHigh": data['dayHigh'],
            "regularMarketPreviousClose": data['regularMarketPreviousClose'],
            "regularMarketOpen": data['regularMarketOpen'],
            "regularMarketDayLow": data['regularMarketDayLow'],
            "regularMarketDayHigh": data['regularMarketDayHigh'],
            "exDividendDate": data['exDividendDate'],
            "fiveYearAvgDividendYield": data['fiveYearAvgDividendYield'],
            "beta": data['beta'],
            "forwardPE": data['forwardPE'],
            "volume": data['volume'],
            "regularMarketVolume": data['regularMarketVolume'],
            "averageVolume": data['averageVolume'],
            "averageVolume10days": data['averageVolume10days'],
            "averageDailyVolume10Day": data['averageDailyVolume10Day'],
            "bid": data['bid'],
            "ask": data['ask'],
            "bidSize": data['bidSize'],
            "askSize": data['askSize'],
            "marketCap": data['marketCap'],
            "fiftyTwoWeekLow": data['fiftyTwoWeekLow'],
            "fiftyTwoWeekHigh": data['fiftyTwoWeekHigh'],
            "priceToSalesTrailing12Months": data['priceToSalesTrailing12Months'],
            "fiftyDayAverage": data['fiftyDayAverage'],
            "twoHundredDayAverage": data['twoHundredDayAverage'],
            "currency": data['currency'],
            "enterpriseValue": data['enterpriseValue'],
            "profitMargins": data['profitMargins'],
            "floatShares": data['floatShares'],
            "sharesOutstanding": data['sharesOutstanding'],
            "sharesShort": data['sharesShort'],
            "sharesShortPriorMonth": data['sharesShortPriorMonth'],
            "sharesShortPreviousMonthDate": data['sharesShortPreviousMonthDate'],
            "dateShortInterest": data['dateShortInterest'],
            "sharesPercentSharesOut": data['sharesPercentSharesOut'],
            "heldPercentInsiders": data['heldPercentInsiders'],
            "heldPercentInstitutions": data['heldPercentInstitutions'],
            "shortRatio": data['shortRatio'],
            "shortPercentOfFloat": data['shortPercentOfFloat'],
            "impliedSharesOutstanding": data['impliedSharesOutstanding'],
            "bookValue": data['bookValue'],
            "priceToBook": data['priceToBook'],
            "lastFiscalYearEnd": data['lastFiscalYearEnd'],
            "nextFiscalYearEnd": data['nextFiscalYearEnd'],
            "mostRecentQuarter": data['mostRecentQuarter'],
            "netIncomeToCommon": data['netIncomeToCommon'],
            "trailingEps": data['trailingEps'],
            "forwardEps": data['forwardEps'],
            "pegRatio": data['pegRatio'],
            "lastSplitFactor": data['lastSplitFactor'],
            "lastSplitDate": data['lastSplitDate'],
            "enterpriseToRevenue": data['enterpriseToRevenue'],
            "enterpriseToEbitda": data['enterpriseToEbitda'],
            "52WeekChange": data['52WeekChange'],
            "SandP52WeekChange": data['SandP52WeekChange'],
            "lastDividendValue": data['lastDividendValue'],
            "lastDividendDate": data['lastDividendDate'],
            "exchange": data['exchange'],
            "currentPrice": data['currentPrice'],
            "targetHighPrice": data['targetHighPrice'],
            "targetLowPrice": data['targetLowPrice'],
            "targetMeanPrice": data['targetMeanPrice'],
            "targetMedianPrice": data['targetMedianPrice'],
            "recommendationMean": data['recommendationMean'],
            "recommendationKey": data['recommendationKey'],
            "numberOfAnalystOpinions": data['numberOfAnalystOpinions'],
            "totalCash": data['totalCash'],
            "totalCashPerShare": data['totalCashPerShare'],
            "ebitda": data['ebitda'],
            "totalDebt": data['totalDebt'],
            "quickRatio": data['quickRatio'],
            "currentRatio": data['currentRatio'],
            "totalRevenue": data['totalRevenue'],
            "debtToEquity": data['debtToEquity'],
            "revenuePerShare": data['revenuePerShare'],
            "returnOnAssets": data['returnOnAssets'],
            "returnOnEquity": data['returnOnEquity'],
            "freeCashflow": data['freeCashflow'],
            "operatingCashflow": data['operatingCashflow'],
            "revenueGrowth": data['revenueGrowth'],
            "grossMargins": data['grossMargins'],
            "ebitdaMargins": data['ebitdaMargins'],
            "operatingMargins": data['operatingMargins'],
            "financialCurrency": data['financialCurrency'],
            "trailingPegRatio": data['trailingPegRatio']
        }

def tsxSecurities():
    securitiesList = [];

    url = "https://stockanalysis.com/list/toronto-stock-exchange/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    table = table.find_all('a', href=lambda href: href and '/quote/tsx/' in href)
    for link in table:
        securitiesList.append(link.text.strip())

    return securitiesList