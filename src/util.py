import numpy as np

def get_risk_prob_behaviors(setup, risks, results):

    # C = 0
    risks_c_0_freq = []
    # C < R
    risks_c_lt_r_freq = []
    # C = R
    risks_c_r_freq = []
    # C > R
    risks_c_gt_r_freq = []

    behaviors_intervals = [
        (risks_c_0_freq, 0, 1),
        (risks_c_lt_r_freq, 1, setup.num_rounds),
        (risks_c_r_freq, setup.num_rounds, setup.num_rounds + 1),
        (risks_c_gt_r_freq, setup.num_rounds + 1, setup.num_rounds * max(setup.legal_moves) + 2)
    ]

    for result in results:
        behaviors_counts = np.array(result["behaviors_counts"].tolist())

        # Sum across generations
        behaviors_counts = np.sum(behaviors_counts, axis=0)

        # Retrieve the sum to compute frequencies
        num_observations = np.sum(behaviors_counts)

        for risks_freq, lower_contrib, upper_contrib in behaviors_intervals:
            risks_freq.append(np.sum(behaviors_counts[lower_contrib:upper_contrib]) / num_observations)

    return risks_c_0_freq, risks_c_lt_r_freq, risks_c_r_freq, risks_c_gt_r_freq



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
