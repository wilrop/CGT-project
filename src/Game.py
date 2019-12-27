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
        :return: A boolean if the target was reached or not.
        """
        contributions = 0
        for round in range(self.num_rounds):
            round_contributions = 0
            for player in self.players:
                contribution = player.select_action(round, contributions, self.target_sum)
                round_contributions += contribution

            contributions += round_contributions

        # Give the payoffs after playing the game.
        if contributions >= self.target_sum or self.risk < np.random.uniform(0, 1):
            for player in self.players:
                player.payoffs.append(player.balance)
                player.balance = player.starting_balance
        else:
            for player in self.players:
                player.payoffs.append(0)
                player.balance = player.starting_balance

        return contributions >= self.target_sum
