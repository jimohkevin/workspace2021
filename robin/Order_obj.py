import robin_methods as rm
from datetime import datetime
import json

class Order:
    ''' The 'Order' class stores info as well as purchases a determined amount of a specified cryptocurrency upon initialization.
        It also monitors and ammends sell-points and sells if the criteria is met.

        Finally, once sold, it logs the data in a file that's specific for the day
    '''
    def __init__(self, symbol, quantity, exit_point, order_type="normal"):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_point = float(rm.check_price(symbol))
        self.exit_point = exit_point
        self.order_is_active = True
        self.order_type = order_type
        self.record_price = self.entry_point

        rm.buy_crypto(self.symbol, self.quantity)

        self.purchasedatetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def update(self, latest_price, stop_loss):
        self.latest_price = latest_price

        if self.order_is_active:
            # "normal" sets it to a normal order type with an upper and lower bound & RSL (rolling stop loss)
            if self.order_type == "normal":
                if self.latest_price >= self.exit_point[1] or self.latest_price <= self.exit_point[0]:
                    rm.sell_crypto(self.symbol, self.quantity)

                    self.selldatetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    self.order_is_active = False

                    try:
                        file = 'order_histories\order-history_{}.json'.format(datetime.now().strftime("%m-%d-%Y"))

                        content = open(file).read()
                        hist = json.loads(content)

                        hist["order_number_{}".format(len(hist))] = self.orderInfo()

                        t = open(file, 'w')
                        t.write(json.dumps(hist, indent=2))
                        t.close()
                    except FileNotFoundError:
                        file = 'order_histories\order-history_{}.json'.format(datetime.now().strftime("%m-%d-%Y"))

                        f = open(file, 'w')
                        f.write("{}")
                        f.close()

                        content = open(file).read()
                        hist = json.loads(content)

                        hist["order_number_{}".format(len(hist))] = self.orderInfo()

                        t = open(file, 'w')
                        t.write(json.dumps(hist, indent=2))
                        t.close()

                self.rolling_stop_loss(self.latest_price, stop_loss)

            # "rolling_only" sets it to be rolling stop-loss only, not factoring in an upper bound
            if self.order_type == "rolling_only":
                if self.latest_price <= self.exit_point[0]:
                    rm.sell_crypto(self.symbol, self.quantity)

                    self.selldatetime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    self.order_is_active = False

                    try:
                        file = 'order_histories\order-history_{}.json'.format(datetime.now().strftime("%m-%d-%Y"))

                        content = open(file).read()
                        hist = json.loads(content)

                        hist["order_number_{}".format(len(hist))] = self.orderInfo()

                        t = open(file, 'w')
                        t.write(json.dumps(hist, indent=2))
                        t.close()
                    except FileNotFoundError:
                        file = 'order_histories\order-history_{}.json'.format(datetime.now().strftime("%m-%d-%Y"))

                        f = open(file, 'w')
                        f.write("{}")
                        f.close()

                        content = open(file).read()
                        hist = json.loads(content)

                        hist["order_number_{}".format(len(hist))] = self.orderInfo()

                        t = open(file, 'w')
                        t.write(json.dumps(hist, indent=2))
                        t.close()

                self.rolling_stop_loss(self.latest_price, stop_loss)

    def orderInfo(self):
        profit_info = self.profit_track()


        info = {"Symbol": self.symbol, "quantity": self.quantity, "Entry_Point": self.entry_point, "Exit_Point": self.exit_point, "Profit_ticker": profit_info[0], "Profit/Loss": profit_info[1]*self.quantity,"Date/Time_Purchased": self.purchasedatetime, "Date/Time_Sold": self.selldatetime}

        return info

    def rolling_stop_loss(self, latest_price, stop_loss):
        if latest_price > self.record_price:
            self.exit_point[0] = latest_price*stop_loss

            self.record_price = latest_price

    def profit_track(self):
        diff = self.exit_point[0] - self.entry_point

        ticker = "none"

        if diff > 0:
            ticker = "PROFITABLE"
        elif diff < 0:
            ticker = "NEGATIVE"
        else:
            ticker = "N/A"

        return [ticker, diff]