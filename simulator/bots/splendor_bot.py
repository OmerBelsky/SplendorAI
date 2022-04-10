from abc import abstractmethod

from simulator.actions.player_action import PlayerAction
from simulator.game_state import GameState
from splendor_ai.game.player import Player


class SplendorBot:
    def __init__(self, represented_player: Player):
        self._represented_player = represented_player

    @abstractmethod
    def turn(self, game_state: GameState) -> PlayerAction:
        raise NotImplementedError()

    @staticmethod
    def purchaseable_cards(game_state: GameState):
        cards_on_board = game_state.cards
        purchasing_power = game_state.player.purchasing_power
        affordable_cards = [card for card in cards_on_board if card.purchaseable_with(purchasing_power)]
        return affordable_cards
