import pandas as pd
import matplotlib.pyplot as plt
import argparse

DF = pd.read_csv('to_analyze.csv')


def plotcoin(symbol):
    coin = DF[symbol]
    coin.plot()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Plot symbol mentions.")
    parser.add_argument("-s", "--symbol", type=str, help="symbol to plot")
    args = parser.parse_args()
    plotcoin(args.symbol)
