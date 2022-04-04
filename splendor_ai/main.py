from splendor_ai.entities.gem_color import GemColor
from splendor_ai.game.player import Player

if __name__ == '__main__':
    player = Player()
    player.currency[GemColor.BLACK] += 1
    print(player)
