import json
import robin_stocks as rh

def check_price(symbol):
    quote = rh.robinhood.get_crypto_quote_from_id(rh.robinhood.get_crypto_info(symbol)["id"])

    return quote["ask_price"]

# login - must be called before any other of the api accessing methods to grant access
def login():
    content = open('JSON_files/config.json').read()
    config = json.loads(content)

    rh.robinhood.authentication.login(config['username'], config['password'])

# buys crypto by amount in dollars
def buy_crypto(symbol, quantity):
    rh.robinhood.order_buy_crypto_by_quantity(symbol, quantity)
    print("{} units of {} purchased.\n".format(quantity, symbol))

# sells crypto by amount in dollars
def sell_crypto(symbol, quantity):
    rh.robinhood.order_sell_crypto_by_quantity(symbol, quantity)
    print("{} units of {} sold.\n".format(quantity, symbol))

# Checks how much of one type of crypto you own
def check_crypto_quantity(symbol):
    info = 0

    for i in rh.robinhood.crypto.get_crypto_positions():
        if i['currency']['code'] == symbol:
            info = i['quantity']
    return info













