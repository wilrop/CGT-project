class Game:
    """
    A class that represents a collective-risk dilemma as an evolutionary game.
    """
    def __init__(self, players, risk, rounds):
        self.players = players
        self.risk = risk
        self.rounds = rounds