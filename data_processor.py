from domain_objects import Game, Team


def tournament_regions(bracket):
    regions = bracket.find_all('li', {'class': 'region'})
    x = []
    for region in regions:
        x.append({
            'name': region.h3.text,
            'games_played': games(bracket),
            'round': region.ul.li['class']
        })
    return x


def games(bracket):
    games = bracket.find_all('li', {'class': 'game'})
    all_teams = teams(bracket)
    games_played = []
    for game in games:
        id = game['data-game-id']
        player_names = [name.text for name in game.find_all('span', {'class': 'name'})]
        players = ([team for team in all_teams if team.name in player_names])
        score = [score.text for score in game.find_all('span', {'class': 'score'})]
        overtime = game.find('span', {'class': 'status'}) == "FINAL"
        winner = players[score.index(max(score))]
        winner.win()
        games_played.append(Game.Game(id, players, score, overtime, winner))
    return games_played


def teams(bracket):
    teams = bracket.find_all('li', {'class': 'team'})
    found_teams = []
    for team in teams:
        name = team.find('span', {'class': 'name'}).text.strip()
        if name not in [team.name for team in found_teams] and len(name) != 0:
            seed = team.find('span', {'class': 'seed'}).text
            found_teams.append(Team.Team(name, seed))
        else:
            continue
    return found_teams
