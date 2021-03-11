# Praos - Composed and Focused

## Introduction
Praos' goal is to help users backtest trade strategies using the binance api and backtrader. It's recommended that amateur traders backtest strategies for 6 - 12 months before trading.

### Capabilities
1. Data Gathering:
    - Crypto Data (1m, 1m, 15m, 1h, 1d)
    - Yahoo Data (1m, 1m, 15m, 1h, 1d) - *Not in current version*
2. Backtesting stratagies using technical indicators (using the binance api) such as:
    - Candlesticks
    - RSI
    - EMA, SMA
    - etc
3. Live Trading - *Not in current version*

### Prerequisites
Clone this repo to your computer using the following in your terminal:
```
git clone https://github.com/imaustinim/praos.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages.

```bash
pip install TA-Lib
pip install binance
pip install backtrader
pip install pandas
pip install Matplotlib
```
May have forget some others...

## Getting Started

### Setup
1. Create a [binance](https://accounts.binance.com/en/register) account (this will allow you to get trading data)
2. Create a .env file with your api address and secret api address (from your binance account) declared as the following:
```
API_KEY = <api_key>
API_SECRET = <secret_key>
```
3. Read the instructions on the GetData file and run after changing the time interval and binance_symbols parameters.
4. Create a strategy using the Strategies file.
5. Read the instruction on the BackTrader file and backtest strategy. (Should already be connected to the Strategies file)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Comments
This is my first project that I've actually created a readme for. I'm more than willing to help and would love to put a solid front end to this later.

## License
MIT