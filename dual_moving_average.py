from datetime import datetime
import pytz

from zipline.api import order, record, symbol, fetch_csv
from zipline import TradingAlgorithm

QUANDL_API_KEY = "vatGLfsDnNH6tAwvwzV6"

def initialize(context):
    #                 Date  VIX Open  VIX High  VIX Low  VIX Close
    # 0     2017-10-02      9.59     10.04     9.37       9.45
    fetch_csv('https://www.quandl.com/api/v3/datasets/CBOE/VIX.csv?api_key=' + QUANDL_API_KEY, symbol='VIX', date_column='Date')
    pass

def handle_data(context, data):
    order(symbol('VXX'), 15)
    record(VXX=data[symbol('VXX')].price)

    order(symbol('XIV'), 15)
    record(XIV=data[symbol('XIV')].price)

    print data.current('VIX', 'VIX Close')