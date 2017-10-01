from datetime import datetime
import pytz

from zipline.api import order, record, symbol
from zipline import TradingAlgorithm


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('XIV'), 15)
    record(XIV=data[symbol('XIV')].price)