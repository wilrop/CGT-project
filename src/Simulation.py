from src.Generation import Generation


def run_simulation(num_generations, num_games, num_rounds, num_players, population_size, initial_endowment, legal_moves, risk):
    """
    A helper function that will run the simulation.
    :param num_generations: The amount of generations we want to run.
    :param num_games: The amount of games per generation.
    :param num_rounds: The amount of rounds per game.
    :param num_players: The amount of players that play a game.
    :param population_size: The total population size.
    :param initial_endowment: The initial endowment for all players in the generation.
    :param legal_moves: The different moves a player can make.
    :param risk: The risk of losing what you have not invested, when failing the game.
    :return: Nothing as of now. TODO make it return something useful.
    """
    for i in range(num_generations):
        generation = Generation(num_games, population_size, num_players, initial_endowment, legal_moves)
        generation.play(num_rounds, risk)

    return 0


if __name__ == "__main__":
    # Declaring static variables.
    num_generations = 10 ^ 4
    num_games = 10 ^ 3
    num_rounds = 10
    num_players = 6
    population_size = 100
    initial_endowment = 2 * num_rounds
    legal_moves = [0, 1, 2]
    risk = 0.5  # Risk is represented as a probability.

    # Running the simulation.
    run_simulation(num_generations, num_games, num_rounds, num_players, population_size, initial_endowment, legal_moves, risk)
