import numpy as np
import pandas as pd
import argparse

from BuildSimulation import BuildSimulation
from Generation import Generation


def run_simulation(setup, savefile):
    """
    A helper function that will run the simulation.
    :param setup: An object containing all variables that will be used in the simulation.
    :param savefile: The file where we want to save the results to.
    :return: averaged payoffs per generation, number of times the target was reached per generation 
        and the averaged contributions per round per generation (GxR matrix)
    """
    generations_avg_payoffs = []
    generations_targets_reached = []
    generations_rounds_contributions_counts = []
    generations_behaviors_counts = []

    generation = Generation(setup)
    for i in range(setup.num_generations):
        setup.risk += setup.risk_cont
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
        # If we are investigating the robustness of strategies we return the number of generations it has survived.
        if setup.strategy is not None:
            if generation.frequency < setup.population_size / 2:
                return i

    # If we are investigating the robustness of strategies we return the number of generations it has survived.
    if setup.strategy is not None:
        return setup.num_generations

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
    parser.add_argument("--risk-dev", type=float, help="the standard deviation of the risk factor")
    parser.add_argument("--interest", type=float, help="the interest for the evolutionary game")
    parser.add_argument("--target-dev", type=float, help="the standard deviation of the contribution target")
    parser.add_argument("--strategy", type=str, help="the strategy for the population")
    parser.add_argument("--continuous", type=float, help="Make the risk factor continuous")
    args = parser.parse_args()

    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    # Set the user specified variables if they chose to do so.
    if args.risk is not None:
        setup.risk = args.risk

    if args.risk_dev is not None:
        setup.risk_dev = args.risk_dev

    if args.continuous is not None:
        setup.risk_cont = args.continuous

    if args.interest is not None:
        setup.interest = args.interest

    if args.target_dev is not None:
        setup.target_dev = args.target_dev

    if args.strategy is not None:
        if args.strategy == "Non-contributors":
            setup.strategy = [0] * setup.num_rounds
        elif args.strategy == "Altruists":
            setup.strategy = [2] * setup.num_rounds
        elif args.strategy == "Fair-rational":
            setup.strategy = [0] * int((setup.num_rounds / 2)) + [2] * int((setup.num_rounds / 2))
        elif args.strategy == "Fair-naive":
            setup.strategy = [1] * setup.num_rounds
        elif args.strategy == "Fair-rational-reverse":
            setup.strategy = [2] * int((setup.num_rounds / 2)) + [0] * int((setup.num_rounds / 2))

        # Filename where to save the results to.
        file = "results-" + args.strategy + ".csv"

        risks = np.linspace(0.0, 1.0, 21)  # 0.05 step size, open intervals

        for risk in risks:
            setup.risk = risk
            runs = 100
            total = 0

            # Execute the experiment for multiple runs.
            for i in range(runs):
                # Running the simulation.
                print("Starting simulation for risk = " + str(setup.risk) + ", interest = "
                      + str(setup.interest) + ", target deviation = " + str(setup.target_dev))
                time = run_simulation(setup, file)
                total += time
                # This is to save time
                if time == setup.num_generations:
                    runs = i + 1
                    break

            # Calculate the average amount of time it took.
            avg = total / runs
            result = {"risk": [risk],
                      "duration": [avg]}
            result = pd.DataFrame(result)
            result.to_csv(file, sep=',', mode='a', header=True, index=False, encoding="ascii")
    else:
        # Filename where to save the results to.
        file = "results-" + str(setup.risk) + "-" + str(setup.interest) + "-" + str(setup.target_dev) + ".csv"

        # Running the simulation.
        print("Starting simulation for risk = " + str(setup.risk) + ", interest = "
              + str(setup.interest) + ", target deviation = " + str(setup.target_dev))
        run_simulation(setup, file)
