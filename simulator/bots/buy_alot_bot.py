from abc import ABC
from collections import defaultdict

from simulator.actions.purchase_card_action import PurchaseCardAction
from simulator.actions.take_coins_action import TakeCoinsAction
from simulator.bots.splendor_bot import SplendorBot
from simulator.game_state import GameState
from simulator.utils import get_payment_for_card, get_purchaseable_cards, get_random_currency
from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.gem_color import GemColor


class BuyAlotBot(SplendorBot, ABC):
    def turn(self, game_state: GameState):
        purchaseable_cards = get_purchaseable_cards(game_state)
        if len(purchaseable_cards) > 0:
            card = purchaseable_cards[0]
            payment = get_payment_for_card(player=game_state.player, card=card)
            return PurchaseCardAction(player=game_state.player, card=card, payment=payment)

        coin_count = len(game_state.player.currency)
        remaining_coins_until_three = min((10 - coin_count), 3)
        coins_taken, remaining_count = get_random_currency(
            game_state.coins,
            remaining_coins_until_three,
            must_be_unique=True,
            ignore_colors=[GemColor.JOKER]
        )
        coins_returned = defaultdict(int)
        if remaining_count > 0:
            coins_returned, cant_return = get_random_currency(
                game_state.player.currency,
                remaining_count,
                must_be_unique=False
            )
            if cant_return > 0:
                raise ValueError(f"cant return board: {game_state.coins} and player: {game_state.player.currency}")
        return TakeCoinsAction(player=game_state.player, coins_taken=coins_taken, coins_returned=coins_returned)
