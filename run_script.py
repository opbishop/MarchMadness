import data_processor as dp
import custom_exception
import scraper as scrape

from bs4 import BeautifulSoup

# Dictionary of websites to access
urls = {
    'MM': 'https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men',
}

try:
    html = open('march_madness.html', 'r')
    soup = BeautifulSoup(html, 'html.parser')
    bracket = soup.find('div', {'class': 'bracket'})

    dp.teams(bracket)
    dp.games(bracket)

except custom_exception.DisallowedException as e:
    print('Connection not permitted with HTTP code {}. Does its robots.txt allow access?'.format(e.status))
