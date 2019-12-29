import numpy as np
import matplotlib.pyplot as plt

from src.BuildSimulation import BuildSimulation
from src.Generation import Generation


def plot_risk_prob_proportions(setup, risks, results):
    """
    Generates a plot showing the evolution of payoffs, probability of reaching the target,
    total contributions, and contributions in different rounds interval for varying risk probabilities.
    """
    risks_payoffs = []
    risks_targets = []
    risks_contribs = []
    risks_fh_contribs = []
    risks_sh_contribs = []
    for risk, (payoffs, targets, rounds_contributions) in zip(risks, results):
        
        avg_payoff = np.average(payoffs) / setup.initial_endowment
        risks_payoffs.append(avg_payoff)
        
        avg_target = np.average(targets) / setup.num_games
        risks_targets.append(avg_target)

        fh_contributions = np.sum(rounds_contributions[:, :setup.num_rounds//2], axis=1)
        fh_avg_contribution = np.average(fh_contributions) / setup.initial_endowment
        risks_fh_contribs.append(fh_avg_contribution)

        sh_contributions = np.sum(rounds_contributions[:, setup.num_rounds//2:], axis=1)
        sh_avg_contribution = np.average(sh_contributions) / setup.initial_endowment
        risks_sh_contribs.append(sh_avg_contribution)

        avg_contribution = fh_avg_contribution + sh_avg_contribution
        risks_contribs.append(avg_contribution)

    plt.figure()
    plt.plot(risks, risks_payoffs, label="Payoff")
    plt.plot(risks, risks_contribs, label="Contribution")
    plt.plot(risks, risks_targets, label="Target")
    plt.plot(risks, risks_fh_contribs, label="First half contributions")
    plt.plot(risks, risks_sh_contribs, label="Second half contributions")
    plt.ylim((0, 1))
    plt.xlabel("Risk probability")
    plt.ylabel("Proportion")
    plt.legend()
    plt.savefig("test2.png", dpi=300)
    plt.show()

def plot_trajectories(setup, result):
    """
    Generates a plot showing the evolution of the average contribution, payoff and proportion of 
    targets reached across generations.
    """
    generations = np.linspace(1, setup.num_generations, setup.num_generations)
    payoffs, targets, rounds_contributions = result
    contributions = np.sum(rounds_contributions, axis=1)
    
    plt.figure(figsize=(16, 4))
    plt.plot(generations, payoffs / setup.initial_endowment, label="Payoff")
    plt.plot(generations, contributions / setup.initial_endowment, label="Contribution")
    plt.plot(generations, targets / setup.num_games, label="Target")
    plt.ylim((0, 1))
    plt.xlabel("Generations")
    plt.ylabel("Proportion")
    plt.legend()
    plt.savefig("test.png", dpi=300)
    plt.show()


def run_simulation(setup):
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

    risks = np.linspace(0.0, 1.0, 21) # 0.05 step size, open intervals
    results = []
    for risk in risks:
        print("Simulation for risk " + str(risk))
        setup.risk = risk
        # Running the simulation.
        result = run_simulation(setup)
        results.append(result)

    plot_risk_prob_proportions(setup, risks, results)
    # plot_trajectories(setup, results[0])


