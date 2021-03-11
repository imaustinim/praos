import backtrader as bt
from pprint import pprint
import datetime
#
#       [
#         1499040000000,      # Open time
#         "0.01634790",       # Open
#         "0.80000000",       # High
#         "0.01575800",       # Low
#         "0.01577100",       # Close
#         "148976.11427815",  # Volume
#         1499644799999,      # Close time
#         "2434.19055334",    # Quote asset volume
#         308,                # Number of trades
#         "1756.87402397",    # Taker buy base asset volume
#         "28.46694368",      # Taker buy quote asset volume
#         "17928899.62484339" # Can be ignored
#     ]
class Setup(bt.Strategy):
    params = {
        "pshort": 14,
        "plong" : 180,
        "rsi_high" : 75,
        "rsi_low" : 25,
        "rsi_period" : 14
    }
    
    def __init__(self):
        super().__init__()
        self.order = None
        self.buyprice = 0
        self.sellprice = 0
        self.idx = 0
        self.hold = 0
        self.top_tail = 0
        self.bottom_tail = 0 
        self.direction = 0
        self.numTrades = 1
        self.wins = 0
        self.losses = 0
        self.profit = 0
        self.EMA_long_set = 0
        self.SMA_long = bt.ind.SMA(self.datas[0], period=self.params.plong)
        self.EMA_long = bt.ind.EMA(self.datas[0], period=self.params.plong)
        self.SMA_short = bt.ind.SMA(self.datas[0], period=self.params.pshort)
        self.EMA_short = bt.ind.EMA(self.datas[0], period=self.params.pshort)
        self.RSI = bt.ind.RSI_Safe(self.datas[0], period=self.params.rsi_period)

        self.doji = {}
        self.dojiAverage = {}
        self.trailingData = []
        self.trailingAverages = {}
        self.HeikinAshi = {}
        self.HeikinAshii = {}


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log("BUY ORDER FILLED: {}".format(order.executed.price))
                self.buyprice = order.executed.price
            elif order.issell():
                self.sellprice = order.executed.price
                if self.buyprice < self.sellprice:
                    self.wins += 1
                elif self.buyprice > self.sellprice:
                    self.losses += 1
                self.numTrades += 1
                # self.log("SELL ORDER FILLED: {}".format(order.executed.price))
        self.notify_trade
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.profit += trade.pnlcomm
        self.log("GROSS: %.2f, NET: %.2f" % (trade.pnl, trade.pnlcomm))


    def log(self, txt, gain=None, dt=None, tm=None):
        dt = dt or self.datas[0].datetime.date(0)
        tm = tm or self.datas[0].datetime.time(0)
        print("%s || %s %s || win: %s || aProfit: $%s || tProfit: $%s || %s" % (self.numTrades, dt.isoformat(), tm, round(self.wins / self.numTrades,2), round(self.profit/self.numTrades,2), round(self.profit,2), txt))

    def getDoji(self, idx, data=None):
        high = self.data.high[0]
        low = self.data.low[0]
        openn = self.data.open[0]
        close = self.data.close[0]
        doji = {
            "direction" : None,
            "body" : 0,
            "range" : high - low,
            "top" : 0,
            "bottom" : 0,
        }
        if doji["range"] == 0:
            doji["direction"] = 0
            doji["body"] = 0
            doji["top"] = 0
            doji["bot"] = 0
        elif close > openn:
            # Direction = Up
            doji["direction"] = 1
            doji["body"] = close - openn
            doji["top"] = high - close
            doji["bot"] = openn - low
        elif close < openn:
            # Direction = Down
            doji["direction"] = -1
            doji["body"] = openn - close
            doji["top"] = high - openn
            doji["bot"] = close - low
        elif close == openn:
            # Direction = None
            doji["body"] = close - openn
            doji["top"] = high - close
            doji["bot"] = close - low
        self.doji[idx] = doji

    def getHeikinAshi(self, idx):
        high = self.data.high[0]
        low = self.data.low[0]
        openn = self.data.open[0]
        close = self.data.close[0]
        haOpen = (self.HeikinAshi[idx-1]["open"] + self.HeikinAshi[idx-1]["close"]) / 2 if idx > 0 else openn
        haClose = (high + low + openn + close) / 4
        heikinAshi = {
            "open" : haOpen,
            "high" : max(haOpen, high, haClose),
            "low" : min(haOpen, low, haClose),
            "close" : haClose
        }
        heikinAshi["range"] = heikinAshi["high"] - heikinAshi["low"]
        heikinAshi["direction"] = heikinAshi["close"] - heikinAshi["open"]
        self.HeikinAshi[idx] = heikinAshi

    def getHeikinAshii(self, idx):
        hashi = self.HeikinAshi
        high = hashi[idx]["high"]
        low = hashi[idx]["low"]
        openn = hashi[idx]["open"]
        close = hashi[idx]["close"]
        haOpen = (self.HeikinAshii[idx-1]["open"] + self.HeikinAshii[idx-1]["close"]) / 2 if idx > 0 else openn
        haClose = (high + low + openn + close) / 4
        heikinAshi = {
            "open" : haOpen,
            "high" : max(haOpen, high, haClose),
            "low" : min(haOpen, low, haClose),
            "close" : haClose
        }
        heikinAshi["range"] = heikinAshi["high"] - heikinAshi["low"]
        heikinAshi["direction"] = heikinAshi["close"] - heikinAshi["open"]
        self.HeikinAshii[idx] = heikinAshi


    # def getDojiAverage(self, idx=int, period=int):
    #     doji = self.doji[idx]
    #     if idx == 0:
    #         self.trailingDojis = doji
    #     if idx < period:
    #         dojis.append(doji)
    #         for key in self.trailingDojis:
    #             self.trailingDojis[key] = (self.trailingDojis[key] * idx + doji[key]) / (idx + 1)
    #         self.trailingDojis["period"] = idx
    #         return self.trailingDojis
    #     else:
    #         doji

        

    #         newAvg = {
    #             "direction" : (avg["direction"] * idx + doji["direction"])/(idx + 1)),
    #             "body" : (avg["body"] * idx + doji["body"])/(idx + 1),
    #             "range" : (avg["range"] * idx + doji["range"])/(idx + 1),
    #             "top" : 0,
    #             "bottom" : 0,
    #         }

    #     print(dojis)
    #     return dojis
        # doji = {
        #     "direction" : sum(),
        #     "body" : 0,
        #     "range" : high - low,
        #     "top" : 0,
        #     "bottom" : 0,
        #     "period" : min(period, idx)
        # }

        # averageDoji = {
            
        # }
        # for i in range(idx-period, idx, 1):
    
    def getTrailingAverages(self, idx=int, period=int):
        o = self.data.open[0]
        h = self.data.high[0]
        l = self.data.low[0]
        c = self.data.close[0]

        if idx >= period:
            self.trailingData.pop(0)
        self.trailingData.append({
            "open" : h,
            "high" : l,
            "low" : o,
            "close" : c,
        })
        oa, ha, la, ca = 0, 0, 0, 0
        p = min(idx + 1, period)
        for i in range(p):
            oa += self.trailingData[i]["open"]
            ha += self.trailingData[i]["high"]
            la += self.trailingData[i]["low"]
            ca += self.trailingData[i]["close"]

        self.trailingAverages = {
            "open" : oa / p,
            "high" : ha / p,
            "low" : la / p,
            "close" : ca / p,
        }
    
    # def getTrailingIndicators(self, idx=int, period=int)

