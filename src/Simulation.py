from src.BuildSimulation import BuildSimulation
from src.Generation import Generation


def run_simulation(setup):
    """
    A helper function that will run the simulation.
    :param setup: An object containing al variables that will be used in the simulation.
    :return: Nothing as of now. TODO make it return something useful.
    """

    for i in range(setup.num_generations):
        print("Generation " + str(i))
        generation = Generation(setup)
        generation.play()
        generation.calculate_fitness()

    return 0


if __name__ == "__main__":
    # Declaring variables that are used in the evolutionary game.
    setup = BuildSimulation()

    # Running the simulation.
    run_simulation(setup)
