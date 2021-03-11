import backtrader as bt
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import Strategies
import csv
import os
import plot


def data_processor(file_path):
    df = pd.read_csv(file_path)
    if "Date" in df:
        data = bt.feeds.YahooFinanceCSVData(
            dataname=file_path
        )
    else:
        data = bt.feeds.GenericCSVData(
            dataname=file_path,
            dtformat=2,
            query_timeframe="1Day",
            timeframe=bt.TimeFrame.Minutes,
        )
    return data


def clean_csv_data(file_path):
    df = pd.read_csv(file_path, header=1)
    row_end = df.loc[df.Id.str.contains("===")].index[0]
    df = df[:row_end]
    df = df[df.columns.drop(list(df.filter(regex='len')))]
    df = df[df.columns.drop(df.columns[1])]
    df = df[df.columns.drop(df.columns[8])]
    df = df.drop(["datetime.1", "Broker", "BuySell", "Trades - Net Profit/Loss"], axis=1)
    df.to_csv(file_path)


class File():
    def __init__(self, folder, dataType, timeInterval, symbol):
        self.folder = folder
        self.dataType = dataType
        self.timeInterval = timeInterval
        self.symbol = symbol

    def getFilePath(self):
        folder_path = "%s/%s/%s" % (self.folder, self.dataType, self.timeInterval)
        for f in os.listdir(folder_path):
            if self.symbol in f:
                print(f)
                return ("%s/%s" % (folder_path, f))


if __name__ == '__main__':
    file = File("chart_data", "crypto", "1h", "NANOUSDT")  # Choose the location of the folder (chart_data and crypto), candlestick time interval (1h), and ticker symbol (NANOUSDT)
    file_path = file.getFilePath()
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000)  # Set cash value
    cerebro.addsizer(bt.sizers.SizerFix, stake=10000)  # Set number of shares bought
    cerebro.broker.setcommission(commission=0.001)  # Set commission fee
    data = data_processor(file_path)

    cerebro.adddata(data)

    strat = Strategies.Crypto_Strategy
    cerebro.addstrategy(strat)
    start_value = cerebro.broker.getvalue()

    cerebro.run()
    print('Starting Portfolio Value: $%.0f' % start_value)
    end_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: $%.0f' % end_value)
    if end_value > start_value:
        change = float(end_value)/float(start_value) * 100
    else:
        change = float(end_value - start_value)/float(start_value) * 100
    print('Portfolio Value: %.2f%%' % change)
    plot.default_colors()
    cerebro.plot(
        style="candlestick",
        barup="#16A085",
        bardown="#E74C3C",
    )
