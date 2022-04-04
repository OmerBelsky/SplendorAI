class IncorrectNumPlayersError(Exception):
    def __init__(self):
        self.message = "Too many players. Player count should be an integer between 2 and 4."