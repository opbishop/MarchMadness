import custom_exception

import tldextract
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
    ext = tldextract.extract(url)

    response = requests.get('http://{}.{}/robots.txt'.format(ext.domain, ext.suffix), headers={
        'User - Agent': 'python - requests / 4.8.2(Compatible;{};{})'.format(user_agent['name'], user_agent['email'])},
                            timeout=10)

    # Only scrape URL if allowed by robots.txt
    if response.status_code != 200:
        if response.status_code == 404:
            # TODO 404 exception
            print('Robots.txt not found')
        else:
            raise custom_exception.DisallowedException(response.status_code)

    return requests.get(url)


def parse_links(soup):
    """
    Return a dictionary from all href links on site and their displayed String name on the page

    :param soup:
    :return:
    """
    print(soup.prettify())
    results = {}
    for link in soup.find_all('a'):
        print(link.attrs)
        if link.string is not None:
            results[link.string] = link.attrs['href']
    return results


def parse_ss_teams(soup):
    teams = {}
    team_list = soup.find('div', {'class': 'preview-item-list'})

    for team_details in team_list.find_all('div', {'class': 'preview-item'}):
        strings = team_details.find_all('span', limit=2)
        teams[strings[0].text] = strings[1].text

    print(teams)


# Dictionary of websites to access
urls = {
    # 'Web Scraper Test Site': 'http://webscraper.io',
    'StarLadder': 'https://starladder.com/en/starseries-i-league-pubg',
    # 'Google': 'http://www.google.com',
    # 'Reddit': 'https://www.reddit.com'
}

for key, value in urls.items():
    print(value)
    try:
        page = BeautifulSoup(get_url(value).text, 'html.parser')
        parse_ss_teams(page)
        # print(page.prettify())
        # print(parse_links(page))
    except custom_exception.DisallowedException as e:
        print('Connection to {} not permitted with HTTP code {}. Does its robots.txt allow access?'.format(value,
                                                                                                           e.status))
