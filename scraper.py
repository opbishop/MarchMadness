import custom_exception
import requests
from bs4 import BeautifulSoup


def get_url(url):
    """
    Check URL's robots.txt for permission to access. If allowed, return HTTP of page.

    :param url:
    :return:
    """
    user_agent = {
        'name': 'John Smith',
        'email': 'john.smith@js.com'
    }
    response = requests.get(url+'/robots.txt', headers={
        'User - Agent': 'python - requests / 4.8.2(Compatible;{};{})'.format(user_agent['name'], user_agent['email'])},
                            timeout=10)

    # Only scrape URL if allowed by robots.txt
    if response.status_code != 200:
        raise custom_exception.DisallowedException(response.status_code)

    return requests.get(url)


def parse_links(soup):
    """
    Return a dictionary from all href links on site and their displayed String name on the page

    :param soup:
    :return:
    """
    results = {}
    for link in soup.find_all('a'):
        if link.string is not None:
            results[link.string] = link.attrs['href']
    return results


# Dictionary of websites to access
urls = {
    'Web Scraper Test Site': 'http://webscraper.io',
    'Google': 'http://www.google.com',
    'Reddit': 'https://www.reddit.com'
}

for key, value in urls.items():
    print(value)
    try:
        page = BeautifulSoup(get_url(value).text, 'html.parser')
        print(parse_links(page))
    except custom_exception.DisallowedException as e:
        print('Connection to {} not permitted with HTTP code {}. Does its robots.txt allow access?'.format(value,
                                                                                                           e.status))
