import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# Download historical Apple stock data
apple = yf.download("AAPL", start="2020-01-01", end="2026-01-01")


# Plot Apple's closing stock price
plt.figure(figsize=(10, 5))
plt.plot(apple["Close"])
plt.title("Apple Stock Price (2020-2025)")
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

print(crossovers[["Close", "50 Day MA", "200 Day MA", "Signal", "Position"]])
