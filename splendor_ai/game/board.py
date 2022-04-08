import itertools
import random
from collections import defaultdict
from typing import List

from splendor_ai import constants
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.entities.noble import Noble


class Board:
    def __init__(self, num_players: int, cards: List[Card] = constants.FULL_DECK,
                 nobles: List[Noble] = constants.NOBLES):
        num_nobles = num_players + 1
        nobles_selection = nobles.copy()
        random.shuffle(nobles_selection)
        self._nobles = nobles_selection[:num_nobles]

        cards_selection = cards.copy()
        random.shuffle(cards_selection)
        self.decks = defaultdict(list)
        for card in cards:
            self.decks[card.level].append(card)

        players_to_coins = {4: 7, 3: 5, 2: 4}
        num_coins = players_to_coins[num_players]

        self.coins = {
            GemColor.WHITE: num_coins,
            GemColor.RED: num_coins,
            GemColor.GREEN: num_coins,
            GemColor.BLUE: num_coins,
            GemColor.BLACK: num_coins,
            GemColor.JOKER: 5
        }

    @property
    def cards(self):
        return itertools.chain(self.decks[1], self.decks[2], self.decks[3])
