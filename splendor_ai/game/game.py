from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.board import Board
import numpy as np

class Game:

    def __init__(self, players):

        self.players = players
        self.num_players = len(players)
        # Make sure number of players is valid
        if self.num_players not in [2, 3, 4]:
            raise ValueError("Too many players. Player count should be an integer between 2 and 4.")

        # Define currency and nobles according to number of players
        self.board = Board(self.num_players)
        self.player_turn = 0

    def take_three_coins(self, player, coins_to_take, coins_to_return=None):

        if coins_to_return is None:
            coins_to_return = dict()

        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

        if sum(coins_to_take.values()) > 3:
            raise ValueError("At most 3 coins can be requested")

        if any([amnt > 1 for amnt in coins_to_take.values()]):
            raise ValueError("Coins requested must be unique")

        if not all([self.board.coins[color] > 0 for color in coins_to_take]):
            raise ValueError("One or more of the colors you requested is not available on the board")

        if not all([player.currency[color] >= amnt for color, amnt in coins_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if len(player.currency) + len(coins_to_take) - len(coins_to_return) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if GemColor.JOKER in coins_to_take:
            raise ValueError("Jokers can only be taken via mortgaging")

        for color in coins_to_take:
            player.currency[color] += 1
            self.board.coins[color] -= 1

        for color, amnt in coins_to_return.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self.player_turn = (self.player_turn + 1) % self.num_players

    def take_double_coins(self, player, coin_to_take, coins_to_return=None):
      
        if coins_to_return is None:
            coins_to_return = dict()

        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

        if self.board.coins[coin_to_take] < 4:
            raise ValueError("There aren't at least 4 coins from the color you requested")

        if not all([player.currency[color] >= amnt for color, amnt in coins_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if len(player.currency) + 2 - len(coins_to_return) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if GemColor.JOKER == coin_to_take:
            raise ValueError("Jokers can only be taken via mortgaging")

        player.currency[coin_to_take] += 2
        self.board.coins[coin_to_take] -= 2

        for color, amnt in coins_to_return.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self.player_turn = (self.player_turn + 1) % self.num_players

    def buy_card(self, player, level, idx, coins_to_pay):

        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

        if level not in [1, 2, 3]:
            raise ValueError("Card level must be an integer between 1 and 3")

        if idx not in [1, 2, 3, 4]:
            raise ValueError("Card index must be an integer between 1 and 4")

        if any([coins_to_pay[color] > player.currency[color] for color in coins_to_pay]):
            ValueError("You tried to pay with more coins than you own")

        requested_card = self.board.decks[level][idx - 1]
        diff_dict = {color: requested_card.price[color] - coins_to_pay[color] for color in self.board.coins}

        if any([diff_dict[color] < 0 for color in diff_dict]):
            raise ValueError("You over-payed a type of coin")

        if sum(diff_dict.values()) > coins_to_pay[GemColor.JOKER]:
            raise ValueError("You under-payed for the card")

        for color, amnt in coins_to_pay.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self.board.decks[level].pop(idx - 1)
        player.cards.append(requested_card)

        self.player_turn = (self.player_turn + 1) % self.num_players
