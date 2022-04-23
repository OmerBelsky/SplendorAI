from typing import Dict, Tuple, List

from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.board import Board
from splendor_ai.game.player import Player

WINNING_SCORE = 15


class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.num_players = len(players)
        # Make sure number of players is valid
        if self.num_players not in [2, 3, 4]:
            raise ValueError("Too many players. Player count should be an integer between 2 and 4.")

        # Define currency and nobles according to number of players
        self.board = Board(self.num_players)
        self.player_turn = 0
        self.game_winner = None

    @property
    def vectorized_state(self):
        player_order = [(self.player_turn + i) % self.num_players for i in range(self.num_players)]
        player_purchase_power_1 = {
            plyr: [max(max([card.price[color] - self.players[plyr].purchasing_power[color] for color in card.price]), 0)
                   for
                   card in self.board.decks[1][:4]] for plyr in player_order}
        player_purchase_power_2 = {
            plyr: [max(max([card.price[color] - self.players[plyr].purchasing_power[color] for color in card.price]), 0)
                   for
                   card in self.board.decks[2][:4]] for plyr in player_order}
        player_purchase_power_3 = {
            plyr: [max(max([card.price[color] - self.players[plyr].purchasing_power[color] for color in card.price]), 0)
                   for
                   card in self.board.decks[3][:4]] for plyr in player_order}
        player_purchase_power = {plyr: (player_purchase_power_1[plyr] + [0] * 4)[:4] +
                                       (player_purchase_power_2[plyr] + [0] * 4)[:4] +
                                       (player_purchase_power_3[plyr] + [0] * 4)[:4]
                                 for plyr in player_order}

        return sum([self.players[plyr].vectorized_state + player_purchase_power[plyr] for plyr in player_order], []) + \
               self.board.vectorized_state

    def _increment_player(self):
        if self.players[self.player_turn].points >= 15:
            self.game_winner = self.player_turn
            return
        self.player_turn = (self.player_turn + 1) % self.num_players

    def distribute_nobles(self, player: Player):
        player_colors = player.discounts

        obtainable_nobles = [all([player_colors[color] >= req
                                  for color, req in noble.requirements.items()])
                             for noble in self.board.nobles]

        nobles_indices = sorted([i for i, obtainable in enumerate(obtainable_nobles) if obtainable], reverse=True)

        for idx in nobles_indices:
            player.nobles.append(self.board.nobles.pop(idx))

    def take_coins(self, player: Player, coins_to_take: Dict[GemColor, int],
                   coins_to_return: Dict[GemColor, int] = None):
        if sum(coins_to_take.values()) == 2:
            for color, count in coins_to_take.items():
                if count == 2:
                    return self.take_double_coins(player, color, coins_to_return)
        return self.take_unique_coins(player, coins_to_take, coins_to_return)

    def _take_unique_coins_check(self, player: Player, coins_to_take: Dict[GemColor, int],
                                 coins_to_return: Dict[GemColor, int] = None):
        if coins_to_return is None:
            coins_to_return = dict()

        self._verify_player_turn(player)

        if sum(coins_to_take.values()) > 3:
            raise ValueError("Only less or equal to 3 coins can be requested")

        if sum(coins_to_take.values()) < sum(coins_to_return.values()):
            raise ValueError("You cant take less coins than you return")

        if any([amnt not in [0, 1] for amnt in coins_to_take.values()]):
            raise ValueError("Coins requested must be unique")

        if any([amnt < 0 for amnt in coins_to_return.values()]):
            raise ValueError("Coins returned must be a non negative integer")

        if not all([self.board.coins[color] > 0 for color in coins_to_take if
                    (coins_to_take[color] - coins_to_return.get(color, 0)) > 0]):
            raise ValueError("One or more of the colors you requested is not available on the board")

        if not all([(player.currency.get(color, 0) + coins_to_take.get(color, 0)) >= amnt for color, amnt in
                    coins_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if player.total_currency + sum(coins_to_take.values()) - sum(coins_to_return.values()) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if sum(coins_to_return.values()) > 0:  # if returning coins (taking less than 3)
            if player.total_currency + sum(coins_to_take.values()) - sum(
                    coins_to_return.values()) < 10:  # if it brings you to less than 10 coins
                existing_colors = [color for color in GEM_COLORS if self.board.coins[color] > 0]
                if len(existing_colors) >= 3:  # if there are enough colors to choose 3 of.
                    raise ValueError("Attempted to return coins even though total is brought to less than 10.")
                else:
                    for color, amnt in coins_to_return.items():
                        if amnt > 0:
                            if (self.board.coins[color] == 0) and (coins_to_take.get(color, 0) == amnt):
                                pass
                            else:
                                raise ValueError(
                                    "Attempted to return coins even though total is brought to less than 10.")

        if GemColor.JOKER in coins_to_take:
            raise ValueError("Jokers can only be taken via mortgaging")

        return True

    def take_unique_coins(self, player, coins_to_take: Dict[GemColor, int],
                          coins_to_return: Dict[GemColor, int] = None):
        if coins_to_return is None:
            coins_to_return = dict()

        self._take_unique_coins_check(player, coins_to_take, coins_to_return)

        for color, amnt in coins_to_take.items():
            player.currency[color] += amnt
            self.board.coins[color] -= amnt

        for color, amnt in coins_to_return.items():
            player.currency[color] -= amnt
            self.board.coins[color] += amnt

        self._increment_player()

    def _take_double_coins_check(self, player, coin_to_take: GemColor, coins_to_return: Dict[GemColor, int]):
        if coins_to_return is None:
            coins_to_return = dict()

        self._verify_player_turn(player)

        if self.board.coins[coin_to_take] < 4:
            raise ValueError("There aren't at least 4 coins from the color you requested")

        if any([amnt < 0 for amnt in coins_to_return.values()]):
            raise ValueError("Coins returned must be a non negative integer")

        if not all([(player.currency[color] + (2 if color == coin_to_take else 0)) >= amnt for color, amnt in
                    coins_to_return.items()]):
            raise ValueError("You do no own one or more of the colors you tried to return")

        if player.total_currency + 2 - sum(coins_to_return.values()) > 10:
            raise ValueError("Your action brings you to more than 10 coins")

        if sum(coins_to_return.values()) > 0:
            if player.total_currency + 2 - sum(coins_to_return.values()) <= 10:
                raise ValueError("Attempted to return coins even though total is brought to less than 10.")

        if GemColor.JOKER == coin_to_take:
            raise ValueError("Jokers can only be taken via mortgaging")

        return True

    def take_double_coins(self, player, coin_to_take: GemColor, coins_to_return: Dict[GemColor, int] = None):

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

        if any([payment < 0 for payment in coins_to_pay.values()]):
            raise ValueError("Coins payed must be a non negative integer")

        discounts = player.discounts
        requested_card = self.board.decks[level][idx - 1]
        diff_dict = {
            color: max(requested_card.price.get(color, 0) - discounts.get(color, 0), 0) - coins_to_pay.get(color, 0)
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
        self.distribute_nobles(player)
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

        if any([payment < 0 for payment in coins_to_pay.values()]):
            raise ValueError("Coins payed must be a non negative integer")

        discounts = player.discounts

        requested_card = player.mortgage_card[idx - 1]
        diff_dict = {
            color: max(requested_card.price.get(color, 0) - discounts.get(color, 0), 0) - coins_to_pay.get(color, 0)
            for color in GEM_COLORS}

        if any([diff_dict[color] < 0 for color in diff_dict]):
            raise ValueError("You over-payed a type of coin")

        if sum(diff_dict.values()) != coins_to_pay.get(GemColor.JOKER, 0):
            raise ValueError("You didn't include enough jokers for the purchase")

        return True

    def buy_mortgaged_card(self, player, idx, coins_to_pay):
        self._buy_mortgaged_card_check(player, idx, coins_to_pay)
        self._buy_card(player, player.mortgage_card.pop(idx - 1), coins_to_pay)

    def _mortgage_card_check(self, player, level, idx, coin_to_return):
        self._verify_player_turn(player)
        self._verify_card_exists(level, idx)

        if len(player.mortgage_card) == 3:
            raise ValueError("Player already has 3 cards mortgaged")

        if coin_to_return is None and player.total_currency == 10:
            raise ValueError("If you take a joker coin you must return another coin")

        return True

    def mortgage_card(self, player, level, idx, coin_to_return=None):
        self._mortgage_card_check(player, level, idx, coin_to_return)

        requested_card = self.board.decks[level].pop(idx - 1)
        player.mortgage_card.append(requested_card)

        if self.board.coins[GemColor.JOKER] > 0:
            player.currency[GemColor.JOKER] += 1
            self.board.coins[GemColor.JOKER] -= 1
            if player.total_currency == 11:
                player.currency[coin_to_return] -= 1
                self.board.coins[coin_to_return] += 1

        self._increment_player()

    @property
    def winner(self) -> Player:
        for player in self.players:
            if player.points >= WINNING_SCORE:
                return player

    def card_to_level_index(self, card) -> Tuple[int, int]:
        for deck_index, deck in self.board.decks.items():
            for card_index, deck_card in enumerate(deck):
                if card is deck_card:
                    return deck_index, card_index + 1

        raise ValueError("Card not in deck")
