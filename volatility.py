from datetime import datetime
import pandas as pd
import pytz

from zipline.api import order, order_target_percent, record, symbol, fetch_csv
from zipline import TradingAlgorithm

QUANDL_API_KEY = "vatGLfsDnNH6tAwvwzV6"
TRADING_DAY_MINIMUM = 20


def initialize(context):
    context.trading_day_count = 0
    context.vixData = pd.DataFrame(columns=["VIX Close"])

    for symbol in ['VIX', 'VXV']:
       #                 Date  VIX Open  VIX High  VIX Low  VIX Close
       # 0     2017-10-02      9.59     10.04     9.37       9.45
       fetch_csv('https://www.quandl.com/api/v3/datasets/CBOE/' + symbol + '.csv?api_key=' + QUANDL_API_KEY, symbol=symbol, date_column='Date')

    pass

def handle_data(context, data):
    # print context.get_datetime()

    # ========== Pre-Game Setup ==========
    context.vixData = context.vixData.append({"VIX Close": data.current('VIX', 'VIX Close')}, ignore_index=True)

    context.trading_day_count += 1
    if context.trading_day_count < TRADING_DAY_MINIMUM:
        return

    # ==========  Active Analysis ==========

    volatilityRatio = data.current('VIX', 'VIX Close') / data.current('VXV', 'CLOSE')
    print "VIX/VXV: %s" % volatilityRatio

    if volatilityRatio > 1:
        # order_target_percent(symbol('VXX'), 1.0)
        order_target_percent(symbol('XIV'), 0.0)
        record(VXX=data[symbol('VXX')].price)
        record(XIV=data[symbol('VXX')].price)
    else:
        order_target_percent(symbol('XIV'), 1.0)
        # order_target_percent(symbol('VXX'), 0.0)
        record(VXX=data[symbol('VXX')].price)
        record(XIV=data[symbol('VXX')].price)


    # order(symbol('VXX'), 15)
    # record(VXX=data[symbol('VXX')].price)

    # order(symbol('XIV'), 15)
    # record(XIV=data[symbol('XIV')].price)

    # order(symbol('ZIV'), 15)
    # record(XIV=data[symbol('ZIV')].price)

    # print data.current('VIX', 'VIX Close')
    # print data.history(symbol("XIV"), "close", 10, "1d")


def analyze(context, perf):
    print "\n=============== Analysis ==============="
    print "VIX mean: %s" % context.vixData['VIX Close'].mean()
    print "\n"
