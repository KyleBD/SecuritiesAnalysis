import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
from scipy.stats import norm, t
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
yf.pdr_override()

# ==============Define global variables============
MonteCarloSims = 100
stockList = ['SU', 'T']
simTimeFrame = 100
initialPortfolioVal = 10000 #Initial value in dollars.
#==================================================

#Chose stocks on the TSX
stocks = [stock +'.TO' for stock in stockList]

class SimulatePortfolio:

    def __init__(self, stocks, start, end) -> None:
        self.stocks = stocks
        self.start = start
        self.end = end
        self.getData()
        self.weightReturns()
        self.monteCarloSimulation()

    def getData(self):
        stockData = pdr.get_data_yahoo(self.stocks, start=self.start, end=self.end)
        stockData = stockData['Close']
        self.returns = stockData.pct_change()
        self.meanReturns = self.returns.mean()
        self.covMatrix = self.returns.cov()

    '''
    def portfolioPerformance(self, weights, meanReturns, covMatrix, Time):
        self.returnsPerformance = np.sum(meanReturns*weights)*Time
        self.std = np.sqrt( np.dot(weights.T, np.dot(covMatrix, weights)) ) * np.sqrt(Time)
    '''


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




def main():
    endDate = dt.datetime.now()
    startDate = endDate - dt.timedelta(days=300)
    simulatedPortfolio = SimulatePortfolio(stocks=stocks, start=startDate, end=endDate)

    plt.plot(simulatedPortfolio.simulatedReturns)
    plt.xlabel('Time (Days)')
    plt.ylabel('Portfolio Value (CAD)')
    plt.title('Monte Carlo sim of given portfolio')
    plt.show()

    portfolioResults = pd.Series(simulatedPortfolio.simulatedReturns[-1,:])

    totalVaR = initialPortfolioVal -  valueAtRisk(portfolioResults, alpha=5)
    conditionalVaR = initialPortfolioVal - conditionalValueAtRisk(portfolioResults, alpha=5)

    print(f"The VaR of the given portfolio is ${round(totalVaR,2)} \nThe CVaR of the portfolio is ${round(conditionalVaR, 2)}")

if __name__ == '__main__':
    main()
