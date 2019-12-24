import numpy as np


class Game:
    """
    A class that represents a collective-risk dilemma as an evolutionary game.
    """
    def __init__(self, setup, players):
        self.players = players
        self.num_rounds = setup.num_rounds
        self.risk = setup.risk

        self.target_sum = len(players) * self.num_rounds  # The target sum that needs to be invested before succeeding.

    def play(self):
        """
        A method that will play a single game.
        :return:
        """
        contributions = 0
        for round in range(self.num_rounds):
            for player in self.players:
                if contributions < player.threshold and player.balance >= player.strategy_below:
                    contributions += player.strategy_below
                    player.balance -= player.strategy_below
                elif contributions >= player.threshold and player.balance >= player.strategy_above:
                    contributions += player.strategy_above
                    player.balance -= player.strategy_above

        # Give The payoffs after playing the game.
        if contributions >= self.target_sum or self.risk < np.random.uniform(0, 1):
            for player in self.players:
                player.payoffs.append(player.balance)
        else:
            for player in self.players:
                player.payoffs.append(0)

        return contributions
