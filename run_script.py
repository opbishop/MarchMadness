import data_processor as dp
import custom_exception
import scraper as scrape

from bs4 import BeautifulSoup


# Run stuff
# Dictionary of websites to access
urls = {
    # 'Web Scraper Test Site': 'http://webscraper.io',
    'StarLadder': 'https://starladder.com/en/starseries-i-league-pubg',
    # 'Google': 'http://www.google.com',
    # 'Reddit': 'https://www.reddit.com'
}

for key, value in urls.items():

    try:
        page = BeautifulSoup(scrape.get_url(value).text, 'html.parser')

        team_standings = dp.parse_historic(page)
        team_stats = dp.parse_historic_stats(page)

        final_results = dp.aggregate_historic_results(team_standings, team_stats)

        print(final_results)

    except custom_exception.DisallowedException as e:
        print('Connection to {} not permitted with HTTP code {}. Does its robots.txt allow access?'.format(value,
                                                                                                           e.status))
