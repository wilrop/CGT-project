import numpy as np
import matplotlib.pyplot as plt

from src.BuildSimulation import BuildSimulation
from src.Generation import Generation

def plot_game_summary(setup):
    pass

def plot_trajectories(setup, results):
    """
    Generates a plot showing the evolution of the average contribution, payoff and proportion of 
    targets reached across generations.
    """
    generations = np.linspace(1, setup.num_generations, setup.num_generations)
    payoffs, targets, rounds_contributions = results
    contributions = np.sum(rounds_contributions, axis=1)
    
    plt.figure()
    plt.plot(generations, payoffs / setup.initial_endowment, label="Payoff")
    plt.plot(generations, contributions / setup.initial_endowment, label="Contribution")
    plt.plot(generations, targets / setup.num_games, label="Target Reached")
    plt.xlabel("Generations")
    plt.ylabel("Proportion")
    plt.legend()
    plt.show()

def run_simulation(setup):
    """
    A helper function that will run the simulation.
    :param setup: An object containing all variables that will be used in the simulation.
    :return: Nothing as of now. TODO make it return something useful.
    """
    generations_avg_payoffs = []
    generations_targets_reached = []
    generations_avg_rounds_contributions = []

    generation = Generation(setup)
    for i in range(setup.num_generations):
        print("Generation " + str(i))
        targets_reached, avg_payoff, avg_rounds_contributions = generation.play()
        generations_avg_payoffs.append(avg_payoff)
        generations_targets_reached.append(np.sum(targets_reached))
        generations_avg_rounds_contributions.append(avg_rounds_contributions)
        print("Targets reached: ", np.sum(targets_reached))
        print("With an average payoff of " + str(avg_payoff))
        print("Averaged rounds contributions : ")
        print(avg_rounds_contributions)
        generation.evolve()

    print("Average payoff over all generations: ")
    print(np.average(generations_avg_payoffs))
    return np.array(generations_avg_payoffs), np.array(generations_targets_reached), np.array(generations_avg_rounds_contributions)


if __name__ == "__main__":
    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    # Running the simulation.
    results = run_simulation(setup)

    # Plot the results.
    plot_trajectories(setup, results)


