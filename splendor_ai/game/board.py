import itertools
import random
from collections import defaultdict
from typing import List, Dict, Iterable

from splendor_ai import constants
from splendor_ai.entities.card import Card
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.entities.noble import Noble


class Board:
    def __init__(self, num_players: int, cards: List[Card] = constants.FULL_DECK,
                 nobles: List[Noble] = constants.NOBLES):
        self.num_players = num_players
        num_nobles = num_players + 1
        nobles_selection = nobles.copy()
        random.shuffle(nobles_selection)
        self.nobles = nobles_selection[:num_nobles]

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
    def cards(self) -> Iterable[Card]:
        return itertools.chain(self.decks[1], self.decks[2], self.decks[3])

    @property
    def vectorized_state(self) -> List[int]:
        # vectorize the cards in the decks and in case deck is empty
        # append vectors of 0's
        vectorized_cards_level_1 = []
        vectorized_cards_level_2 = []
        vectorized_cards_level_3 = []
        for card in self.decks[1][:4]:
            vectorized_cards_level_1 += card.vectorized_state
        for card in self.decks[2][:4]:
            vectorized_cards_level_2 += card.vectorized_state
        for card in self.decks[3][:4]:
            vectorized_cards_level_3 += card.vectorized_state
        vectorized_cards_level_1 += [0] * 8 * (4 - len(self.decks[1][:4]))
        vectorized_cards_level_2 += [0] * 8 * (4 - len(self.decks[2][:4]))
        vectorized_cards_level_3 += [0] * 8 * (4 - len(self.decks[3][:4]))

        # vectorize nobles
        vectorized_nobles = []
        for noble in self.nobles:
            vectorized_nobles += noble.vectorized_state
        vectorized_nobles += [0] * 6 * (self.num_players + 1 - len(self.nobles))

        return [self.coins[GemColor.WHITE], self.coins[GemColor.RED], self.coins[GemColor.BLUE],
                self.coins[GemColor.GREEN], self.coins[GemColor.BLACK], self.coins[GemColor.JOKER]
                ] + vectorized_cards_level_1 + vectorized_cards_level_2 + vectorized_cards_level_3 + vectorized_nobles

    @property
    def open_cards(self) -> Iterable[Card]:
        return itertools.chain(self.decks[1][:4], self.decks[2][:4], self.decks[3][:4])
