from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict

from simulator.actions.player_action import PlayerAction
from splendor_ai.entities.gem_color import GemColor


@dataclass
class TakeCoinsAction(PlayerAction):
    coins_taken: Dict[GemColor, int]
    coins_returned: Dict[GemColor, int] = field(default_factory=lambda: defaultdict(int))
