import os
import csv
import regex
import sys
import talib
from binance.client import Client
import datetime
import time
import pytz
import pandas as pd

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
client = Client(API_KEY, API_SECRET)
today = datetime.datetime.utcnow().date().strftime("%Y %m %d")


class Symbols():
    def __init__(self, interval=str):
        self.interval = interval
        self.folder = "chart_data/crypto/%s" % (self.interval)
        self.file_path = None
        self.symbols = []

    def getSymbols(self, filter=False, overwrite=False):
        self.file_path = "%s/-Binance Symbols %s.csv" % (self.folder, self.interval)

        if os.path.exists(self.file_path) and not overwrite:
            print("%s already exists" % (self.file_path))
            print("Process will run with existing file")
            print("Change overwrite variable to True if you want to overwrite")
            f = open(self.file_path, 'r', newline='')
            reader = csv.reader(f)
            for symbol in reader:
                self.symbols.append(symbol[0])

        else:
            f = open(self.file_path, 'w', newline='')
            writer = csv.writer(f)
            exchangeInfo = client.get_exchange_info()["symbols"]
            x = 0
            for i in range(0, len(exchangeInfo)):
                symbol = exchangeInfo[i]["symbol"]
                if filter:
                    if filter in symbol:
                        writer.writerow([symbol])
                        self.symbols.append(symbol)
                        print(symbol)
                        x += 1
                else:
                    writer.writerow([symbol])
                    self.symbols.append(symbol)
                    print(symbol)
                    x += 1
            f.close()
            print("%s/%s symbols added" % (x, len(exchangeInfo)))


class Data():
    def __init__(self, symbol, interval="1d", time="00:00:00", timezone="UTC+0000"):
        self.beginDate = "2000 01 01"
        self.endDate = today
        self.symbol = symbol
        self.interval = interval
        self.time = time
        self.timezone = timezone
        self.folder = "chart_data/crypto/%s" % (interval)
        self.file_path = ""
        self.klines = None

    def getData(self):
        file_name = "%s %s" % (self.symbol, self.interval.upper())
        files_list = os.listdir(self.folder)
        update = False

        for file_path in files_list:
            if file_name in file_path:
                update = True
                break

        if update:
            self.updateCryptoData(file_path)
        else:
            self.getCryptoData()

    def getCryptoData(self):
        klines = client.get_historical_klines(symbol=self.symbol, interval=self.interval, start_str=self.beginDate, end_str=self.endDate, limit=2500)
        self.beginDate = datetime.datetime.utcfromtimestamp(klines[0][0] / 1000).strftime("%Y %m %d")
        self.endDate = datetime.datetime.utcfromtimestamp(klines[-1][0] / 1000).strftime("%Y %m %d")
        self.file_path = "%s/%s %s %s - %s.csv" % (self.folder, self.symbol, self.interval.upper(), self.beginDate, self.endDate)
        f = open(self.file_path, 'w', newline='')
        writer = csv.writer(f, delimiter=',')
        for k in klines:
            k[0] = k[0] / 1000
            writer.writerow(k)
        f.close()
        print("%s created" % (self.file_path))

    def updateCryptoData(self, file_path):
        dates = regex.findall(r"\d{4} \d{2} \d{2}", file_path)
        self.file_path = "%s/%s" % (self.folder, file_path)
        if dates[1] != today:
            self.beginDate = dates[0]
            self.endDate = today
            klines = client.get_historical_klines(symbol=self.symbol, interval=self.interval, start_str=dates[1], end_str=today)
            f = open(self.file_path, 'a+', newline='')
            writer = csv.writer(f, delimiter=',')
            for k in klines[1:]:
                k[0] = k[0] / 1000
                writer.writerow(k)
            f.close()
            new_file_path = "%s/%s %s %s - %s.csv" % (self.folder, self.symbol, self.interval.upper(), self.beginDate, today)
            os.rename(self.file_path, new_file_path)
            self.file_path = new_file_path
            print("%s updated" % (self.file_path))
        else:
            print("%s already updated" % (self.file_path))


if __name__ == '__main__':
    time_intervals = ["15m", "1h", "1d"]  # Choose time intervals of data you want to get. Options are "1m", "5m", "15m", "30m", "1h", "1d", etc.
    for ti in time_intervals:
        binance_symbols = Symbols(ti)
        binance_symbols.getSymbols(overwrite=False)

        # 1. Uncomment below after running and getting binance_symbols. A file should be created in chart_data/crypto/<time interval>/ called -Binance Symbols.csv.
        # 2. In -Binance Symbols, remove any charts you don't want. Don't format
        # 3. Uncomment below and run. Warning: It takes a while, especially 1m and 5m so I would suggest working with 1d or 1h first.
        # 4. It will automatically update if you run the program.

        # sTime = time.time()
        # l = len(binance_symbols.symbols)
        # for i, symbol in enumerate(binance_symbols.symbols):
        #     eTime = datetime.timedelta(seconds=time.time()- sTime)
        #     print("%s/%s | %s | " % (i+1, l, str(eTime).split(".")[0]), end='')
        #     data = Data(symbol, ti)
        #     data.getData()
        #     data = None
