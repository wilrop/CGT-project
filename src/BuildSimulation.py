class BuildSimulation:
    """
    A class that holds all variables that will be used in the simulation. This class will get passed as a parameter and
    different components of the simulation will use different variables from it.
    """
    def __init__(self):
        # Variables that define an amount for something.
        self.num_generations = 10 ** 4
        self.num_games = 10 ** 3
        self.num_rounds = 10
        self.num_players = 6

        # Variables for the players
        self.population_size = 100
        self.initial_endowment = 2 * self.num_rounds
        self.legal_moves = [0, 1, 2]
        self.target_dev = 0
        self.strategy = None
        # Map the legal moves to their position in the list
        # Useful to keep track of the frequencies of each moves
        self.legal_move_idx = {self.legal_moves[i]: i for i in range(len(self.legal_moves))}
        self.target_sum = self.num_players * self.num_rounds

        # The risk that a player loses their balance.
        self.risk = 0.9  # Risk is represented as a probability.
        self.risk_dev = 0  # The standard deviation of the noise added to the risk.
        self.risk_cont = 0  # The extra risk that gets added after each generation.

        # A measure for the intensity of selection
        self.beta = 1

        # The variables used in the noise generation process when evolving a generation.
        self.mu = 0.03
        self.sigma = 0.15

        # Interest on the common account
        self.interest = 0
