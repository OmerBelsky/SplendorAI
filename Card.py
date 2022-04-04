from enum import Enum

class Gem(Enum):
    WHITE = 1
    RED = 2
    BLUE = 3
    GREEN = 4
    BLACK = 5

class Card:

    def __init__(self, level, gem_color, point_value, price_w, price_r, price_u, price_g, price_b):
        self._level = level
        self._gem_color = gem_color
        self._point_value = point_value
        self._price = {Gem.WHITE: price_w,
                      Gem.RED: price_r,
                      Gem.BLUE: price_u,
                      Gem.GREEN: price_g,
                      Gem.BLACK: price_b}
    
    @property
    def price(self):
        return self._price

    @property
    def gem_color(self):
        return self._gem_color
    
    @property
    def level(self):
        return self._level

    @property
    def point_value(self):
        return self._point_value