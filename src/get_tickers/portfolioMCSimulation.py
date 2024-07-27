import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
from scipy.stats import norm, t
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

#from getTickers import getSPFhundered

yf.pdr_override()

# ==============Define global variables============
MonteCarloSims = 1000
stocks = ['SU', 'CNQ']
#stocks = getSPFhundered()
simTimeFrame = 50
initialPortfolioVal = 10000 #Initial value in dollars.
#==================================================

#Chose stocks on the TSX
#stocks = [stock +'.TO' for stock in stockList]

class SimulatePortfolio:

    def __init__(self, stocks, start, end) -> None:
        self.stocks = stocks
        self.start = start
        self.end = end
        self.getData()
        self.weightReturns()
        self.monteCarloSimulation()
        self.portfolioPerformance()

    def getData(self):
        stockData = pdr.get_data_yahoo(self.stocks, start=self.start, end=self.end)
        stockData = stockData['Close']
        self.returns = stockData.pct_change()
        self.meanReturns = self.returns.mean()
        self.covMatrix = self.returns.cov()


    def portfolioPerformance(self):
        self.returnsPerformance = np.sum(self.meanReturns*self.weights)*simTimeFrame
        self.std = np.sqrt( np.dot(self.weights.T, np.dot(self.covMatrix, self.weights)) ) * np.sqrt(simTimeFrame)


    def weightReturns(self):
        self.returns = self.returns.dropna()
        weights = np.random.random(len(self.meanReturns))

        #Normalize the weights matrix
        weights /= np.sum(weights)
        self.weights = weights

    def monteCarloSimulation(self):
        #Creating the Monte Carlo Simulation

        #Define the returns matrix dimensions based on num of stocks and simulation time.
        meanReturnsMatrix = np.full(shape=(simTimeFrame, len(self.weights)), fill_value=self.meanReturns)
        meanReturnsMatrix = meanReturnsMatrix.T

        self.simulatedReturns = np.full(shape=(simTimeFrame, MonteCarloSims), fill_value=0.0)

        #Use formula for computing daily returns (Represented by the covarients matrix)
        for sim in range(0, MonteCarloSims):
            randVar = np.random.normal(size=(simTimeFrame, len(self.weights)))
            #Formula uses Cholesky Decomp to find the lower triangular, tying together the multiple variables.
            lowerTriangular = np.linalg.cholesky(self.covMatrix)
            dailyReturns = meanReturnsMatrix + np.inner(lowerTriangular, randVar)
            self.simulatedReturns[:,sim] = np.cumprod(np.inner(self.weights, dailyReturns.T)+1) * initialPortfolioVal



#Will return the maximum value at risk for a given alpha (bottom alpha percent)
def valueAtRisk(returns, alpha =5):
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected a data series input")

def conditionalValueAtRisk(returns, alpha =5):
    if isinstance(returns, pd.Series):
        bottomValueAtRisk = returns <= valueAtRisk(returns, alpha=alpha)
        return returns[bottomValueAtRisk].mean()
    else:
        raise TypeError("Expected a data series input")


def terminalOut(results):
    plt.plot(results)
    plt.xlabel('Time (Days)')
    plt.ylabel('Portfolio Value (CAD)')
    plt.title('Monte Carlo sim of given portfolio')
    plt.show()

    portfolioResults = pd.Series(results[-1,:])

    totalVaR = initialPortfolioVal -  valueAtRisk(portfolioResults, alpha=5)
    conditionalVaR = initialPortfolioVal - conditionalValueAtRisk(portfolioResults, alpha=5)
    avgReturn = results * initialPortfolioVal
    print(f"The average return of the portfolio is ${round(avgReturn,2)} \nThe VaR of the given portfolio is ${round(totalVaR,2)} \nThe CVaR of the portfolio is ${round(conditionalVaR, 2)}")


def main(args):
    endDate = dt.datetime.now()
    startDate = endDate - dt.timedelta(days=300)
    simulatedPortfolio = SimulatePortfolio(stocks=args, start=startDate, end=endDate)

    return simulatedPortfolio


if __name__ == '__main__':
    test = main(stocks)
    terminalOut(test.simulatedReturns)

