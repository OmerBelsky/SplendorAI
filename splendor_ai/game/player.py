from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.entities.noble import Noble


@dataclass
class Player:
    cards: List[Card] = field(default_factory=list)
    mortgage_card: List[Card] = field(default_factory=list)
    currency: Dict[GemColor, int] = field(default_factory=lambda: defaultdict(int))
    nobles: List[Noble] = field(default_factory=list)

    @property
    def points(self) -> int:
        return self.noble_points + self.card_points

    @property
    def noble_points(self) -> int:
        return sum([n.point_value for n in self.nobles])

    @property
    def card_points(self) -> int:
        return sum([c.point_value for c in self.cards])
