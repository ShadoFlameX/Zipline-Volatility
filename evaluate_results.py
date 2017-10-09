import argparse
import locale
import matplotlib.pyplot as plt
import os.path
import pandas as pd
import sys

from pylab import plot

RESULTS_DIR = "results/"
RESULTS_PLOTS_DIR = RESULTS_DIR + "plots/"

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
    if not os.path.exists(RESULTS_PLOTS_DIR):
        os.makedirs(RESULTS_PLOTS_DIR)

    plots = [("Position Balance", dataFrame.ending_value), \
             ("Returns", dataFrame.returns), \
             ("PNL", dataFrame.pnl), \
             ("Alpha", dataFrame.alpha), \
             ("Total Balance", dataFrame.portfolio_value), \
             ("Cash Balance", dataFrame.ending_cash)]
    for index, plotItem in enumerate(plots):
        plt.figure(index)
        plotItem[1].plot(title=plotItem[0], secondary_y=True, grid=True, figsize=(12,6), alpha=0.75, color="blue")
        plt.savefig(RESULTS_PLOTS_DIR + 'plot%d.png' % index)

def printSummary(dataFrame):
    startingPortfolioValue = dataFrame.portfolio_value[0]
    totalProfit = dataFrame.pnl.sum()
    totalCapitalOutlay = -(dataFrame.capital_used.sum())
    totalReturn = totalProfit / totalCapitalOutlay if totalCapitalOutlay > 0 else 0   

    print "=========== Portfolio Summary ==========="
    print " Starting Value: %s" % locale.currency(startingPortfolioValue, grouping=True)
    print "                   "
    print " Captial Outlay: %s" % (locale.currency(totalCapitalOutlay, grouping=True))
    print "    Profit/Loss: %s (%s)" % (locale.currency(totalProfit, grouping=True), '{:.2%}'.format(totalReturn))
    print " Position Value: %s" % locale.currency(dataFrame.ending_value[-1], grouping=True)
    print "                   "
    print "Portfolio Total: %s" % locale.currency(dataFrame.portfolio_value[-1], grouping=True)
    print "========================================="

if __name__ == "__main__":
    main()