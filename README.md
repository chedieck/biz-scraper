# biz-scraper

Quantitative scraper for cryptocurrencies on the 4channel /biz/ board.
-
```
usage: biz.py [-h] [-n NUMBER] [-v] [-c]

/biz/ scraper.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        get n most mentioned tokens, default is 10
  -v, --verbose         print which assets are being ignored
  -c, --cached          used cached data
```
A simple scraper to count occurence of symbols that exist on CMC (Coinmarketcap) on /biz/. The listing `json` can be updated using a personal API key from CMC (which is not needed to perform the scraping on 4chan) using `update_cmc.py` with the API key written to a file named `api.key`.

The algorithm counts symbol occurence for each post: in other words, if somebody posts:

```
BUY BTC BUY BTC BTC BTC BUY BTC BTC BUY!11!!
```

The symbol `BUY` and the symbol `BTC` will only be counted once for this post.

Furthermore, as words like `BUY` and `THE` and `FOR` are usually not symbols (even though they exist on CMC), but regular words typed by someone with capslock turned on, the script starts with a `passlist` of "symbols" to be ignored. This can be manually edited, and the `-v` option can be used to see the relevance (CMC ranking) of the tokens being ignored.

`-c` Option to use cached data, in order to avoid rescraping the data.
