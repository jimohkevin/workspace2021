import json
import robin_stocks as rh

'''
Program notes:

•have the program update the stoploss percentage to be reduced by a percentage of profit ie: if the profit went up 2%, we can afford another 1% drop.
•Update the trend tracking.
'''

def check_price(symbol):
    quote = rh.robinhood.get_crypto_quote(symbol)

    return quote['mark_price']

# login - must be called before any other of the api accessing methods to grant access
def login():
    content = open('JSON_files/config.json').read()
    config = json.loads(content)

    rh.robinhood.authentication.login(config['username'], config['password'])

# buys crypto by quantity
def buy_crypto(symbol, quantity):
    rh.robinhood.order_buy_crypto_by_quantity(symbol, quantity)
    print("{} unit(s) purchased.".format(quantity))

# sells crypto by quantity
def sell_crypto(symbol, quantity):
    rh.robinhood.order_sell_crypto_by_quantity(symbol, quantity)
    print("{} unit(s) sold.".format(quantity))

# Checks how much of one type of crypto you own
def check_crypto_quantity(symbol):
    info = 0

    for i in rh.robinhood.crypto.get_crypto_positions():
        if i['currency']['code'] == symbol:
            info = i['quantity']
    return info