import random
from collections import defaultdict
from typing import Dict, Tuple, List

from simulator.game_state import GameState
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player
from splendor_ai.constants import GEM_COLORS


def get_purchaseable_cards(game_state: GameState) -> List[Card]:
    cards_on_board = game_state.open_cards
    purchasing_power = game_state.player.purchasing_power
    affordable_cards = [card for card in cards_on_board if card_purchaseable_with(card, purchasing_power)]
    return affordable_cards


def get_payment_for_card(player: Player, card: Card):
    payment = defaultdict(int)
    purchasing_power = player.purchasing_power
    jokers_remaining = purchasing_power.get(GemColor.JOKER, 0)
    price = card.price
    assert card_purchaseable_with(card, purchasing_power)

    for color in GEM_COLORS:
        required_coins = price.get(color, 0) - player.discounts.get(color, 0)
        if required_coins <= 0:
            continue

        player_coins_of_color = player.currency.get(color, 0)
        after_purchase = player_coins_of_color - required_coins
        if after_purchase < 0:
            payment[color] = player_coins_of_color
            remaining_payment = abs(after_purchase)
            assert jokers_remaining > remaining_payment
            jokers_remaining -= remaining_payment
            payment[GemColor.JOKER] += remaining_payment
        else:
            payment[color] = required_coins
    return payment


def card_purchaseable_with(card: Card, purchasing_power: Dict[GemColor, int]) -> bool:
    jokers_remaining = purchasing_power.get(GemColor.JOKER, 0)
    price = card.price
    for color in GEM_COLORS:
        after_purchase = purchasing_power.get(color, 0) - price[color]
        if after_purchase < 0:
            jokers_remaining += after_purchase

    return jokers_remaining >= 0


def get_random_currency(coins: Dict[GemColor, int], count: int, must_be_unique: bool,
                        ignore_colors: List[GemColor] = None) -> Tuple[Dict[GemColor, int], int]:
    taken = defaultdict(int)
    if ignore_colors is None:
        coins_colors = coins.keys()
    else:
        coins_colors = [color for color in coins.keys() if color not in ignore_colors]

    for coin_color in sorted(coins_colors, key=lambda _: random.random()):
        coins_of_color = coins[coin_color]
        for i in range(coins_of_color):
            taken[coin_color] += 1
            count -= 1
            if count == 0:
                return taken, 0
            if must_be_unique:
                break
    return taken, count
