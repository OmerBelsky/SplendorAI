from abc import ABC
from collections import defaultdict

from simulator.actions.purchase_card_action import PurchaseCardAction
from simulator.actions.take_coins_action import TakeCoinsAction
from simulator.bots.splendor_bot import SplendorBot
from simulator.game_state import GameState
from simulator.utils import get_payment_for_card, get_purchaseable_cards
from splendor_ai.constants import GEM_COLORS


class BuyAlotBot(SplendorBot, ABC):
    def turn(self, game_state: GameState):
        purchaseable_cards = get_purchaseable_cards(game_state)
        if len(purchaseable_cards) > 0:
            card = purchaseable_cards[0]
            payment = get_payment_for_card(player=game_state.player, card=card)
            return PurchaseCardAction(player=game_state.player, card=card, payment=payment)

        coin_count = len(game_state.player.currency)
        if coin_count <= 7:
            coins_taken = defaultdict(int)
            return TakeCoinsAction(player=game_state.player, coins_taken=coins_taken)
