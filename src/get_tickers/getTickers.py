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


def getData(stocks, start, end):
    stockData = pdr.get_data_yahoo(stocks, start=start, end=end)
    stockData = stockData['Close']
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return returns, meanReturns, covMatrix

# Portfolio Performance
def portfolioPerformance(weights, meanReturns, covMatrix, Time):
    returns = np.sum(meanReturns*weights)*Time
    std = np.sqrt( np.dot(weights.T, np.dot(covMatrix, weights)) ) * np.sqrt(Time)
    return returns, std


endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=300)

returns, meanReturns, covMatrix = getData(stocks, start=startDate, end=endDate)
returns = returns.dropna()
weights = np.random.random(len(meanReturns))

#Normalize the weights matrix
weights /= np.sum(weights)

#Creating the Monte Carlo Simulation

#Define the returns matrix dimensions based on num of stocks and simulation time.
meanReturnsMatrix = np.full(shape=(simTimeFrame, len(weights)), fill_value=meanReturns)
meanReturnsMatrix = meanReturnsMatrix.T

simulatedReturns = np.full(shape=(simTimeFrame, MonteCarloSims), fill_value=0.0)

#Use formula for computing daily returns (Represented by the covarients matrix)
for sim in range(0, MonteCarloSims):
    randVar = np.random.normal(size=(simTimeFrame, len(weights)))
    #Formula uses Cholesky Decomp to find the lower triangular, tying together the multiple variables.
    lowerTriangular = np.linalg.cholesky(covMatrix)
    dailyReturns = meanReturnsMatrix + np.inner(lowerTriangular, randVar)
    simulatedReturns[:,sim] = np.cumprod(np.inner(weights, dailyReturns.T)+1) * initialPortfolioVal

plt.plot(simulatedReturns)
plt.xlabel('Time (Days)')
plt.ylabel('Portfolio Value (CAD)')
plt.title('Monte Carlo sim of given portfolio')
plt.show()