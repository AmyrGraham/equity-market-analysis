import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Download historical Apple stock data
apple = yf.download("AAPL", start="2021-01-01", end="2026-01-01")


# Plot Apple's closing stock price
plt.figure(figsize=(10, 5))
plt.plot(apple["Close"])
plt.title("Apple Stock Price (2021-2025)")
plt.xlabel("Date")
plt.ylabel("Closing Price ($)")
plt.show()

# Calculate daily percentage returns
apple["Daily Return"] = apple["Close"].pct_change() * 100

# Display the first five daily returns
print(apple["Daily Return"].head())

# Calculate annualised volatility
daily_volatility = apple["Daily Return"].std()
annualised_volatility = daily_volatility * (252 ** 0.5)

print("Daily Volatility:", daily_volatility)
print("Annualised Volatility:", annualised_volatility)
# Plot distribution of daily returns
plt.figure(figsize=(10, 5))
plt.hist(apple["Daily Return"].dropna(), bins=50)
plt.title("Distribution of Apple's Daily Returns")
plt.xlabel("Daily Return (%)")
plt.ylabel("Frequency")
plt.show()

# Summary statistics for daily returns
mean_return = apple["Daily Return"].mean()
volatility = apple["Daily Return"].std()
minimum_return = apple["Daily Return"].min()
maximum_return = apple["Daily Return"].max()

print("Mean Daily Return:", mean_return)
print("Daily Volatility:", volatility)
print("Minimum Daily Return:", minimum_return)
print("Maximum Daily Return:", maximum_return)

# Calculate moving averages
apple["50 Day MA"] = apple["Close"].rolling(window=50).mean()

apple["200 Day MA"] = apple["Close"].rolling(window=200).mean()

# Plot stock price and moving averages
plt.figure(figsize=(10, 5))

plt.plot(apple["Close"], label="Apple Closing Price")
plt.plot(apple["50 Day MA"], label="50 Day Moving Average")
plt.plot(apple["200 Day MA"], label="200 Day Moving Average")

plt.title("Apple Stock Price and Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()

plt.show()

# Identify whether the 50-day moving average is above the 200-day moving average
apple["Signal"] = 0

apple.loc[
    apple["50 Day MA"] > apple["200 Day MA"],
    "Signal"
] = 1

# Identify changes in the signal
apple["Position"] = apple["Signal"].diff()
crossovers = apple[
    apple["50 Day MA"].notna() &
    apple["200 Day MA"].notna()
]

crossovers = crossovers[crossovers["Position"] != 0]

print(crossovers[["Close", "50 Day MA", "200 Day MA", "Signal", "Position"]])

# Calculate strategy returns
apple["Strategy Return"] = apple["Daily Return"] * apple["Signal"]

# Calculate cumulative strategy returns
apple["Cumulative Strategy Return"] = (
    1 + apple["Strategy Return"] / 100
).cumprod()

# Calculate cumulative buy-and-hold returns
apple["Cumulative Buy and Hold"] = (
    1 + apple["Daily Return"] / 100
).cumprod()

# Calculate annualised strategy return (CAGR)
start_value = apple["Cumulative Strategy Return"].dropna().iloc[0]
end_value = apple["Cumulative Strategy Return"].dropna().iloc[-1]

years = (
    apple["Cumulative Strategy Return"].dropna().index[-1]
    - apple["Cumulative Strategy Return"].dropna().index[0]
).days / 365.25

annualised_return = (end_value / start_value) ** (1 / years) - 1

# Calculate annualised strategy volatility
strategy_volatility = (
    apple["Strategy Return"].dropna().std() / 100
) * np.sqrt(252)

# Calculate Sharpe ratio
risk_free_rate = 0

daily_strategy_return = apple["Strategy Return"].dropna() / 100

sharpe_ratio = (
    (daily_strategy_return.mean() - risk_free_rate / 252)
    / daily_strategy_return.std()
) * np.sqrt(252)

print("Annualised Strategy Return:", annualised_return)
print("Annualised Strategy Volatility:", strategy_volatility)
print("Sharpe Ratio:", sharpe_ratio)

# Calculate maximum drawdown
running_max = apple["Cumulative Strategy Return"].cummax()

drawdown = (
    apple["Cumulative Strategy Return"] - running_max
) / running_max

max_drawdown = drawdown.min()

print("Maximum Drawdown:", max_drawdown)

# Calculate buy-and-hold performance
buy_hold_start = apple["Cumulative Buy and Hold"].dropna().iloc[0]
buy_hold_end = apple["Cumulative Buy and Hold"].dropna().iloc[-1]

buy_hold_return = (
    (buy_hold_end / buy_hold_start) ** (1 / years)
) - 1

print("Annualised Buy-and-Hold Return:", buy_hold_return)

# Compare strategy with buy-and-hold
plt.figure(figsize=(10, 5))

plt.plot(
    apple["Cumulative Strategy Return"],
    label="Moving Average Strategy"
)

plt.plot(
    apple["Cumulative Buy and Hold"],
    label="Buy and Hold"
)

plt.title("Apple: Moving Average Strategy vs Buy and Hold")
plt.xlabel("Date")
plt.ylabel("Growth of $1")
plt.legend()

plt.show()

# Calculate buy-and-hold annualised volatility
buy_hold_volatility = (
    apple["Daily Return"].dropna().std() / 100
) * np.sqrt(252)

# Calculate buy-and-hold Sharpe ratio
daily_buy_hold_return = apple["Daily Return"].dropna() / 100

buy_hold_sharpe = (
    (daily_buy_hold_return.mean() - risk_free_rate / 252)
    / daily_buy_hold_return.std()
) * np.sqrt(252)
# Calculate buy-and-hold maximum drawdown
buy_hold_running_max = apple["Cumulative Buy and Hold"].cummax()

buy_hold_drawdown = (
    apple["Cumulative Buy and Hold"] - buy_hold_running_max
) / buy_hold_running_max

buy_hold_max_drawdown = buy_hold_drawdown.min()

print("Annualised Buy-and-Hold Return:", buy_hold_return)
print("Annualised Buy-and-Hold Volatility:", buy_hold_volatility)
print("Buy-and-Hold Sharpe Ratio:", buy_hold_sharpe)
print("Buy-and-Hold Maximum Drawdown:", buy_hold_max_drawdown)

# Calculate total cumulative returns
strategy_total_return = (
    apple["Cumulative Strategy Return"].dropna().iloc[-1] - 1
)

buy_hold_total_return = (
    apple["Cumulative Buy and Hold"].dropna().iloc[-1] - 1
)

print("Total Strategy Return:", strategy_total_return)
print("Total Buy-and-Hold Return:", buy_hold_total_return)

# Count crossover signals
number_of_signals = len(crossovers)

print("Number of Crossover Signals:", number_of_signals)