import numpy as np


class Player:
    """
    A class that represents a player in our collective-risk dilemma.
    """
    def __init__(self, coins, legal_moves, rounds):
        self.starting_balance = coins
        self.balance = coins
        self.legal_moves = legal_moves  # The contributions that are allowed in our game.
        self.rounds = rounds

        # The player strategies.
        self.thresholds = np.random.uniform(0, 1, size=rounds)
        self.strategies_above = np.random.choice(legal_moves, size=rounds)
        self.strategies_below = np.random.choice(legal_moves, size=rounds)

        # Initialize the player's payoff history
        self.payoffs = []

    def select_action(self, round, contributions, target):
        """
        A method that will select an action for this player.
        :param round: The current round.
        :param contributions: The current contributions in the common account.
        :param target: The target that we aim to reach with this common account.
        :return: A contribution to the common account.
        """
        # We first select the correct strategy for this round.
        threshold = self.thresholds[round] * target
        strategy_above = self.strategies_above[round]
        strategy_below = self.strategies_below[round]

        if contributions < threshold and self.balance >= strategy_below:
            self.balance -= strategy_below
            return strategy_below
        elif contributions >= threshold and self.balance >= strategy_above:
            self.balance -= strategy_above
            return strategy_above
        else:
            return 0

    def create_offspring(self, mu, sigma):
        """
        A method that will create a child from this player.
        :param mu: The mutation probability.
        :param sigma: The standard deviation in the normal distribution used for the noise generation.
        :return: A newly created player that represents the child of this player.
        """
        def calc_noise():
            """
            Calculate noise from a normal distribution with a given standard deviation.
            :return: The random sample from the distribution.
            """
            return np.random.normal(scale=sigma)

        offspring = Player(self.starting_balance, self.legal_moves, self.rounds)
        offspring.thresholds = self.thresholds
        offspring.strategies_above = self.strategies_above
        offspring.strategies_below = self.strategies_below
        
        # Check for random mutation in every round.
        for round in range(self.rounds):
            if np.random.uniform(0, 1) < mu:
                offspring.thresholds[round] += calc_noise()

            if np.random.uniform(0, 1) < mu:
                offspring.strategies_above[round] = np.random.choice(self.legal_moves)

            if np.random.uniform(0, 1) < mu:
                offspring.strategies_below[round] = np.random.choice(self.legal_moves)

        return offspring
