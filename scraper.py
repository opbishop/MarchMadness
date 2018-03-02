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
    if response.status_code == 200:
        # Only scrape URL if allowed by robots.txt
        return requests.get(url)
    else:
        # TODO: raise not allowed by robots.txt exception
        print("Not allowed by robots.txt")


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


if __name__ == '__main__':
    # Dictionary of websites to access
    urls = {
        'Web Scraper Test Site': 'http://webscraper.io',
        'Disc': 'http://discworld.starturtle.net/lpc'
    }

    for key, value in urls.items():
        print(value)
        print(parse_links(BeautifulSoup(get_url(value).text, 'html.parser')))
