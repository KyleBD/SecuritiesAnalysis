import unittest
import datetime as dt
import pandas as pd
import numpy as np
from get_tickers.portfolioMCSimulation import SimulatePortfolio, valueAtRisk, conditionalValueAtRisk

class TestSimulatePortfolio(unittest.TestCase):

    def setUp(self):
        self.stocks = ['TSLA', 'GME']
        self.startDate = dt.datetime(2023, 1, 1)
        self.endDate = dt.datetime(2023, 12, 31)

    def test_getData(self):
        portfolio = SimulatePortfolio(self.stocks, self.startDate, self.endDate)
        portfolio.getData()
        self.assertIsNotNone(portfolio.returns)
        self.assertIsNotNone(portfolio.meanReturns)
        self.assertIsNotNone(portfolio.covMatrix)

    def test_weightReturns(self):
        portfolio = SimulatePortfolio(self.stocks, self.startDate, self.endDate)
        portfolio.getData()
        portfolio.weightReturns()
        self.assertEqual(len(portfolio.weights), len(self.stocks))
        self.assertAlmostEqual(np.sum(portfolio.weights), 1.0)

    def test_monteCarloSimulation(self):
        portfolio = SimulatePortfolio(self.stocks, self.startDate, self.endDate)
        portfolio.getData()
        portfolio.weightReturns()
        portfolio.monteCarloSimulation()
        self.assertEqual(portfolio.simulatedReturns.shape, (self.simTimeFrame, self.MonteCarloSims))

    def test_valueAtRisk(self):
        returns = pd.Series(np.random.normal(0, 1, 1000))
        var = valueAtRisk(returns, alpha=5)
        self.assertIsInstance(var, float)

    def test_conditionalValueAtRisk(self):
        returns = pd.Series(np.random.normal(0, 1, 1000))
        cvar = conditionalValueAtRisk(returns, alpha=5)
        self.assertIsInstance(cvar, float)

if __name__ == '__main__':
    unittest.main()