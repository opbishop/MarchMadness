import json

def bbc(soup):
    news_stories = soup.find_all('div', {'class': 'gs-c-promo-body'})

    stories = []

    for story in news_stories:
        story_dict = {}
        if len(story.find('h3').text) == 0:
            continue
        else:
            story_dict['title'] = (story.find('h3').text).strip()
        try:
            story_dict['link'] = story.find('a')['href']
        except TypeError as e:
            # TODO: log
            story_dict['link'] = 'None'
        stories.append(story_dict)

    return convert_to_json(stories)


def sky(soup):
    news_stories = soup.find_all('h3', {'class': 'sdc-news-story-grid__headline'})
    stories = []

    for story in news_stories:
        story_dict = {
            'title': story.text.strip(),
            'link': story.find('a')['href']
        }
        stories.append(story_dict)

    return convert_to_json(stories)


def convert_to_json(stories):
    return json.dumps(stories)
