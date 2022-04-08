import pytest

from splendor_ai.constants import GEM_COLORS
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player
from splendor_ai.game.game import Game


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


def test_cant_buy_without_paying():
    players = [Player() for _ in range(4)]
    game = Game(players)
    with pytest.raises(ValueError):
        game.buy_deck_card(players[game.player_turn], 1, 1, {color: 0 for color in GEM_COLORS})

def test_cant_buy_with_coins_not_owned():
    players = [Player() for _ in range(4)]
    game = Game(players)
    with pytest.raises(ValueError):
        card = game.board.decks[1][1]
        game.buy_deck_card(players[game.player_turn], 1, 1, {color: card.price[color] for color in GEM_COLORS})

def test_card_purhcased():
    players = [Player() for _ in range(4)]
    game = Game(players)
    card = game.board.decks[2][0]
    for color in GEM_COLORS:
        players[0].currency[color] += 100
    game.buy_deck_card(players[game.player_turn], 2, 1, card.price)
    assert game.player_turn == 1
    assert card in players[0].cards
    assert players[0].discounts[card.gem_color] == 1
    assert players[0].points == card.point_value
    assert all([players[0].currency[color] == (100 - card.price[color]) for color in GEM_COLORS])
    assert card not in game.board.decks[2]
    assert all([game.board.coins[color] == (7 + card.price[color]) for color in GEM_COLORS])