class Setup_Binance(Setup):
    def __init__(self):
        super().__init__()

class Setup_Yahoo(Setup):
    def __init__(self):
        super().__init__()

    def log(self, txt, gain=None, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s || %s" % (dt.isoformat(), txt))

class Crypto_Strategy(Setup_Binance):
    def __init__(self):
        super().__init__()
        self.ind_string = "SMA"

    def next(self):
        idx = self.idx
        self.getHeikinAshi(idx)
        self.getDoji(idx)
        self.getTrailingAverages(idx, 14)
        # self.getTrailingIndicators(idx, 14)

        data = self.data
        tAvg = self.trailingAverages
        hashi = self.HeikinAshi
        # hashii = self.HeikinAshii
        doji = self.doji
        # print(hashi[idx]["direction"])
        # print(data.open[0], data.high[0], data.low[0], data.close[0])
        # print(hashi[idx]["open"], hashi[idx]["high"], hashi[idx]["low"], hashi[idx]["close"])

        # dojiAvg = self.getDojiAverage(idx, 14)
        # dateTime = self.datetime.datetime(ago=0)
        # pprint(self.doji[idx])
        # print(data.close[-1], data.open[-1], data.high[-1], data.low[-1])

        rsi = self.RSI
        buy = False
        sell = False

        # Use heikin ashi for reversals
        # Breakouts 
        if self.order:
            return

        if self.hold > 0:
            self.hold -= 1
            return

        if idx > 30:
            d0 = hashi[idx]["direction"]
            d1 = hashi[idx-1]["direction"]
            if not self.position:
                if d0 > 0 and d1 > 0 and rsi > 50:
                    # if d0 / d1 > 1:
                    buy = True
                    
                    # if doji["bot"] > doji["body"] + doji["top"] * 2:
                    buy = True

                if buy:
                    # self.log("BUY ORDER OPEN: {}".format(d.close[0]))
                    self.order = self.buy()
                    self.hold = 15

            elif self.position:
                if (d0 < 0 and d1 < 0) and rsi > 70:
                    if d0 / d1 > 1:
                        sell = True
                if data.close[0] > self.buyprice * 1.10 or rsi > 70:
                    sell = True
                if data.close[0] < self.buyprice * .95 and rsi > 50:
                    sell = True
                    
                if sell:
                    # self.log("SELL ORDER OPEN: {}".format(d.close[0]))
                    self.sell()
                    self.hold = 1

        self.idx += 1
