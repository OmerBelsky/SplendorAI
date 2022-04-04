from splendor_ai.entities.gem_color import GemColor
from splendor_ai.constants import NOBLES, FULL_DECK
from splendor_ai.game.errors import IncorrectNumPlayersError
import numpy as np

class Game:

    def __init__(self, num_players):

        # Make sure number of players is valid
        if num_players not in [2, 3, 4]:
            raise IncorrectNumPlayersError()

        # Define currency and nobles according to number of players
        num_nobles = num_players + 1
        if num_players == 4:
            num_coins = 7
        elif num_players == 3:
            num_coins = 5
        elif num_players == 2:
            num_coins = 4

        # Initialize game parameters
        self.coins = {GemColor.WHITE: num_coins, GemColor.RED: num_coins,
                      GemColor.GREEN: num_coins, GemColor.BLUE: num_coins,
                      GemColor.BLACK: num_coins, GemColor.JOKER: 5}
        self.deck = FULL_DECK
        self.nobles = NOBLES

        # Shuffle deck and nobles
        self.random_seed = np.random.randint(0, 10000000)
        np.random.shuffle(self.deck)
        np.random.shuffle(self.nobles)
        self.nobles = self.nobles[:num_nobles]

