import neat
import os
from splendor_ai.game.player import Player
from splendor_ai.game.game import Game
from splendor_ai.constants import ACTION_DICT

def eval_genomes(genomes, config):
    for genome in genomes:
        genome.fitness = 0
    for i, _ in enumerate(genomes[::4]):
        idx_start = i * 4
        player_genomes ={j: genomes[idx_start + j] for j in range(4)}
        players = [Player() for _ in player_genomes]
        game = Game(players)
        nets = {(idx_start + j): neat.nn.FeedForwardNetwork.create(genome, config) for j, genome in
                player_genomes.items()}






def run(config):
    # Create the population, which is the top-level object for a NEAT run.
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 100)


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
