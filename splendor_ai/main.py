from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.board import Board
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player
from splendor_ai.constants import GEM_COLORS
from itertools import product

if __name__ == '__main__':
    # generate buy 3 return any actions
    actions = []
    for i, color1 in enumerate(GEM_COLORS):
        for j, color2 in enumerate(GEM_COLORS[i + 1: ], i + 1):
            for color3 in GEM_COLORS[j + 1:]:
                for a, color_ret1 in enumerate(GEM_COLORS + ['']):
                    if color_ret1 != '':
                        color_ret1 = color_ret1.value
                    for b, color_ret2 in enumerate(GEM_COLORS[a + 1:] + [''], a + 1):
                        if color_ret2 != '':
                            color_ret2 = color_ret2.value
                        for color_ret3 in GEM_COLORS[b + 1:] + ['']:
                            if color_ret3 != '':
                                color_ret3 = color_ret3.value
                            actions.append(f"buy3_{color1}_{color2}_{color3}_ret_{color_ret1}_{color_ret2}_{color_ret3}")
    set_form_action = [(set(action.split("ret")[0].split("_")[1: -1]), set(action.split("ret")[1].split("_")[1:])) for
                       action in actions if action.startswith("buy3")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))

    # generate buy 2 return any actions
    for color in GEM_COLORS:
        for a, color_ret1 in enumerate(GEM_COLORS + ['']):
            if color_ret1 != '':
                color_ret1 = color_ret1.value
            for b, color_ret2 in enumerate(GEM_COLORS[a + 1:] + [''], a + 1):
                if color_ret2 != '':
                    color_ret2 = color_ret2.value
                for color_ret3 in GEM_COLORS[b + 1:] + ['']:
                    if color_ret3 != '':
                        color_ret3 = color_ret3.value
                    actions.append(f"buy2_{color}_ret_{color_ret1}_{color_ret2}_{color_ret3}")
    set_form_action = [(set(action.split("ret")[0].split("_")[1: -1]), set(action.split("ret")[1].split("_")[1:])) for
                       action in actions if action.startswith("buy2")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))

    # generate buy cards from board
    # string will be formatted buycard_level_idx_<colors to be replaced with jokers>
    for level in [1, 2, 3]:
        for idx in [1, 2, 3, 4]:
            for a, joker_c1 in enumerate(GEM_COLORS + ['']):
                if joker_c1 != '':
                    joker_c1 = joker_c1.value
                for b, joker_c2 in enumerate(GEM_COLORS[a + 1:] + [''], a + 1):
                    if joker_c2 != '':
                        joker_c2 = joker_c2.value
                    for c, joker_c3 in enumerate(GEM_COLORS[b + 1:] + [''], b + 1):
                        if joker_c3 != '':
                            joker_c3 = joker_c3.value
                        for d, joker_c4 in enumerate(GEM_COLORS[c + 1:] + [''], c + 1):
                            if joker_c4 != '':
                                joker_c4 = joker_c4.value
                            for joker_c5 in GEM_COLORS[d + 1:] + ['']:
                                if joker_c5 != '':
                                    joker_c5 = joker_c5.value
                                actions.append(f"buycard_{level}_{idx}_{joker_c1}_{joker_c2}_{joker_c3}_{joker_c4}_{joker_c5}")
    set_form_action = [(action.split("_")[1], action.split("_")[2], set(action.split("_")[3:])) for action in actions if
                       action.startswith("buycard")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))

    # generate buy cards from mortgage
    for idx in [1, 2, 3]:
        for a, joker_c1 in enumerate(GEM_COLORS + ['']):
            if joker_c1 != '':
                joker_c1 = joker_c1.value
            for b, joker_c2 in enumerate(GEM_COLORS[a + 1:] + [''], a + 1):
                if joker_c2 != '':
                    joker_c2 = joker_c2.value
                for c, joker_c3 in enumerate(GEM_COLORS[b + 1:] + [''], b + 1):
                    if joker_c3 != '':
                        joker_c3 = joker_c3.value
                    for d, joker_c4 in enumerate(GEM_COLORS[c + 1:] + [''], c + 1):
                        if joker_c4 != '':
                            joker_c4 = joker_c4.value
                        for joker_c5 in GEM_COLORS[d + 1:] + ['']:
                            if joker_c5 != '':
                                joker_c5 = joker_c5.value
                            actions.append(f"buymortgage_{idx}_{joker_c1}_{joker_c2}_{joker_c3}_{joker_c4}_{joker_c5}")
    set_form_action = [(action.split("_")[1], set(action.split("_")[2:])) for action in actions if
                       action.startswith("buymortgage")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))
    print(len(actions))
    print("{")
    for i, action in enumerate(actions):
        print(str(i) + ": '" + str(action) + "',")
    print("}")

