from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict

from simulator.actions.player_action import PlayerAction
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player


@dataclass
class TakeCoinsAction(PlayerAction):
    coins_taken: Dict[GemColor, int]
    coins_returned: Dict[GemColor, int] = field(default_factory=lambda: defaultdict(int))

    @staticmethod
    def from_str(representation: str, player: Player):
        ret_part, get_part = representation.split("ret")
        get_coins = [GemColor(int(color)) for color in ret_part.split("_") if color != '']
        ret_coins = [GemColor(int(color)) for color in get_part.split("_")[1:] if color != '']
        get_dict = defaultdict(int)
        ret_dict = defaultdict(int)

        for color in get_coins:
            get_dict[color] += 1

        for color in ret_coins:
            ret_dict[color] += 1

        return TakeCoinsAction(coins_taken=get_dict, coins_returned=ret_dict, player=player)
