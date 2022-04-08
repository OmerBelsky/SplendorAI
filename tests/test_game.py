import pytest

from splendor_ai.game.game import Game
from splendor_ai.game.player import Player


def test_create_game_sanity():
    for i in [2, 3, 4]:
        players = [Player() for _ in range(i)]
        g = Game(players)
        assert g


def test_create_game_bad_player_count():
    players = [Player() for _ in range(5)]

    with pytest.raises(ValueError):
        g = Game(players)
