# Apple Equity Market Data Analysis

## Overview

This project analyses historical Apple (AAPL) equity data using Python and evaluates a 50/200-day moving-average crossover strategy against a buy-and-hold benchmark.

## Analysis

The project:

- Analyses Apple equity data from 2021–2025
- Calculates daily returns and annualised volatility
- Examines the distribution and summary statistics of daily returns
- Calculates 50-day and 200-day moving averages
- Identifies moving-average crossover signals
- Backtests a 50/200-day moving-average strategy
- Calculates annualised return, volatility, Sharpe ratio and maximum drawdown
- Compares the strategy against a buy-and-hold benchmark
- Visualises cumulative strategy and benchmark performance

## Results

| Metric | Moving-Average Strategy | Buy & Hold |
|---|---:|---:|
| Total Return | 12.90% | 115.81% |
| Annualised Return | 2.46% | 16.40% |
| Annualised Volatility | 18.68% | 27.86% |
| Sharpe Ratio | 0.224 | 0.693 |
| Maximum Drawdown | -27.19% | -33.36% |

The moving-average strategy generated 9 crossover signals during the analysis period.

The strategy reduced annualised volatility and maximum drawdown relative to buy-and-hold, but substantially underperformed the benchmark in terms of total and annualised return.

## Technologies

- Python
- NumPy
- pandas
- Matplotlib
- yfinance

## Disclaimer

This project is for educational purposes and does not constitute investment advice.
