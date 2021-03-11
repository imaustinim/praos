import backtrader as bt
from pprint import pprint
import datetime


class Setup(bt.Strategy):
    params = {
        "pshort": 14,
        "plong": 180,
        "rsi_high": 75,
        "rsi_low": 25,
        "rsi_period": 14
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
                self.buyprice = order.executed.price
            elif order.issell():
                self.sellprice = order.executed.price
                if self.buyprice < self.sellprice:
                    self.wins += 1
                elif self.buyprice > self.sellprice:
                    self.losses += 1
                self.numTrades += 1
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
        print("%s || %s %s || win: %s || aProfit: $%s || tProfit: $%s || %s" % (self.numTrades, dt.isoformat(), tm,
                                                                                round(self.wins / self.numTrades, 2), round(self.profit/self.numTrades, 2), round(self.profit, 2), txt))

    def getDoji(self, idx, data=None):
        high = self.data.high[0]
        low = self.data.low[0]
        openn = self.data.open[0]
        close = self.data.close[0]
        doji = {
            "direction": None,
            "body": 0,
            "range": high - low,
            "top": 0,
            "bottom": 0,
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
            "open": haOpen,
            "high": max(haOpen, high, haClose),
            "low": min(haOpen, low, haClose),
            "close": haClose
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
            "open": haOpen,
            "high": max(haOpen, high, haClose),
            "low": min(haOpen, low, haClose),
            "close": haClose
        }
        heikinAshi["range"] = heikinAshi["high"] - heikinAshi["low"]
        heikinAshi["direction"] = heikinAshi["close"] - heikinAshi["open"]
        self.HeikinAshii[idx] = heikinAshi

    def getTrailingAverages(self, idx=int, period=int):
        o = self.data.open[0]
        h = self.data.high[0]
        l = self.data.low[0]
        c = self.data.close[0]

        if idx >= period:
            self.trailingData.pop(0)
        self.trailingData.append({
            "open": h,
            "high": l,
            "low": o,
            "close": c,
        })
        oa, ha, la, ca = 0, 0, 0, 0
        p = min(idx + 1, period)
        for i in range(p):
            oa += self.trailingData[i]["open"]
            ha += self.trailingData[i]["high"]
            la += self.trailingData[i]["low"]
            ca += self.trailingData[i]["close"]

        self.trailingAverages = {
            "open": oa / p,
            "high": ha / p,
            "low": la / p,
            "close": ca / p,
        }


class Setup_Binance(Setup):
    def __init__(self):
        super().__init__()


class Setup_Yahoo(Setup):
    def __init__(self):
        super().__init__()

    def log(self, txt, gain=None, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s || %s" % (dt.isoformat(), txt))


class Reversal(Setup_Binance):
    def __init__(self):
        super().__init__()
        self.ind_string = "SMA"

    def next(self):
        idx = self.idx

        data = self.data
        rsi = self.RSI
        buy = False
        sell = False

        if self.order:
            return

        if idx > 14:
            if not self.position:
                if rsi < 30 and data.close[0] > data.close[-1]:
                    buy = True

                if buy:
                    self.order = self.buy()
                    self.hold = 15

            elif self.position:
                if data.close[0] > self.buyprice * 1.01 and rsi > 50:
                    sell = True
                if data.close[0] < self.buyprice * .99:  # stop loss at 1%
                    sell = True

                if sell:
                    self.sell()
                    self.hold = 1

        self.idx += 1

# Copy template class "Reversal" to create strategy
