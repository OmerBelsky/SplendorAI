from dataclasses import dataclass
from typing import Dict

from simulator.actions.player_action import PlayerAction
from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player


@dataclass
class PurchaseCardAction(PlayerAction):
    card: Card
    payment: Dict[GemColor, int]

    @staticmethod
    def from_str(representation: str, player: Player, game: Game):
        level, idx = map(int, representation.split("_")[1:3])
        card = game.board.decks[level][idx - 1]
        discounts = player.discounts
        joker_replacements = [GemColor(int(color)) for color in representation.split("_")[3:] if color != '']
        joker_replacements = {color: sum([color == rep for rep in joker_replacements]) for color in
                              GEM_COLORS}
        payment = {color: max(price - discounts[color], 0) - joker_replacements[color] for color, price
                   in card.price.items()}
        payment[GemColor.JOKER] = sum(joker_replacements.values())

        return PurchaseCardAction(player=player, card=card, payment=payment)
