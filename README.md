# Securities Analysis
The goal of the project is to create a backend using Flask that will write to a React front end. On the back end there will be calculations in a Monte Carlo simulation for a selected portoflio of securities. As well as the ability to list current stocks on the TSX ranked by certain metrics including: EPS, P/E, PEG, among others.

## Monte Carlo Simulation
Why use the Monte Carlo simulation? The simple answer is that the market does not have a determanistic solution. To account for this a MC simulation allows for the introduction of a random variable in a given range to make up for those uncertainties. The method of calculation that I chose to use was variance-covarience, in which I calculated the covarience of the mean returns over my desired time interval. I then am able to use the Cholesky Decomposition to introduce correlation into my simulation.<br>
<img width="623" alt="Screen Shot 2024-02-22 at 2 06 42 PM" src="https://github.com/KyleBD/SecuritiesAnalysis/assets/114958251/75343536-f351-40b8-bc58-97a17b5c34cf"><br>
Figure 1: Simulated Returns from companies on the S&P 500 over a 100 day inveral using 1000 simulations.

## VaR and CVaR
Gives a value for the value at risk over a chosen confidence interval. In the case of my testing I have set it at a 5% confidence interval to get the worst 5% of cases returned as the VaR. Then to find my CVaR i take all of the values that are bellow the VaR that was calculated.<br>
<img width="377" alt="Screen Shot 2024-02-22 at 2 07 09 PM" src="https://github.com/KyleBD/SecuritiesAnalysis/assets/114958251/b6bf8c45-5f8f-4eb5-8649-c4ea0a88ffb1"><br>
Figure 2: Mean estimated returns from simulation in Fig. 1 as well as VaR and CVaR from same simulation.

## Current Work
- Creating the front end using React
- Deloping and backtesting formulas that can be used to find undervalued stocks on the TSX

## Future Plans
- Develop and backtest an options pricing model
- Develop a model that uses Fourier Series to create an aproximation of common trends and test the efficacy of a purely chart based method.
