from dataclasses import field, dataclass
from typing import List, Dict

from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player


@dataclass
class GameState:
    player: Player
    other_players: List[Player] = field(default_factory=list)
    cards: List[Card] = field(default_factory=list)
    coins: Dict[GemColor, int] = field(default_factory=dict)
