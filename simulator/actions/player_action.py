from dataclasses import dataclass

from splendor_ai.game.player import Player


@dataclass
class PlayerAction:
    player: Player
