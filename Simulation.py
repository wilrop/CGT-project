from Game import Game
from Player import Player


def play_game(game):
    """
    A helper function that will play the game.
    :param game: The game object that will be used to simulate a collective-risk dilemma.
    :return: Nothing as of right now. // TODO make it return something useful.
    """
    return 0


if __name__ == "__main__":
    # Declaring static variables.
    rounds = 10
    risk = 0.5  # Risk is represented as a probability.
    initial_endowment = 2 * rounds

    # Creating the players.
    num_players = 6
    players = [Player(initial_endowment) for x in range(rounds)]

    # Creating the game.
    game = Game(players, risk, rounds)

    # Play the created game.
    play_game()
