import news_data_processor as dp
import custom_exception
import scraper as scrape

from bs4 import BeautifulSoup


# Run stuff
# Dictionary of websites to access
urls = {
    # 'StarLadder': 'https://starladder.com/en/starseries-i-league-pubg',
     'BBC': 'http://www.bbc.co.uk/news',
     'Sky': 'https://news.sky.com/uk'
}


try:
    bbc_page = BeautifulSoup(scrape.get_url(urls['BBC']).text, 'html.parser')
    sky_page = BeautifulSoup(scrape.get_url(urls['Sky']).text, 'html.parser')

    bbc_stories = dp.bbc(bbc_page)
    sky_stories = dp.sky(sky_page)

    print(bbc_stories)
    print(sky_stories)

    # team_standings = dp.parse_historic(page)
    # team_stats = dp.parse_historic_stats(page)
    #
    # final_results = dp.aggregate_historic_results(team_standings, team_stats)

    # print(final_results)

except custom_exception.DisallowedException as e:
    print('Connection to {} not permitted with HTTP code {}. Does its robots.txt allow access?'.format(value,
                                                                                                       e.status))
