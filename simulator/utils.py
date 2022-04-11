from collections import defaultdict
from typing import Dict

from simulator.game_state import GameState
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player
from splendor_ai.constants import GEM_COLORS


def get_purchaseable_cards(game_state: GameState):
    cards_on_board = game_state.cards
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
        player_coins_of_color = purchasing_power.get(color, 0)
        after_purchase = player_coins_of_color - price[color]
        if after_purchase < 0:
            payment[color] = player_coins_of_color
            remaining_payment = abs(after_purchase)
            assert jokers_remaining > remaining_payment
            jokers_remaining -= remaining_payment
            payment[GemColor.JOKER] += remaining_payment
        else:
            payment[color] = price[color]
    return payment


def card_purchaseable_with(card: Card, purchasing_power: Dict[GemColor, int]) -> bool:
    jokers_remaining = purchasing_power.get(GemColor.JOKER, 0)
    price = card.price
    for color in GEM_COLORS:
        after_purchase = purchasing_power.get(color, 0) - price[color]
        if after_purchase < 0:
            jokers_remaining += after_purchase

    return jokers_remaining >= 0
