import numpy as np
from util import calc_noise


class Game:
    """
    A class that represents a collective-risk dilemma as an evolutionary game.
    """
    def __init__(self, setup, players):
        self.players = players
        self.num_rounds = setup.num_rounds
        self.risk = setup.risk
        self.risk_dev = setup.risk_dev
        self.interest = setup.interest
        self.target_sum = setup.target_sum
        self.target_dev = setup.target_dev

    def play(self):
        """
        A method that will play a single game.
        :return: A boolean if the target was reached or not.
        """
        contributions = 0
        # Store the total contribution for each player, needed to compute behavior frequencies
        player_contribution = np.zeros(len(self.players), dtype=np.int32)
        for round in range(self.num_rounds):
            round_contributions = 0
            for i, player in enumerate(self.players):
                contribution = player.select_action(round, contributions)
                round_contributions += contribution
                player_contribution[i] += contribution

            contributions += round_contributions
            contributions += contributions * self.interest

        # Give the payoffs after playing the game.
        target = calc_noise(self.target_sum, self.target_dev)
        target_reached = contributions >= target
        risk = calc_noise(self.risk, self.risk_dev)
        if target_reached or risk < np.random.uniform(0, 1):
            for player in self.players:
                player.payoffs.append(player.balance)
                player.balance = player.starting_balance
        else:
            for player in self.players:
                player.payoffs.append(0)
                player.balance = player.starting_balance

        return target_reached, player_contribution
