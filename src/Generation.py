import numpy as np
import math

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
        self.population_size = setup.population_size
        self.population = [Player(setup.initial_endowment, setup.legal_moves, self.num_rounds) for x in range(self.population_size)]
        self.risk = setup.risk
        self.beta = setup.beta

    def play(self):
        """
        A function that will play all the games of the generation.
        :return: Nothing as of now. TODO make it return something useful.
        """
        for i in range(self.num_games):
            players = np.random.choice(self.population, self.num_players, replace=False)
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
        print(np.average(avg_payoffs))
        return fitness

    def evolve(self):
        """
        A function that will execute a Wright-Fisher process to evolve a generation.
        :return: /
        """
        fi_lst = self.calculate_fitness()
        fitness_sum = np.sum(fi_lst)
        probabilities = [fi / fitness_sum for fi in fi_lst]

        parents = np.random.choice(self.population, size=self.population_size, replace=True, p=probabilities)
        offspring = []
        for parent in parents:
            child = parent.create_offspring(self.setup.mu, self.setup.sigma)
            offspring.append(child)

        self.population = offspring
