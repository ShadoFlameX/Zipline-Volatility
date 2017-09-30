import argparse
import pandas as pd

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument( "-p", "--plot", help="plot graphs", action="store_true")
	parser.add_argument('source_file', help='Pickle file to evaluate')
	args = parser.parse_args()

	print args.source_file

	if args.plot:
   		print "Plot a fancy graph"

if __name__ == "__main__":
    main()