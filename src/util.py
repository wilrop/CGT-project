import numpy as np

def get_risk_prob_proportions(setup, risks, results):
    """
    Gets the values of the evolution of payoffs, probability of reaching the target, total contributions and
    contributions in different rounds interval for varying risk probabilities.
    :param setup: The setup file used in the experiments.
    :param risks: The different risk values used in the experiments.
    :param results: The results obtained from the experiments.
    :return: All calculated values.
    """
    risks_payoffs = []
    risks_targets = []
    risks_contribs = []
    risks_fh_contribs = []
    risks_sh_contribs = []

    for risk, result in zip(risks, results):
        payoffs = result["avg_payoffs"]
        targets = result["targets_reached"]
        rounds_contributions_counts = np.array(result["rounds_contributions_counts"].tolist())

        # Sum the counts across generations
        rounds_contributions_counts = np.sum(rounds_contributions_counts, axis=0)
        # Compute the total contributions from the counts
        rounds_contributions = np.sum(rounds_contributions_counts * setup.legal_moves, axis=1) / np.sum(rounds_contributions_counts, axis=1)
        
        avg_payoff = np.average(payoffs) / setup.initial_endowment
        risks_payoffs.append(avg_payoff)

        avg_target = np.average(targets) / setup.num_games
        risks_targets.append(avg_target)

        fh_contributions = np.sum(rounds_contributions[:setup.num_rounds // 2])
        fh_avg_contribution = np.average(fh_contributions) / setup.initial_endowment
        risks_fh_contribs.append(fh_avg_contribution)

        sh_contributions = np.sum(rounds_contributions[setup.num_rounds // 2:])
        sh_avg_contribution = np.average(sh_contributions) / setup.initial_endowment
        risks_sh_contribs.append(sh_avg_contribution)

        avg_contribution = fh_avg_contribution + sh_avg_contribution
        risks_contribs.append(avg_contribution)

    return risks_payoffs, risks_targets, risks_contribs, risks_fh_contribs, risks_sh_contribs
