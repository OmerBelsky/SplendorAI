from splendor_ai.entities.gem_color import GemColor
from splendor_ai.constants import NOBLES, FULL_DECK
from splendor_ai.game.board import Board
from splendor_ai.game.errors import IncorrectNumPlayersError
import numpy as np

class Game:

    def __init__(self, num_players):

        # Make sure number of players is valid
        if num_players not in [2, 3, 4]:
            raise IncorrectNumPlayersError()

        # Define currency and nobles according to number of players

        self.board = Board(num_players)

