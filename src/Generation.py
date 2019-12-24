import numpy as np

from src.Game import Game
from src.Player import Player


class Generation:
    """
    A class representing a generation for a certain population.
    """
    def __init__(self, setup):
        self.setup = setup
        self.num_games = setup.num_games
        self.num_players = setup.num_players
        self.num_rounds = setup.num_rounds
        self.population = [Player(setup.initial_endowment, setup.legal_moves) for x in range(setup.population_size)]
        self.risk = setup.risk
        self.beta = setup.beta

    def play(self):
        """
        A function that will play all the games of the generation.
        :return: Nothing as of now. TODO make it return something useful.
        """
        for i in range(self.num_games):
            players = np.random.choice(self.population, self.num_players)
            game = Game(self.setup, players)
            game.play()
        return 0

    def calculate_fitness(self):
        """
        A function that will calculate the fitness of all players in the generation.
        :return: An array containing the fitness per player.
        """
        avg_payoffs = [np.average(player.payoffs) for player in self.population]
        fitness = np.exp(avg_payoffs * self.beta)
        return fitness

    def evolve(self):
        """
        A function that will execute a Wright-Fisher process to evolve a generation.
        :return: /
        """
        new_population = self.population
        self.population = new_population
