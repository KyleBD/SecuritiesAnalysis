# Securities Analysis
The goal of the project is to create a backend using Flask that will write to a React front end. On the back end there will be calculations in a Monte Carlo simulation for a selected portoflio of securities. As well as the ability to list current stocks on the TSX ranked by certain metrics including: EPS, P/E, PEG, among others.

## Monte Carlo Simulation
Why use the Monte Carlo simulation? The simple answer is that the market does not have a determanistic solution. To account for this a MC simulation allows for the introduction of a random variable in a given range to make up for those uncertainties. The method of calculation that I chose to use was variance-covarience, in which I calculated the covarience of the mean returns over my desired time interval. I then am able to use the Cholesky Decomposition to introduce correlation into my simulation.

## VaR and CVaR
Gives a value for the value at risk over a chosen confidence interval. In the case of my testing I have set it at a 5% confidence interval to get the worst 5% of cases returned as the VaR. Then to find my CVaR i take all of the values that are bellow the VaR that was calculated.

## Current Work
- Creating the front end using React
- Deloping and backtesting formulas that can be used to find undervalued stocks on the TSX

## Future Plans
- Develop and backtest an options pricing model
- Develop a model that uses Fourier Series to create an aproximation of common trends and test the efficacy of a purely chart based method.
