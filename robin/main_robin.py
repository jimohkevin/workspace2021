import robin_methods as rm
import time as t
import json
from datetime import datetime
from Order_obj import Order

'''
Project Notes:
    •There is margin of error in reporting price and the price actually traded at
    •Add in the percentage of datamax before it allows trades as a variable that can be edited with the JSON
    
    ** update to my update ** I realized that what's actually happening is the orders aren't executed to buy right away so the profits are actually much more messed up than I realized. 
    To combat this I think we have to trade on longer time frames and have fewer trade orders placed at once
    
    
    
    
'''


def return_trend(pricelist, timeframe):
    rates = []

    pos_tally = 0
    neg_tally = 0

    for index in range(len(pricelist)):
        if index != 0:
            rates.append((pricelist[index] - pricelist[index - 1]) / timeframe)

    avg = sum(rates) / len(rates)

    for rate in rates:
        if rate > 0:
            pos_tally += 1
        elif rate < 0:
            neg_tally += 1

    if pos_tally > neg_tally:
        return ["UPTREND", avg]
    elif neg_tally > pos_tally:
        return ["DOWNTREND", avg]
    else:
        return ["NO_CHANGE", avg]

    '''
    if avg > 0:
        return ["UPTREND", avg]
    elif avg < 0:
        return ["DOWNTREND", avg]

    else:
        return ["NO_CHANGE", avg]

    '''


def calculate_daily_profits():
    file = 'order_histories\order-history_{}.json'.format(datetime.now().strftime("%m-%d-%Y"))

    content = open(file).read()
    hist = json.loads(content)

    net_total = 0

    for each in hist:
        profit = hist[each]["Profit/Loss"]

        net_total += profit


    return {"Net_Total": net_total}


if __name__ == '__main__':
    print("hello from main")

    ##############

    # Setup
    if True:  # just did this to group all setup code together so they could be hidden

        rm.login()

        content = open('JSON_files/setup.json').read()
        setup = json.loads(content)

        symbol = setup["symbol"]

        prices = []

        start_time = t.time()
        start_time2 = t.time()

        trends = []
        trend_data_max = 6

        orders = []
        # ^^ Values not to be tweaked ^^

        # vv Values to be tweaked vv.
        datamax = setup["datamax"]
        timeframe = setup["timeframe"] / datamax

        order_max = setup["order_max"]
        amt = setup["quantity_per_order"]

        stop_loss_percentage = setup["stop_loss_percentage"]  # 0.2 percent losses max

        refresh_interval = 1


    # Continuous loop



    while True:
        if t.time() - start_time > timeframe:
            prices.append(float(rm.check_price(symbol)))

            if len(prices) > datamax:
                del prices[0]

            # resets time interval to continue loop
            start_time = t.time()

            try:
                entry_price = orders[0].entry_point
                record_price = orders[0].record_price
                stop_loss_price = orders[0].exit_point[0]

            except IndexError as e:
                entry_price = "N/A"
                record_price = "N/A"
                stop_loss_price = "N/A"

            try:
                trend_data = return_trend(prices, timeframe)
                print(
                    "Price is: {}. Rate of Change is: {}\nTrend is: {} (Total price list size is {})\nActive orders: {}. \nEntry Price is: {}. Record Price is: {}. Stop Loss Price is: {}\n".format(
                        prices[-1], trend_data[1], trend_data[0], len(prices), len(orders), entry_price, record_price,
                        stop_loss_price))

                trends.append(trend_data[0])

            except ZeroDivisionError as e:
                print(e)

            if len(trends) > trend_data_max:
                del trends[0]

            try:
                if trends[0] != "UPTREND" and trends[1] != "UPTREND" and trends[2] != "UPTREND" and trends[
                    -2] == "UPTREND" and trends[-1] == "UPTREND":
                    if len(prices) >= datamax * .9 and len(orders) < order_max:
                        orders.append(Order(symbol, quant, [prices[-1] * stop_loss_percentage, "null"], "sandbox"))

            except IndexError as e:
                print(e)

            try:
                for i in range(len(orders) - 1, -1, -1):
                    orders[i].update(prices[-1], setup["stop_loss_percentage"])

                    if orders[i].order_is_active == False:
                        del orders[i]

            except IndexError as e:
                print(e)

        if t.time() - start_time2 > refresh_interval:
            content = open('JSON_files/setup.json').read()
            setup = json.loads(content)

            symbol = setup["symbol"]

            datamax = setup["datamax"]
            timeframe = setup["timeframe"] / datamax

            order_max = setup["order_max"]
            quant = setup["quantity_per_order"]

            stop_loss_percentage = setup["stop_loss_percentage"]

            start_time2 = t.time()

