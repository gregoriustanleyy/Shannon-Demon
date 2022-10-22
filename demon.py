from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
#Reference: geeksforgeeks.com
#https://www.richmondquant.com/news/2021/9/21/shannons-demon-amp-how-portfolio-returns-can-be-created-out-of-thin-air
#TODO: https://www.shufflup.org/volatility.php

asset = input("Inser the asset: ")
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)

data = yf.download(asset, start = start_date, end = end_date)

data = data["Close"].to_frame()
data = data.reset_index()


#Initialize
portfolio = pd.DataFrame(columns=["Date", "Price", "Lot", "Stock", "Cash", "Total"])
portfolio_rebalance = portfolio.copy()
portfolio_unbalance = portfolio.copy()
initial_cap = 1000.0
initial_alloc = {"Date": data["Date"].iloc[0], 
                "Price": data["Close"].iloc[0], 
                "Lot": (initial_cap/2) / data["Close"].iloc[0], 
                "Stock": initial_cap/2, 
                "Cash": initial_cap/2, 
                "Total": initial_cap}
portfolio_rebalance = portfolio_rebalance.append(initial_alloc, ignore_index=True)
portfolio_unbalance = portfolio_unbalance.append(initial_alloc, ignore_index=True)

for i in range(1, len(data)):
    date = data["Date"].iloc[i]
    price = data["Close"].iloc[i]
    lot = portfolio_rebalance["Lot"].iloc[i-1]
    stock = price * portfolio_rebalance["Lot"].iloc[i-1]
    cash = portfolio_rebalance["Cash"].iloc[i-1]

    #TODO: BISA DI SMOOTH
    if stock/cash != 3.0: #unbalanced
        total = stock + cash
        lot = (total/2) / price
        stock = lot * price
        cash = total - stock

    temp = {"Date": date,
            "Price": price,
            "Lot": lot,
            "Stock": stock,
            "Cash": cash,
            "Total": total}
    portfolio_rebalance = portfolio_rebalance.append(temp, ignore_index=True)

for i in range(1, len(data)):
    date = data["Date"].iloc[i]
    price = data["Close"].iloc[i]
    lot = portfolio_unbalance["Lot"].iloc[i-1]
    stock = price * portfolio_unbalance["Lot"].iloc[i-1]
    cash = portfolio_unbalance["Cash"].iloc[i-1]
    total = stock + cash

    temp = {"Date": date,
            "Price": price,
            "Lot": lot,
            "Stock": stock,
            "Cash": cash,
            "Total": total}
    portfolio_unbalance = portfolio_unbalance.append(temp, ignore_index=True)
portfolio_unbalance

f1 = plt.figure(figsize = (20,10))
plt.title(asset + "from" + str(start_date) + "to" + str(end_date))
plt.plot(data['Close'], label = "Asset Price")
plt.legend()
plt.savefig("Asset Price.png")

f2 = plt.figure(figsize = (20,10))
plt.plot(portfolio_rebalance["Total"], label = "Rebalanced")
plt.plot(portfolio_unbalance["Total"], label = "Unbalanced")
plt.legend()
plt.savefig("Portfolio.png")

print("Initial Capital: $1000.0")
print("Portfolio Unbalanced: $" + str(round(portfolio_unbalance["Total"].iloc[-1], 2)))
print("Portfolio Rebalanced: $" + str(round(portfolio_rebalance["Total"].iloc[-1], 2)))