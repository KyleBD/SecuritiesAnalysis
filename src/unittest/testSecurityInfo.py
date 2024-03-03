import unittest
from unittest.mock import patch, MagicMock
from get_tickers.securityInfo import stockData, tsxSecurities

class TestStockData(unittest.TestCase):
    
    @patch('yfinance.Ticker')
    def test_get_info(self, mock_ticker):
        mock_data = {
            'previousClose': 100,
            'open': 105,
        }
        mock_ticker.return_value.info = mock_data
        
        stock = stockData()
        

        stock.get_info('AAPL')

        self.assertEqual(stock.param['previousClose'], 100)
        self.assertEqual(stock.param['open'], 105)
        
    @patch('requests.get')
    @patch('bs4.BeautifulSoup')
    def test_tsxSecurities(self, mock_soup, mock_requests):
        mock_response = MagicMock()
        mock_response.text = '<table><a href="/quote/tsx/AAPL">AAPL</a><a href="/quote/tsx/GOOG">GOOG</a></table>'
        mock_requests.return_value = mock_response
        
        mock_table = MagicMock()
        mock_table.find_all.return_value = [MagicMock(text="AAPL"), MagicMock(text="GOOG")]
        mock_soup.return_value.find.return_value = mock_table

        result = tsxSecurities()
        
        self.assertEqual(result, ['AAPL', 'GOOG'])

if __name__ == '__main__':
    unittest.main()
