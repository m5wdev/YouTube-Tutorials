from urllib.request import urlopen, Request
from xml.etree import ElementTree
from time import sleep
import threading
import os
from datetime import datetime


def fetch_data_from_url(feed_url):
    http_request = Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(http_request) as response:
        if response.status == 200:
            return response.read().decode()

def feed_reader(feed_url):
    xml_data = ElementTree.fromstring(fetch_data_from_url(feed_url))
    print(f'Feed from: {feed_url}')
    for item in xml_data.iter('item'):
        el = {
            'title': item.find('title').text,
            'link': item.find('link').text,
            'pubdate': item.find('pubDate').text,
        }
        print(el)
    print('\n')


def clear_console():
    os.system('cls')


while True:
    print(f'Fetched at: {datetime.now()}')

    t1 = threading.Thread(target=feed_reader, args=('https://byxatab.com/rss.xml',))
    t2 = threading.Thread(target=feed_reader, args=('https://www.skidrowreloaded.com/feed/',))
    t3 = threading.Thread(target=feed_reader, args=('https://fitgirl-repacks.site/feed/',))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    sleep(60)
    clear_console()

# dev-ed.ru
