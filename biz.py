#!/bin/python3

from bs4 import BeautifulSoup
import requests
import json
import html
from string import punctuation
import argparse
import threading


# It's not very pythonic to have functions
# modyfing global arguments and returing None.
# However, I decided to structure the following
# code this way; for I figured it would make it
# more readable.

################################################################
# global variables:
COUNTING_DICT = {}
CLEAR_TRANS = str.maketrans(punctuation, ' ' * len(punctuation))
# shitcoins named after common capsed words that shall
# not be counted.
passlist = {
            'A',
            'IT',
            'THE',
            'YOU',
            'SENT',
            'LOL',
            'BUY',
            'FOR',
            'GET',
            'ME',
            'UP',
            'GO',
            }
# the most popular of those coins, at the time I am writing this,
# is FOR, at position 296 in CMC.
#################################################################


def passlist_info(cmc_json):
    for symb in passlist:
        print(f"{symb:<7} ranked {cmc_json[symb]['cmc_rank']:<4} ignored...")


def init_dict(cmc_json):
    for symb in cmc_json.keys():
        COUNTING_DICT[symb] = 0


def count_word(word):
    clean_word = word.translate(CLEAR_TRANS).strip()
    if clean_word in COUNTING_DICT and clean_word not in passlist:
        COUNTING_DICT[clean_word] += 1


def parse_string(_string):
    clear_string = _string.translate(CLEAR_TRANS)
    # to avoids spam/repetition
    unique_words = list(set(clear_string.split()))
    for word in unique_words:
        count_word(word)


def scrap_thread(thread_id):
    thread_url = 'https://boards.4channel.org/biz/thread/' + thread_id
    page = requests.get(thread_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    raw_posts = soup.findAll('blockquote', attrs={'class': 'postMessage'})[1:]
    for raw_post in raw_posts:
        post = html.unescape(raw_post.get_text(' '))
        parse_string(post)


def scrap_all():
    # load url and BS it
    catalog_url = 'https://boards.4channel.org/biz/catalog'
    page = requests.get(catalog_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get start of catalog json
    js_catalog = soup.findAll('script')[2]
    js_text = js_catalog.contents[0]
    catalog_var_start_id = js_text.find('catalog')
    catalog_var_trailing_noise = js_text[catalog_var_start_id:]

    # get end of catalog json
    catalog_var_end_id = catalog_var_trailing_noise.find('};var')
    catalog_var = catalog_var_trailing_noise[:catalog_var_end_id] + '}'
    catalog_json_str = catalog_var.split('=', 1)[1].lstrip()

    catalog_json = json.loads(catalog_json_str)

    # parse json
    threads = catalog_json['threads']
    process_threads = []
    for thread_id, content in threads.items():
        sub = html.unescape(content['sub'])
        teaser = html.unescape(content['teaser'])
        parse_string(teaser + ' ' + sub)
        process_threads.append(threading.Thread(target=scrap_thread,
                                                args=(thread_id,)))

    # run scraping threads
    print('sending requests...')
    for t in process_threads:
        t.start()
    print('waiting for responses...')
    for t in process_threads:
        t.join()
    print('saving on cache...')
    with open('.cache/counting_dict.json', 'w') as f:
        json.dump(COUNTING_DICT, f)
    print('done.')


def show_trend(args, D=COUNTING_DICT):
    n = args.number
    cached = args.cached
    if cached:
        print('using cache...')
        with open('.cache/counting_dict.json', 'r') as f:
            D = json.load(f)

    # show n most cited assets
    sorted_items = sorted(D.items(), key=lambda x: x[1], reverse=1)
    for i, (k, v) in enumerate(sorted_items):
        if i >= n:
            return
        print(f"{k + ' ':-<20} {v}")


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(description="/biz/ scraper.")
    parser.add_argument('-n', '--number', type=int,
                        help='get n most mentioned tokens, default is 10')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print which assets are being ignored')

    parser.add_argument('-c', '--cached', action='store_true',
                        help='used cached data')
    args = parser.parse_args()

    # run scraper or not, if cached
    if args.number is None:
        args.number = 10
    if not args.cached:
        # load json
        with open('cmc_by_symbol.json', 'r') as f:
            cmc_json = json.load(f)
        if args.verbose:  # print passlist info
            passlist_info(cmc_json)
        init_dict(cmc_json)
        # run scraping
        scrap_all()
    
    # show results
    show_trend(args)
