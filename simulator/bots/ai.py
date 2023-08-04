from abc import ABC

from simulator.bots.splendor_bot import SplendorBot
from simulator.game_state import GameState


class AiBot(SplendorBot, ABC):
    net: object
    def turn(self, game_state: GameState):