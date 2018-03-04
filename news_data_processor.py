

def bbc(soup, stories):
    """
    Scrape news stories from BBC News

    :param soup:
    :param stories: list of already scraped dictionaries in form {title: , link: } where link is href URL
        (empty first run)
    :return: list of dictionaries in form {title: , link: } where link is href URL
    """
    news_stories = soup.find_all('div', {'class': 'gs-c-promo-body'})

    for story in news_stories:
        # Create new story
        story_dict = {}
        # Sometimes the div is empty for formatting purposes, we don't want this
        # Also skip any story whose name already exists in the list (we've already seen it)
        if len(story.find('h3').text) == 0 or \
                story.find('h3').text.strip() in set(story['title'] for story in stories):
            continue
        else:
            story_dict['title'] = story.find('h3').text.strip()
        try:
            story_dict['link'] = story.find('a')['href']
        except TypeError as e:
            # TODO: log
            story_dict['link'] = 'None'
        stories.append(story_dict)
        print('NEW from BBC: {} {}'.format(story_dict['title'], story_dict['link']))

    return stories


def sky(soup, stories):
    """
    Check Sky News for new stories

    :param soup:
    :param stories: list of already scraped dictionaries in form {title: , link: } where link is href URL
        (empty first run)
    :return: list of dictionaries in form {title: , link: } where link is href URL
    """
    news_stories = soup.find_all('h3', {'class': 'sdc-news-story-grid__headline'})

    for story in news_stories:
        # If story with this name already exists, skip it
        if story.text.strip() in set(story['title'] for story in stories):
            continue
        story_dict = {
            'title': story.text.strip(),
            'link': story.find('a')['href']
        }
        stories.append(story_dict)
        print('NEW from Sky: {} {}'.format(story_dict['title'], story_dict['link']))

    return stories
