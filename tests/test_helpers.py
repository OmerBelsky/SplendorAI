from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor


def get_cards(color: GemColor, discount: int):
    return [Card(
        level=0,
        gem_color=color,
        point_value=999,
        price_w=0,
        price_r=0,
        price_u=0,
        price_g=0,
        price_b=0)] * discount
