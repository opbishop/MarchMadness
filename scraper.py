import custom_exception

import tldextract
import requests
from bs4 import BeautifulSoup
import pandas as pd


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
    """
    Read and return team position and name as a Pandas DataFrame

    :param soup:
    :return:
    """
    positions = []
    team_names = []
    team_list = soup.find('div', {'class': 'preview-item-list'})

    for team_details in team_list.find_all('div', {'class': 'preview-item'}):
        strings = team_details.find_all('span', limit=2)
        positions.append(int(strings[0].text))
        team_names.append(strings[1].text)

    data = {
        'Position': positions,
        'Team Name': team_names
    }

    return pd.DataFrame(data, columns=['Position', 'Team Name'])


def parse_ss_stats(soup):
    """
    Read and return team points as a Pandas DataFrame

    :param soup:
    :return:
    """
    team_list = soup.find('div', {'class': 'preview-item-list'})
    team_details = team_list.find_all('div', {'class': 'preview-item'})
    placement_pts = []
    kills = []
    kills_pts = []
    overall_pts = []

    for team in team_details:
        placement_pts.append(team.contents[5].find('span').text)
        kills.append(team.contents[7].find('span').text)
        kills_pts.append(team.contents[9].find('span').text)
        overall_pts.append(team.contents[11].find('span').text)

    data = {
        'Placement Pts': placement_pts,
        'Kills': kills,
        'Kill Pts': kills_pts,
        'Overall Pts': overall_pts
    }

    return pd.DataFrame(data, columns=['Placement Pts', 'Kills', 'Kill Pts', 'Overall Pts'])

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
        team_standings = parse_ss_teams(page)
        team_stats = parse_ss_stats(page)

        print(pd.concat([team_standings,team_stats], axis=1))

    except custom_exception.DisallowedException as e:
        print('Connection to {} not permitted with HTTP code {}. Does its robots.txt allow access?'.format(value,
                                                                                                           e.status))
