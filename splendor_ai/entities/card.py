from dataclasses import dataclass
from typing import Dict

from splendor_ai.entities.gem_color import GemColor


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
