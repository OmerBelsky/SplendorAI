from abc import ABC

from simulator.actions.purchase_card_action import PurchaseCardAction
from simulator.bots.splendor_bot import SplendorBot
from simulator.game_state import GameState
from splendor_ai.constants import GEM_COLORS


class BuyAlotBot(SplendorBot, ABC):
    def turn(self, game_state: GameState):
        purchaseable_cards = self.purchaseable_cards(game_state)
        if len(purchaseable_cards) > 0:
            card = purchaseable_cards[0]
            return PurchaseCardAction(player=game_state.player, card=card)

        coin_count = len(game_state.player.currency)
        if coin_count <= 7:
            for color in GEM_COLORS:
                game_state.coins
