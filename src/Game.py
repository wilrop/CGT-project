class Game:
    """
    A class that represents a collective-risk dilemma as an evolutionary game.
    """
    def __init__(self, players, num_rounds, risk):
        self.players = players
        self.num_rounds = num_rounds
        self.risk = risk

        self.target_sum = len(players) * num_rounds  # The target sum that needs to be invested before succeeding.

    def play(self):
        """
        A method that will play a single game.
        :return:
        """
        return 0