import argparse
import locale
import matplotlib.pyplot as plt
import os.path
import pandas as pd
import sys

from pylab import plot

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('source_file', help='Pickle file to evaluate')
	parser.add_argument( "-p", "--plot", help="plot graphs", action="store_true")
	args = parser.parse_args()

	if not os.path.isfile(args.source_file):
		sys.exit("Invalid source file: " + args.source_file)

	locale.setlocale( locale.LC_ALL, '' )

# Zipline columns:
# Index([u'AAPL','algo_volatility','algorithm_period_return','alpha',
#        u'benchmark_period_return','benchmark_volatility','beta',
#        u'capital_used','ending_cash','ending_exposure','ending_value',
#        u'excess_return','gross_leverage','long_exposure','long_value',
#        u'longs_count','max_drawdown','max_leverage','net_leverage',
#        u'orders','period_close','period_label','period_open','pnl',
#        u'portfolio_value','positions','returns','sharpe',
#        u'short_exposure','short_value','shorts_count','sortino',
#        u'starting_cash','starting_exposure','starting_value',
#        u'trading_days','transactions','treasury_period_return'],

	dataFrame = pd.read_pickle(args.source_file)

	printSummary(dataFrame)

	if args.plot:
   		plotData(dataFrame)

def plotData(dataFrame):
	plt.figure(1)
	plt.subplot(221)
	dataFrame.ending_value.plot(title="Position Balance", secondary_y=True, grid=True, figsize=(12,6), alpha=0.75, color="blue")
	plt.subplot(222)
	dataFrame.portfolio_value.plot(title="Total Balance", secondary_y=True, grid=True, figsize=(12,6), alpha=0.75, color="blue")
	plt.subplot(223)
	dataFrame.ending_cash.plot(title="Cash Balance", secondary_y=True, grid=True, figsize=(12,6), alpha=0.75, color="blue")
	plt.savefig('plots.png')

def printSummary(dataFrame):
	print "================ Portfolio Summary ================"
	print "  Positions: %s" % locale.currency(dataFrame.ending_value[-1], grouping=True )
	print "       Cash: %s" % locale.currency(dataFrame.ending_cash[-1], grouping=True )
	print "Grand Total: %s" % locale.currency(dataFrame.portfolio_value[-1], grouping=True )
	print "==================================================="

if __name__ == "__main__":
    main()