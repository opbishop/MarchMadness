from data_structures import Game, Team
from selenium import webdriver

def games (bracket):
    games = bracket.find_all('li', {'class': 'game'})

    for game in games:
        #Game(id, players, score, overtime, winner)
        id = game['data-game-id']
        players = [name.text for name in game.find_all('span', {'class': 'name'})]
        score = [score.text for score in game.find_all('span', {'class': 'score'})]
        overtime = game.find('span', {'class': 'status'}) == "FINAL"
        winner = players[score.index(max(score))]
        print('id {}, players {}, score {}, overtime {}, winner {}'.format(id, players, score, overtime, winner))
        # TODO create object, return list of objects
        # TODO add the rest of the elements from the page (region etc)


def teams(bracket):
    teams = bracket.find_all('li', {'class': 'team'})

    found_teams = []
    for team in teams:
        name = team.find('span', {'class': 'name'}).text.strip()
        if name not in [name.strip() for name in team.name for team in found_teams] and len(name) != 0:
            seed = team.find('span', {'class': 'seed'}).text.strip()
            found_teams.append(Team.Team(name, seed))
        else:
            continue

    return found_teams