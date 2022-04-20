import neat
import os
from splendor_ai.game.player import Player
from splendor_ai.game.game import Game
from splendor_ai.entities.gem_color import GemColor
from splendor_ai.constants import ACTION_DICT, GEM_COLORS
import numpy as np
from time import time

def reward(action_str, player):
    # in order to save runtime calculates reward post action (assumes action was legal and has be executed.
    if action_str.startswith("buy3"):
        ret_coins = [color for color in action_str.split("ret")[1].split("_") if color != '']
        ret_coin_value = sum([(1.5 if color == GemColor.JOKER.value else 1) for color in ret_coins])
        return (3 - ret_coin_value) * 0.2
    elif action_str.startswith("buy2"):
        ret_coins = [color for color in action_str.split("ret")[1].split("_") if color != '']
        ret_coin_value = sum([(1.5 if color == GemColor.JOKER.value else 1) for color in ret_coins])
        return (2 - ret_coin_value) * 0.2
    elif action_str.startswith("buycard") or action_str.startswith("buymortgage"):
        return player.cards[-1].point_value
    elif action_str.startswith("mortgage"):
        coin_ret = action_str.split("_")[-1]
        card = player.mortgage_card[-1]
        turn_til_purchasable = max(max([card.price[color] - player.purchasing_power[color] for color in card.price]), 0)
        return card.point_value / (turn_til_purchasable + 1) + (0.1 if coin_ret == GemColor.JOKER.value else 0)


def play_tourney(genomes, nets):
    print("playing tourney")
    winners = []
    winner_nets = []
    for i, _ in enumerate(genomes[::4]):
        idx_start = i * 4
        player_genomes = {j: genomes[idx_start + j] for j in range(4)}
        players = [Player() for _ in player_genomes]
        game = Game(players)
        game_round = 0
        start_time = time()
        while (game_round <= 25) and (game.game_winner is None):
            curr_player = game.player_turn
            if curr_player == 0:
                print(f"round took {round(time() - start_time)} seconds")
                start_time = time()
                game_round += 1
            output = nets[idx_start + curr_player].activate(game.vectorized_state)
            ranked_actions = np.argsort(output)[::-1]
            action_taken = False
            for action_idx in ranked_actions:
                action = ACTION_DICT[action_idx]
                try:
                    if action.startswith("buy3"):
                        ret_coins = [GemColor(int(color)) for color in action.split("ret")[1].split("_") if color != '']
                        get_coins = [GemColor(int(color)) for color in action.split("ret")[0].split("_")[1:] if
                                     color != '']
                        game.take_three_coins(players[curr_player],
                                              {color: 1 if color in get_coins else 0 for color in GEM_COLORS},
                                              {color: sum([c == color for c in ret_coins]) for color in GEM_COLORS})
                    elif action.startswith("buy2"):
                        ret_coins = [GemColor(int(color)) for color in action.split("ret")[1].split("_") if color != '']
                        get_coins = GemColor(int(action.split("_")[1]))
                        game.take_double_coins(players[curr_player],
                                               get_coins,
                                               {color: sum([c == color for c in ret_coins]) for color in GEM_COLORS})
                    elif action.startswith("buycard"):
                        level, idx = map(int, action.split("_")[1:3])
                        if len(game.board.decks[level]) >= idx:
                            discounts = players[curr_player].discounts
                            card = game.board.decks[level][idx - 1]
                            joker_replacements = [GemColor(int(color)) for color in action.split("_")[3:] if color != '']
                            joker_replacements = {color: sum([color == rep for rep in joker_replacements]) for color in
                                                  GEM_COLORS}
                            payment = {color: max(price - discounts[color], 0) - joker_replacements[color] for color, price in card.price.items()}
                            payment[GemColor.JOKER] = sum(joker_replacements.values())
                            game.buy_deck_card(players[curr_player], level, idx, payment)
                        else:
                            raise ValueError("No cards to buy")
                    elif action.startswith("buymortgage"):
                        idx = int(action.split("_")[1])
                        if len(players[curr_player].mortgage_card) >= idx:
                            discounts = players[curr_player].discounts
                            card = players[curr_player].mortgage_card[idx - 1]
                            joker_replacements = [GemColor(int(color)) for color in action.split("_")[2:] if color != '']
                            joker_replacements = {color: sum([color == rep for rep in joker_replacements]) for color in
                                                  GEM_COLORS}
                            payment = {color: max(price - discounts[color], 0) - joker_replacements[color] for color, price in card.price.items()}
                            payment[GemColor.JOKER] = sum(joker_replacements.values())
                            game.buy_mortgaged_card(players[curr_player], idx, payment)
                        else:
                            raise ValueError("No cards to mortgage")
                    elif action.startswith("mortgage"):
                        level, idx, ret_coin = action.split("_")[1:]
                        level = int(level)
                        idx = int(idx)
                        game.mortgage_card(players[curr_player], level, idx,
                                           None if ret_coin == '' else GemColor(ret_coin))
                    player_genomes[curr_player][1].fitness += reward(action, players[curr_player])
                    action_taken = True
                    break
                except ValueError as e:
                    pass
            if not action_taken:
                raise Exception("no action was taken")
        if game.game_winner is not None:
            winners.append(player_genomes[game.game_winner])
            winner_nets.append(nets[idx_start + game.game_winner])
        else:
            most_points_player = max(player_genomes, key=lambda idx: players[idx].points)
            winners.append(player_genomes[most_points_player])
            winner_nets.append(nets[idx_start + most_points_player])
    return winners, winner_nets


def eval_genomes(genomes, config):
    nets = []
    print("creating nets")
    for i, (_, genome) in enumerate(genomes):
        start_time = time()
        genome.fitness = 0
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        print(f"creating net took {round(time() - start_time)} seconds")
    print("finished creating nets")
    winners1, winners1_nets = play_tourney(genomes, nets)
    winners2, winners2_nets = play_tourney(winners1, winners1_nets)
    play_tourney(winners2, winners2_nets)


def run(config):
    # Create the population, which is the top-level object for a NEAT run.
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
    print("creating population")
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    print("adding statistics")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run for up to 300 generations.
    print("evaluating genomes")
    winner = p.run(eval_genomes, 100)


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run(config)
