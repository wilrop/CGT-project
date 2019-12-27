import numpy as np

from src.BuildSimulation import BuildSimulation
from src.Generation import Generation


def run_simulation(setup):
    """
    A helper function that will run the simulation.
    :param setup: An object containing al variables that will be used in the simulation.
    :return: Nothing as of now. TODO make it return something useful.
    """
    avg_payoffs = []

    generation = Generation(setup)
    for i in range(setup.num_generations):
        print("Generation " + str(i))
        targets_reached, avg_payoff = generation.play()
        avg_payoffs.append(avg_payoff)
        print("Targets reached: ")
        print(np.unique(targets_reached, return_counts=True))
        print("With an average payoff of " + str(avg_payoff))
        generation.evolve()

    print("Average payoff over all generations: ")
    print(np.average(avg_payoffs))
    return 0


if __name__ == "__main__":
    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    # Running the simulation.
    run_simulation(setup)
