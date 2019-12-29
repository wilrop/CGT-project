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
        self.population = [Player(setup.initial_endowment, setup.legal_moves, self.num_rounds, setup.target_sum) for x in range(self.population_size)]
        self.risk = setup.risk
        self.beta = setup.beta

    def play(self):
        """
        A function that will play all the games of the generation.
        :return: An array that holds for every game if the target was reached, 
            the average payoff and the average contributions per round.
        """
        targets_reached = []
        for i in range(self.num_games):
            players = np.random.choice(self.population, self.num_players, replace=False)  # Pick players for the game.
            game = Game(self.setup, players)
            target_reached = game.play()
            targets_reached.append(target_reached)

        avg_payoff = np.average([np.average(player.payoffs) for player in self.population if player.games_played > 0])
        avg_rounds_contributions = np.average(
            [player.rounds_contributions / player.games_played for player in self.population if player.games_played > 0], 
            axis=0)

        return targets_reached, avg_payoff, avg_rounds_contributions

    def calculate_fitness(self):
        """
        A function that will calculate the fitness of all players in the generation.
        :return: An array containing the fitness per player.
        """
        avg_payoffs = [np.average(player.payoffs) for player in self.population if player.games_played > 0]
        fitness = np.exp(avg_payoffs * self.beta)
        return fitness

    def evolve(self):
        """
        A function that will execute a Wright-Fisher process to evolve a generation.
        :return: /
        """
        fi = self.calculate_fitness()
        fitness_sum = np.sum(fi)
        probabilities = fi / fitness_sum  # Calculate the probabilities that a player will get chosen to be a parent.
        population = list(filter(lambda p: p.games_played > 0, self.population))
        parents = np.random.choice(population, size=self.population_size, replace=True, p=probabilities)
        offspring = []
        for parent in parents:
            child = parent.create_offspring(self.setup.mu, self.setup.sigma)  # Create offspring.
            offspring.append(child)

        self.population = offspring  # Set the population to the offspring, thereby "evolving" the population.
