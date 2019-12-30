import numpy as np
import pandas as pd

from src.BuildSimulation import BuildSimulation
from src.Generation import Generation


def run_simulation(setup, savefile):
    """
    A helper function that will run the simulation.
    :param setup: An object containing all variables that will be used in the simulation.
    :return: averaged payoffs per generation, number of times the target was reached per generation 
        and the averaged contributions per round per generation (GxR matrix)
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
        generations_avg_rounds_contributions.append(avg_rounds_contributions.tolist())
        print("Targets reached: ", np.sum(targets_reached))
        print("With an average payoff of " + str(avg_payoff))
        print("Averaged rounds contributions : ")
        print(avg_rounds_contributions)
        generation.evolve()

    print(generations_targets_reached)

    # We place everything inside a dictionary and then in a data frame.
    results = {"avg_payoffs": generations_avg_payoffs,
               "targets_reached": generations_targets_reached,
               "avg_rounds_contributions": generations_avg_rounds_contributions}
    results_df = pd.DataFrame(results)

    # We write the results to a file.
    with open(savefile, 'a') as f:
        results_df.to_csv(f, sep=',', mode='a', header=True, index=False, encoding="ascii")


if __name__ == "__main__":
    # Declaring the file we want to save the results to.
    filename = "results"

    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    risks = np.linspace(0.0, 1.0, 21)  # 0.05 step size, open intervals
    for risk in risks:
        print("Simulation for risk " + str(risk))
        setup.risk = risk
        savefile = filename + "-" + str(risk) + ".csv"

        # Running the simulation.
        run_simulation(setup, savefile)
