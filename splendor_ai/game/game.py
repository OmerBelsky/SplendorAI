from splendor_ai.entities.gem_color import GemColor
from splendor_ai.constants import NOBLES, FULL_DECK
from splendor_ai.game.board import Board
from splendor_ai.game.errors import IncorrectNumPlayersError
import numpy as np

class Game:

    def __init__(self, players):

        self.players = players
        self.num_players = len(players)
        # Make sure number of players is valid
        if self.num_players not in [2, 3, 4]:
            raise IncorrectNumPlayersError()

        # Define currency and nobles according to number of players
        self.board = Board(self.num_players)
        self.player_turn = 0

    def take_three_coins(self, player, colors, colors_to_return=None):

        if colors_to_return is None:
            colors_to_return = dict()

        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

        if sum(colors.values()) > 3:
            raise ValueError("At most 3 coins can be requested")

        if any([amnt > 1 for amnt in colors.values()]):
            raise ValueError("Coins requested must be unique")

        if not all([self.board.coins[color] > 0 for color in colors]):
            raise ValueError("One or more of the colors you requested is not available on the board")

        if not all([player.currency[color] >= amnt for color, amnt in colors_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if len(player.currency) + len(colors) - len(colors_to_return) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if GemColor.JOKER in colors:
            raise ValueError("Jokers can only be taken via mortgaging")

        for color in colors:
            player.currency[color] += 1
            self.board.coins[color] -= 1

        for color in colors_to_return:
            player.currency[color] -= 1
            self.board.coins[color] += 1

