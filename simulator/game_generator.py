from simulator.bots.buy_alot_bot import BuyAlotBot
from splendor_ai.game.game import Game


def generate_games(count, player_count=4):
    bots = [BuyAlotBot() for i in range(player_count)]

    game = Game()

if __name__ == '__main__':
    generate_games(10)