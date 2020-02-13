import numpy as np
import pandas as pd
import argparse

from BuildSimulation import BuildSimulation
from Generation import Generation


def run_simulation(setup, savefile):
    """
    A helper function that will run the simulation.
    :param setup: An object containing all variables that will be used in the simulation.
    :return: averaged payoffs per generation, number of times the target was reached per generation 
        and the averaged contributions per round per generation (GxR matrix)
    """
    generations_avg_payoffs = []
    generations_targets_reached = []
    generations_rounds_contributions_counts = []
    generations_behaviors_counts = []

    generation = Generation(setup)
    for i in range(setup.num_generations):
        print("Generation " + str(i))
        targets_reached, avg_payoff, rounds_contributions_counts, behaviors_counts = generation.play()
        generations_avg_payoffs.append(avg_payoff)
        generations_targets_reached.append(np.sum(targets_reached))
        generations_rounds_contributions_counts.append(rounds_contributions_counts.tolist())
        generations_behaviors_counts.append(behaviors_counts.tolist())
        print("Targets reached: ", np.sum(targets_reached))
        print("With an average payoff of " + str(avg_payoff))
        print("Behavior counts: ")
        print(behaviors_counts)
        print("Rounds contributions counts: ")
        print(rounds_contributions_counts)
        generation.evolve()

    print(generations_targets_reached)

    # We place everything inside a dictionary and then in a data frame.
    results = {"avg_payoffs": generations_avg_payoffs,
               "targets_reached": generations_targets_reached,
               "rounds_contributions_counts": generations_rounds_contributions_counts,
               "behaviors_counts": generations_behaviors_counts}
    results_df = pd.DataFrame(results)
    
    # We write the results to a file.
    results_df.to_csv(savefile, sep=',', mode='w', header=True, index=False, encoding="ascii")


if __name__ == "__main__":
    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--risk", type=float, help="the risk factor of the evolutionary game")
    parser.add_argument("--interest", type=float, help="the interest for the evolutionary game")
    parser.add_argument("--target-dev", type=float, help="the standard deviation of the contribution target")
    args = parser.parse_args()

    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    # Set the user specified variables if they chose to do so.
    if args.risk is not None:
        setup.risk = args.risk

    if args.interest is not None:
        setup.interest = args.interest

    if args.target_dev is not None:
        setup.target_dev = args.target_dev

    # Filename where to save the results to.
    file = "results-" + str(setup.risk) + "-" + str(setup.interest) + "-" + str(setup.target_dev) + ".csv"

    # Running the simulation.
    print("Starting simulation for risk = " + str(setup.risk) + ", interest = "
          + str(setup.interest) + ", target deviation = " + str(setup.target_dev))
    run_simulation(setup, file)
