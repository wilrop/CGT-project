class Player:
    """
    A class that represents a player in our collective-risk dilemma.
    """
    def __init__(self, coins):
        self.balance = coins

    def choose_action(self):
        return 0