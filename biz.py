from bs4 import BeautifulSoup
import requests
import json
import html
from string import punctuation
from tqdm import tqdm

# global variables:
COUNTING_DICT = {}
CLEAR_TRANS = str.maketrans(punctuation, ' ' * len(punctuation))
passlist = {
            'A',
            'AM',
            'ALL',
            'AND',
            'FUCKING',
            'ARE',
            'ANON',
            'BUY',
            'DO',
            'DOING',
            'END',
            'EVERY',
            'EOY',
            'FOR',
            'FUCK',
            'FUCKING',
            'GET',
            'GOING',
            'MY',
            'MAKE',
            'NOW',
            'NOT',
            'ME',
            'I',
            'IN',
            'IS',
            'IT',
            'JUST',
            'OF',
            'SELL',
            'SHOULD',
            'TO',
            'THE',
            'THIS',
            'UK',
            'UP',
            'US',
            'YOU',
            'WILL',
            'WHAT',
            }


def count_word(word, seen_words, D=COUNTING_DICT):
    clean_word = word.translate(CLEAR_TRANS).strip()
    if clean_word.isupper() and clean_word not in seen_words.union(passlist):
        if clean_word in D.keys():
            D[clean_word] += 1
        else:
            D[clean_word] = 1
        seen_words.add(clean_word)
    return seen_words


def parse_string(_string, D=COUNTING_DICT):
    seen_words = set()  # avoids spam/repetition
    for word in _string.split():
        seen_words = count_word(word, seen_words)


def scrap_thread(thread_id, D=COUNTING_DICT):
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
    for thread_id, content in tqdm(threads.items()):
        sub = html.unescape(content['sub'])
        teaser = html.unescape(content['teaser'])
        print (f"At thread {thread_id}, sub: {sub}")
        parse_string(teaser + ' ' + sub)  # ignore repeated content
        scrap_thread(thread_id)


def show_trend(n=10):
    # show n most cited assets
    sorted_items = sorted(COUNTING_DICT.items(), key=lambda x: x[1], reverse=1)
    for i, (k, v) in enumerate(sorted_items):
        if i >= n:
            return
        print(f"{k}: {v}")







