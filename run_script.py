import news_data_processor as dp
import custom_exception
import scraper as scrape

from bs4 import BeautifulSoup
import _thread
import threading
import time
import json


def check_bbc(thread_name, delay):
    """
    Check BBC News for news stories

    :param thread_name:
    :param delay: time to sleep thread for (s)
    :return:
    """
    count = 0
    stories = []
    while count < 5:
        time.sleep(delay)
        count += 1
        print('checking bbc {}'.format(count))
        dp.bbc(BeautifulSoup(scrape.get_url(urls['BBC']).text, 'html.parser'), stories)
    persist(stories, 'bbc_stories')



def check_sky(thread_name, delay):
    """
    Check Sky News for news stories

    :param thread_name:
    :param delay: time to sleep thread for (s)
    :return:
    """
    count = 0
    stories = []
    while count < 5:
        time.sleep(delay)
        count += 1
        print('checking sky {}'.format(count))
        dp.sky(BeautifulSoup(scrape.get_url(urls['Sky']).text, 'html.parser'), stories)
        persist(stories, 'sky_stories')


def persist(stories, filename):
    with open('{}.txt'.format(filename), 'w') as outfile:
        json.dump(stories, outfile)



# Dictionary of websites to access
urls = {
    # 'StarLadder': 'https://starladder.com/en/starseries-i-league-pubg',
    'BBC': 'http://www.bbc.co.uk/news',
    'Sky': 'https://news.sky.com/uk'
}

# Start a thread to check both news sources given (function, (args)
try:
    t1 = threading.Thread(target = check_bbc, args=('Thread 1', 10))
    t2 = threading.Thread(target = check_sky, args=('Thread 1', 20))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

except custom_exception.DisallowedException as e:
    print('Connection not permitted with HTTP code {}. Does its robots.txt allow access?'.format(e.status))
