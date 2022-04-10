from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

from splendor_ai.constants import GEM_COLORS
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

    @property
    def discounts(self) -> Dict[GemColor, int]:
        return {
            color: sum([color == card.gem_color for card in self.cards])
            for color in GEM_COLORS
        }

    @property
    def purchasing_power(self) -> Dict[GemColor, int]:
        combined_colors = dict()
        discounts = self.discounts
        for color in GEM_COLORS:
            combined_colors[color] = self.currency[color] + discounts[color]
        combined_colors[GemColor.JOKER] = self.currency[GemColor.JOKER]

        return combined_colors

    @property
    def vectorized_state(self) -> List[int]:
        # cache
        discounts = self.discounts

        # vectorize mortgaged cards and add 0's in non-existent cards
        vectorized_mortgaged_cards = []
        for card in self.mortgage_card:
            vectorized_mortgaged_cards += card.vectorized_state
        vectorized_mortgaged_cards += [0] * 8 * (3 - len(self.mortgage_card))

        return [self.points, discounts[GemColor.WHITE], discounts[GemColor.RED],
                discounts[GemColor.BLUE], discounts[GemColor.GREEN], discounts[GemColor.BLACK],
                self.currency[GemColor.WHITE], self.currency[GemColor.RED],
                self.currency[GemColor.BLUE], self.currency[GemColor.GREEN],
                self.currency[GemColor.BLACK]] + vectorized_mortgaged_cards

