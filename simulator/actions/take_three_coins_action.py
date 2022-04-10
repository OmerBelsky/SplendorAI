from dataclasses import dataclass

from simulator.actions.player_action import PlayerAction


@dataclass
class TakeThreeCoinsAction(PlayerAction):
    white_coins: int
    red_coins: int
    black_coins: int
    green_coins: int
    blue_coins: int
