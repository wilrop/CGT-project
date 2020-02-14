import numpy as np
from util import calc_noise


class Player:
    """
    A class that represents a player in our collective-risk dilemma.
    """
    def __init__(self, setup):
        self.setup = setup
        self.starting_balance = setup.initial_endowment
        self.balance = setup.initial_endowment
        self.legal_moves = setup.legal_moves  # The contributions that are allowed in our game.
        self.legal_move_idx = setup.legal_move_idx
        self.rounds = setup.num_rounds
        self.target = setup.target_sum

        # The player strategies.
        self.thresholds = np.random.uniform(0, 1, size=self.rounds)
        self.strategies_above = np.random.choice(self.legal_moves, size=self.rounds)
        self.strategies_below = np.random.choice(self.legal_moves, size=self.rounds)
        self.strategy = setup.strategy  # This is either a user provided strategy for the entire population or None

        # Initialize the player's payoff history
        self.payoffs = []

        # Initialize the player's per-round contributions counts (summed for the played games)
        self.rounds_contributions_counts = np.zeros((self.rounds, len(self.legal_moves)))

    @property
    def games_played(self):
        return len(self.payoffs)

    def select_action(self, round, contributions):
        """
        A method that will select an action for this player.
        :param round: The current round.
        :param contributions: The current contributions in the common account.
        :return: A contribution to the common account.
        """
        if self.strategy is not None:
            contribution = self.strategy[round]
        else:
            # We first select the correct strategy for this round.
            threshold = self.thresholds[round] * self.target
            strategy_above = self.strategies_above[round]
            strategy_below = self.strategies_below[round]

            if contributions < threshold and self.balance >= strategy_below:
                contribution = strategy_below
            elif contributions >= threshold and self.balance >= strategy_above:
                contribution = strategy_above
            else:
                contribution = 0

        self.balance -= contribution
        self.rounds_contributions_counts[round, self.legal_move_idx[contribution]] += 1
        return contribution

    def create_offspring(self, mu, sigma):
        """
        A method that will create a child from this player.
        :param mu: The mutation probability.
        :param sigma: The standard deviation in the normal distribution used for the noise generation.
        :return: A newly created player that represents the child of this player.
        """
        offspring = Player(self.setup)

        # Force copy of numpy array to avoid multiple children cumulatively mutating the same strategy.
        offspring.thresholds = np.copy(self.thresholds)
        offspring.strategies_above = np.copy(self.strategies_above)
        offspring.strategies_below = np.copy(self.strategies_below)
        offspring.strategy = np.copy(self.strategy)

        # Check for random mutation in every round.
        for round in range(self.rounds):
            if np.random.uniform(0, 1) < mu:
                if self.strategy is not None:
                    offspring.strategy[round] = np.random.choice(self.legal_moves)
                else:
                    offspring.thresholds[round] += calc_noise(0, sigma)
                    offspring.strategies_above[round] = np.random.choice(self.legal_moves)
                    offspring.strategies_below[round] = np.random.choice(self.legal_moves)

        return offspring
