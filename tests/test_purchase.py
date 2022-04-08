import pytest

from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor


def test_card_purchaseable_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    assert card.purchaseable_with({color: 100 for color in GEM_COLORS})


def test_card_not_purchaseable_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    assert not card.purchaseable_with({color: 0 for color in GEM_COLORS})


def test_card_not_purchaseable_with_only_jokers_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=2,
        price_r=2,
        price_u=2,
        price_g=2,
        price_b=2,
    )
    assert card.purchaseable_with({GemColor.JOKER: 10})
