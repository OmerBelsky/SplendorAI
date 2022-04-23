import pytest

from simulator import utils
from splendor_ai.constants import GEM_COLORS, GEM_COLORS_INCL_JOKER
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player
from tests.test_helpers import get_cards

UNLIMITED_MONEY = {color: 999 for color in GEM_COLORS_INCL_JOKER}


def test_card_purchasable_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    assert utils.card_purchaseable_with(card, {color: 100 for color in GEM_COLORS})


def test_card_not_purchasable_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    assert not utils.card_purchaseable_with(card, {color: 0 for color in GEM_COLORS})


def test_card_not_purchasable_with_only_jokers_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=2,
        price_r=2,
        price_u=2,
        price_g=2,
        price_b=2,
    )
    assert utils.card_purchaseable_with(card, {GemColor.JOKER: 10})


def test_purchase_get_payment_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    player = Player(currency=UNLIMITED_MONEY)
    payment = utils.get_payment_for_card(player, card)
    assert payment[GemColor.WHITE] == 1
    assert payment[GemColor.RED] == 2
    assert payment[GemColor.BLUE] == 3
    assert payment[GemColor.GREEN] == 4
    assert payment[GemColor.BLACK] == 5


def test_purchase_get_payment_discount_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=1,
        price_r=2,
        price_u=3,
        price_g=4,
        price_b=5,
    )
    discounts = get_cards(GemColor.WHITE, 1) + get_cards(GemColor.RED, 2) + get_cards(GemColor.BLUE, 3) + get_cards(
        GemColor.GREEN, 4) + get_cards(GemColor.BLACK, 5)
    player = Player(cards=discounts)
    payment = utils.get_payment_for_card(player, card)
    assert sum(payment.values()) == 0


def test_purchase_get_payment_discount_sanity():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=0,
        price_r=100,
        price_u=0,
        price_g=0,
        price_b=0,
    )
    player = Player(currency=UNLIMITED_MONEY, cards=get_cards(GemColor.RED, 40))
    payment = utils.get_payment_for_card(player, card)
    assert sum(payment.values()) == 60
    assert payment[GemColor.RED] == 60


def test_purchase_get_payment_discount_double():
    card = Card(
        level=999, gem_color=GemColor.WHITE, point_value=999,
        price_w=0,
        price_r=100,
        price_u=50,
        price_g=0,
        price_b=0,
    )
    player = Player(currency=UNLIMITED_MONEY, cards=get_cards(GemColor.RED, 40) + get_cards(GemColor.BLUE, 20))
    payment = utils.get_payment_for_card(player, card)
    assert sum(payment.values()) == 60 + 30
    assert payment[GemColor.RED] == 60
    assert payment[GemColor.BLUE] == 30
