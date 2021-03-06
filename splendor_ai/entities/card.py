from dataclasses import dataclass
from typing import Dict, List

from splendor_ai.entities.gem_color import GemColor

CARD_VECTOR_SIZE = 12


@dataclass
class Card:
    level: int
    gem_color: GemColor
    point_value: int
    price_w: int
    price_r: int
    price_u: int
    price_g: int
    price_b: int

    @property
    def price(self) -> Dict[GemColor, int]:
        return {
            GemColor.WHITE: self.price_w,
            GemColor.RED: self.price_r,
            GemColor.BLUE: self.price_u,
            GemColor.GREEN: self.price_g,
            GemColor.BLACK: self.price_b
        }

    @property
    def vectorized_state(self) -> List[int]:
        from splendor_ai.constants import GEM_COLORS
        return [color == self.gem_color for color in GEM_COLORS] + [self.level, self.point_value, self.price_w,
                                                                    self.price_r, self.price_u, self.price_g,
                                                                    self.price_b]
