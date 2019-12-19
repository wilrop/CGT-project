import numpy as np

from src.Game import Game
from src.Player import Player


class Generation:
    """
    A class representing a generation for a certain population.
    """
    def __init__(self, num_games, population_size, num_players, initial_endowment):
        self.num_games = num_games
        self.num_players = num_players
        self.population = [Player(initial_endowment) for x in range(population_size)]

    def play(self, num_rounds, risk):
        """
        A function that will play all the games of the generation.
        :param num_rounds: The amount of rounds a single game has to run for.
        :param risk: The risk of losing what you have not invested, when failing the game.
        :return: Nothing as of now. TODO make it return something useful.
        """
        for i in range(self.num_games):
            players = np.random.choice(self.population, self.num_players)
            game = Game(players, num_rounds, risk)
            game.play()
        return 0