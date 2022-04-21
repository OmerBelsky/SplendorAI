from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.board import Board
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player
from splendor_ai.constants import GEM_COLORS
from itertools import product

if __name__ == '__main__':
    action = "buy3_2_3_4_ret_2_3_4"
    ret_coins = [GemColor(int(color)) for color in action.split("ret")[1].split("_") if color != '']
    get_coins = [GemColor(int(color)) for color in action.split("ret")[0].split("_")[1:] if
                 color != '']
    ret = {color: sum([c == color for c in ret_coins]) for color in GEM_COLORS}
    players = [Player() for _ in range(4)]
    game = Game(players)
    rgu = {color: 1 if color in get_coins else 0 for color in GEM_COLORS}
    print(rgu)
    wgu = {GemColor.WHITE: 1, GemColor.GREEN: 1, GemColor.BLUE: 1}
    wg = {GemColor.BLUE: 1, GemColor.GREEN: 1}
    game.take_three_coins(players[0], rgu)
    print(game.board.coins)
    game.take_three_coins(players[1], rgu)
    print(game.board.coins)
    game.take_three_coins(players[2], rgu)
    print(game.board.coins)
    game.take_three_coins(players[3], rgu)
    print(game.board.coins)
    game.take_three_coins(players[0], rgu)
    game.take_three_coins(players[1], rgu)
    game.take_three_coins(players[2], rgu)
    game.mortgage_card(players[3], 1, 1)
    print(game.board.coins)
    game.take_double_coins(players[0], GemColor.BLACK)
    game.mortgage_card(players[1], 1, 1)
    game.mortgage_card(players[2], 1, 1)
    game.mortgage_card(players[3], 1, 1)
    # game.mortgage_card(players[0], 1, 1)
    game.take_double_coins(players[0], GemColor.BLACK)
    game.mortgage_card(players[1], 1, 1)
    game.mortgage_card(players[2], 1, 1)
    game.mortgage_card(players[3], 1, 1)
    game.take_three_coins(players[0], rgu, ret)
    print(game.board.coins)
    for player in players:
        print("-----------")
        print(player.currency)
    exit()
    # print(len(game.vectorized_state))
    # exit()
    # generate buy 3 return any actions
    actions = []
    GEM_COLORS_WITH_JOKER = GEM_COLORS + [GemColor.JOKER]
    color_quintuples = set([tuple(sorted(x, key=lambda x: x.value)) for x in
                            product(GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER,
                                    GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER)])
    unique_quintuples = [quintuple for quintuple in color_quintuples if len(quintuple) == len(set(quintuple))]
    color_quadruples = set([tuple(sorted(x, key=lambda x: x.value)) for x in
                            product(GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER,
                                    GEM_COLORS_WITH_JOKER)])
    unique_quadruples = [quadruple for quadruple in color_quadruples if len(quadruple) == len(set(quadruple))]
    color_triplets = set([tuple(sorted(x, key=lambda x: x.value)) for x in
                          product(GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER)])
    unique_triplets = [triplet for triplet in color_triplets if len(triplet) == len(set(triplet))]
    color_duos = set(
        [tuple(sorted(x, key=lambda x: x.value)) for x in product(GEM_COLORS_WITH_JOKER, GEM_COLORS_WITH_JOKER)])
    unique_duos = [duo for duo in color_duos if len(duo) == len(set(duo))]

    for buy_triplet, return_triplet in product(unique_triplets, color_triplets):
        if GemColor.JOKER not in buy_triplet:
            buy_string = f"{buy_triplet[0].value}_{buy_triplet[1].value}_{buy_triplet[2].value}"
            ret_string = f"{return_triplet[0].value}_{return_triplet[1].value}_{return_triplet[2].value}"
            actions.append(f"buy3_{buy_string}_ret_{ret_string}")
    for buy_triplet, return_duo in product(unique_triplets, color_duos):
        if GemColor.JOKER not in buy_triplet:
            buy_string = f"{buy_triplet[0].value}_{buy_triplet[1].value}_{buy_triplet[2].value}"
            ret_string = f"{return_duo[0].value}_{return_duo[1].value}_"
            actions.append(f"buy3_{buy_string}_ret_{ret_string}")
    for buy_triplet, return_color in product(unique_triplets, GEM_COLORS_WITH_JOKER):
        if GemColor.JOKER not in buy_triplet:
            buy_string = f"{buy_triplet[0].value}_{buy_triplet[1].value}_{buy_triplet[2].value}"
            ret_string = f"{return_color.value}__"
            actions.append(f"buy3_{buy_string}_ret_{ret_string}")
    for buy_triplet in unique_triplets:
        if GemColor.JOKER not in buy_triplet:
            buy_string = f"{buy_triplet[0].value}_{buy_triplet[1].value}_{buy_triplet[2].value}"
            actions.append(f"buy3_{buy_string}_ret___")
    set_form_action = [(set(action.split("ret")[0].split("_")[1: -1]), set(action.split("ret")[1].split("_")[1:])) for
                       action in actions if action.startswith("buy3")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))


    # generate buy 2 return any actions
    for buy_color, return_duo in product(GEM_COLORS, color_duos):
        actions.append(f"buy2_{buy_color.value}_ret_{return_duo[0].value}_{return_duo[1].value}")
    for buy_color, return_color in product(GEM_COLORS, GEM_COLORS_WITH_JOKER):
        actions.append(f"buy2_{buy_color.value}_ret_{return_color.value}_")
    for buy_color in GEM_COLORS:
        actions.append(f"buy2_{buy_color.value}_ret__")
    set_form_action = [(set(action.split("ret")[0].split("_")[1]), set(action.split("ret")[1].split("_")[1:])) for
                       action in actions if action.startswith("buy2")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))

    # generate buy cards from board
    # string will be formatted buycard_level_idx_<colors to be replaced with jokers>
    for level in [1, 2, 3]:
        for idx in [1, 2, 3, 4]:
            for triplet in color_triplets:
                actions.append(f"buycard_{level}_{idx}_{triplet[0].value}_{triplet[1].value}_{triplet[2].value}__")
            for duo in color_duos:
                actions.append(f"buycard_{level}_{idx}_{duo[0].value}_{duo[1].value}___")
            for color in GEM_COLORS_WITH_JOKER:
                actions.append(f"buycard_{level}_{idx}_{color.value}____")
            actions.append(f"buycard_{level}_{idx}_____")
    set_form_action = [(action.split("_")[1], action.split("_")[2], set(action.split("_")[3:])) for action in actions if
                       action.startswith("buycard")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))

    # generate buy cards from mortgage
    for idx in [1, 2, 3]:
        for triplet in color_triplets:
            actions.append(f"buymortgage_{idx}_{triplet[0].value}_{triplet[1].value}_{triplet[2].value}__")
        for duo in color_duos:
            actions.append(f"buymortgage_{idx}_{duo[0].value}_{duo[1].value}___")
        for color in GEM_COLORS_WITH_JOKER:
            actions.append(f"buymortgage_{idx}_{color.value}____")
        actions.append(f"buymortgage_{idx}_____")
    set_form_action = [(action.split("_")[1], set(action.split("_")[2:])) for action in actions if
                       action.startswith("buymortgage")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))
    # generate mortgage cards
    for level in [1, 2, 3]:
        for idx in [1, 2, 3, 4]:
            for a, color_ret1 in enumerate(GEM_COLORS_WITH_JOKER + ['']):
                if color_ret1 != '':
                    color_ret1 = color_ret1.value
                actions.append(f"mortgage_{level}_{idx}_{color_ret1}")
    set_form_action = [(action.split("_")[1], action.split("_")[2], action.split("_")[3]) for action in actions if
                       action.startswith("mortgage")]
    print(any([set_form in set_form_action[i + 1:] for i, set_form in enumerate(set_form_action)]))
    print(len(actions))
    print("{")
    for i, action in enumerate(actions):
        print(str(i) + ": '" + str(action) + "',")
    print("}")

