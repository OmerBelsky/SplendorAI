from typing import Dict

from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.board import Board
from splendor_ai.game.player import Player

WINNING_SCORE = 15


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

    def _increment_player(self):
        self.player_turn = (self.player_turn + 1) % self.num_players

    def distribute_nobles(self, player):
        player_colors = {color: sum([color == card.gem_color for card in player.cards])
                         for color in self.board.coins}

        obtainable_nobles = [all([player_colors[color] >= req
                                  for color, req in enumerate(noble.requirements)])
                             for noble in self.board._nobles]

        nobles_indices = sorted([i for i, obtainable in enumerate(obtainable_nobles) if obtainable], reverse=True)

        for idx in nobles_indices:
            player.nobles.append(self.board._nobles.pop[idx])

    def _take_three_coins_check(self, player, coins_to_take, coins_to_return=None):
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

        return True

    def take_three_coins(self, player, coins_to_take, coins_to_return=None):
        if coins_to_return is None:
            coins_to_return = dict()

        self._take_three_coins_check(player, coins_to_take, coins_to_return)

        for color in coins_to_take:
            player.currency[color] += 1
            self.board.coins[color] -= 1

        for color, amnt in coins_to_return.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self._increment_player()

    def _take_double_coins_check(self, player, coin_to_take, coins_to_return):
        if coins_to_return is None:
            coins_to_return = dict()

        self._verify_player_turn(player)

        if self.board.coins[coin_to_take] < 4:
            raise ValueError("There aren't at least 4 coins from the color you requested")

        if not all([player.currency[color] >= amnt for color, amnt in coins_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if len(player.currency) + 2 - len(coins_to_return) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if GemColor.JOKER == coin_to_take:
            raise ValueError("Jokers can only be taken via mortgaging")

        return True

    def take_double_coins(self, player, coin_to_take, coins_to_return=None):

        if coins_to_return is None:
            coins_to_return = dict()

        self._take_double_coins_check(player, coin_to_take, coins_to_return)

        player.currency[coin_to_take] += 2
        self.board.coins[coin_to_take] -= 2

        for color, amnt in coins_to_return.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self._increment_player()

    def _verify_card_exists(self, level, idx):
        if level not in [1, 2, 3]:
            raise ValueError("Card level must be an integer between 1 and 3")

        if idx not in [1, 2, 3, 4]:
            raise ValueError("Card index must be an integer between 1 and 4")

        if len(self.board.decks[level]) < idx:
            raise ValueError("There is no card in this position")

    def _verify_player_turn(self, player: Player):
        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

    def _buy_deck_card_check(self, player: Player, level: int, idx: int, coins_to_pay: Dict[GemColor, int]):
        self._verify_player_turn(player)
        self._verify_card_exists(level, idx)

        if any([coins_to_pay[color] > player.currency[color] for color in coins_to_pay]):
            raise ValueError("You tried to pay with more coins than you own")

        discounts = player.discounts
        requested_card = self.board.decks[level][idx - 1]
        diff_dict = {color: max(requested_card.price[color] - discounts[color], 0) - coins_to_pay.get(color, 0)
                     for color in GEM_COLORS}

        if any([diff_dict[color] < 0 for color in diff_dict]):
            raise ValueError("You over-payed a type of coin")

        if sum(diff_dict.values()) != coins_to_pay.get(GemColor.JOKER, 0):
            raise ValueError("You didn't include enough jokers for the purchase")

        return True

    def _buy_card(self, player, card, coins_to_pay):
        for color, amnt in coins_to_pay.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        player.cards.append(card)

        self._increment_player()

    def buy_deck_card(self, player, level, idx, coins_to_pay):
        self._buy_deck_card_check(player, level, idx, coins_to_pay)
        self._buy_card(player, self.board.decks[level].pop(idx - 1), coins_to_pay)

    def _buy_mortgaged_card_check(self, player, idx, coins_to_pay):
        self._verify_player_turn(player)

        if idx not in [1, 2, 3]:
            raise ValueError("Card index must be an integer between 1 and 3")

        if len(player.mortgage_card) < idx:
            raise ValueError("There is no card in this position")

        if any([coins_to_pay[color] > player.currency[color] for color in coins_to_pay]):
            raise ValueError("You tried to pay with more coins than you own")

        discounts = {color: sum([color == card.gem_color for card in player.cards]) for color in GEM_COLORS}

        requested_card = player.mortgage_card[idx - 1]
        diff_dict = {color: max(requested_card.price[color] - discounts[color], 0) - coins_to_pay.get(color, 0)
                     for color in GEM_COLORS}

        if any([diff_dict[color] < 0 for color in diff_dict]):
            raise ValueError("You over-payed a type of coin")

        if sum(diff_dict.values()) != coins_to_pay.get(GemColor.JOKER, 0):
            raise ValueError("You didn't include enough jokers for the purchase")

        return True

    def _buy_mortgaged_card(self, player, idx, coins_to_pay):
        self._buy_mortgaged_card_check(player, idx, coins_to_pay)
        self._buy_card(player, player.mortgage_card.pop(idx - 1), coins_to_pay)

    def _mortgage_card_check(self, player, level, idx, coin_to_return):

        if player != self.players[self.player_turn]:
            raise ValueError("It isn't this players turn")

        if level not in [1, 2, 3]:
            raise ValueError("Card level must be an integer between 1 and 3")

        if idx not in [1, 2, 3, 4]:
            raise ValueError("Card index must be an integer between 1 and 4")

        if len(self.board.decks[level]) < idx:
            raise ValueError("There is no card in this position")

        if len(player.mortgage_card) == 3:
            raise ValueError("Player already has 3 cards mortgaged")

        if coin_to_return is None and len(player.currency) == 10:
            raise ValueError("If you take a joker coin you must return another coin")

        return True

    def mortgage_card(self, player, level, idx, coin_to_return=None):

        self._mortgage_card_check(player, level, idx, coin_to_return)

        requested_card = self.board.decks[level].pop(idx - 1)
        player.mortgage_card.append(requested_card)

        if self.board.coins[GemColor.JOKER] > 0:
            player.currency[GemColor.JOKER] += 1
            self.board.coins[GemColor.JOKER] -= 1
            if len(player.currency) == 11:
                player.currency[coin_to_return] -= 1
                self.board.coins[coin_to_return] += 1

        self._increment_player()

    @property
    def winner(self) -> Player:
        for player in self.players:
            if player.points >= WINNING_SCORE:
                return player
