import numpy as np


class Player:
    """
    A class that represents a player in our collective-risk dilemma.
    """
    def __init__(self, coins, legal_moves):
        self.balance = coins
        self.legal_moves = legal_moves  # The contributions that are allowed in our game.

        # The player strategy.
        self.threshold = np.random.uniform(0, 1)  # Initial thresholds are uniformly distributed between 0 and 1.
        self.strategy_above = np.random.choice(legal_moves)
        self.strategy_below = np.random.choice(legal_moves)

    def choose_action(self):
        """
        A method that will chose a function given a players strategy.
        :return:
        """
        return 0
