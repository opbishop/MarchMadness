import pandas as pd


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


def parse_historic(soup):
    """
    Read all tournament results and return as Pandas Dataframe

    :param soup:
    :return:
    """
    schedule = soup.find_all('div', {'class': 'tournament-group-preview-holder mod-full mod-small-pd mod-pubg'})

    results = []

    # ignore total tournament standings by only considering [1:]
    # for each game in the tournament
    for game in schedule[1:]:
        positions = []
        team_names = []
        # for each team in the game
        for team_details in game.find_all('div', {'class': 'preview-item'}):
            strings = team_details.find_all('span', limit=2)
            positions.append(int(strings[0].text))
            team_names.append(strings[1].text)

        data = {
            'Position': positions,
            'Team Name': team_names
        }

        results.append(pd.DataFrame(data, columns=['Position', 'Team Name']))

    return results


def parse_historic_stats(soup):
    """
    Read all tournament stats and return as Pandas Dataframe

    :param soup:
    :return:
    """
    schedule = soup.find_all('div', {'class': 'tournament-group-preview-holder mod-full mod-small-pd mod-pubg'})

    results = []
    # team_list = soup.find('div', {'class': 'preview-item-list'})
    # team_details = team_list.find_all('div', {'class': 'preview-item'})

    for game in range(1, len(schedule)):
        team_details = schedule[game].find_all('div', {'class': 'preview-item'})
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

        results.append(pd.DataFrame(data, columns=['Placement Pts', 'Kills', 'Kill Pts', 'Overall Pts']))
    return results


def aggregate_historic_results(team_standings, team_stats):
    """
    Aggregate team standings & team stats into single results table, return sorted aggregated table

    :param team_standings:
    :param team_stats:
    :return:
    """
    historic_results = []

    for game in range(0, len(team_standings)):
        temp_df = pd.concat([team_standings[game], team_stats[game]], axis=1)
        temp_df.drop('Position', axis=1, inplace=True)
        historic_results.append(temp_df)

    results = pd.concat(historic_results, ignore_index=True)

    results[['Placement Pts', 'Kills', 'Kill Pts', 'Overall Pts']] = results[
        ['Placement Pts', 'Kills', 'Kill Pts', 'Overall Pts']].apply(pd.to_numeric)

    results = pd.pivot_table(results, values=['Placement Pts', 'Kills', 'Kill Pts', 'Overall Pts'], index='Team Name',
                             aggfunc=sum)

    return results.sort_values('Overall Pts', ascending=False)
