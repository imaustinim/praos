import os, csv, talib, requests
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_cors import CORS, cross_origin
from binance.client import Client
from binance.enums import *


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key=b'lkafjl;sdkjfal;kjsd;l900980'

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
client = Client(API_KEY, API_SECRET)

@app.route('/')
def index():
    title = "Binance-Trader"

    info = client.get_account()
    balances = info['balances']

    exchangeInfo = client.get_exchange_info()
    symbols = exchangeInfo['symbols']  

    return render_template("index.html", title = title, balances = balances, symbols = symbols)

@app.route('/buy', methods=['POST'])
def buy():
    try:
        order = client.create_order(symbol=request.form['symbol'], side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=request.form['quantity'])
    except Exception as e:
        flash(e, "error")
    return redirect('/')

@app.route('/sell')
def sell():
    # order = client.create_oco_order(
    #     symbol='BNBBTC',
    #     side=SIDE_SELL,
    #     stopLimitTimeInForce=TIME_IN_FORCE_GTC,
    #     quantity=100,
    #     stopPrice='0.00001',
    #     price='0.00002')
    return "sell"

@app.route('/settings')
def settings():
    return "settings"

@app.route('/history')
def history():
    klines = client.get_historical_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_5MINUTE, start_str="1 Jan, 2021", end_str="2 Feb, 2021")
    processed_klines = []
    for kline in klines:
        candlestick = {
            "time": kline[0]/1000,
            "open": kline[1],
            "high": kline[2],
            "low": kline[3],
            "close": kline[4]
        }
        processed_klines.append(candlestick)
    return jsonify(processed_klines)