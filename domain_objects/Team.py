class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.wins = 0

    def win(self):
        self.wins += 1
