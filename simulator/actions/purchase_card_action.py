from dataclasses import dataclass

from simulator.actions.player_action import PlayerAction
from splendor_ai.entities.card import Card


@dataclass
class PurchaseCardAction(PlayerAction):
    card: Card
