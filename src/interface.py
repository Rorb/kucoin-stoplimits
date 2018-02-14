import apis

'''
        This file serves as an abstraction-layer between bots and APIs, so that the bots may be reused with
    different underlying APIs (e.g., for another exchange). I use the same bot-layer on every exchange and only
    change the way APIs are called behind the interface in order to maximize modularity.

'''

## API Interfacing
# Get the current price for a stock symbol
def getPrice(symbol):
    tickInfo = apis.getTick(symbol).call()
    price = tickInfo['lastDealPrice']
    return price

# Initiate a buy order
def buy(symbol, price, amount):
    return apis.transact('BUY', symbol, price, amount).call()

# Initiate a sell order
def sell(symbol, price, amount):
    return apis.transact('SELL', symbol, price, amount).call()
