from dataclasses import dataclass
from typing import Dict

from simulator.actions.player_action import PlayerAction
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor


@dataclass
class PurchaseCardAction(PlayerAction):
    card: Card
    payment: Dict[GemColor, int]
