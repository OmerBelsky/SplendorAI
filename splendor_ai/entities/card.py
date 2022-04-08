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

    def purchaseable_with(self, purchasing_power: Dict[GemColor, int]) -> bool:
        from splendor_ai.constants import GEM_COLORS
        # to avoid import loop
        jokers_remaining = purchasing_power.get(GemColor.JOKER, 0)
        price = self.price
        for color in GEM_COLORS:
            after_purchase = purchasing_power.get(color, 0) - price[color]
            if after_purchase < 0:
                jokers_remaining += after_purchase

        return jokers_remaining >= 0
