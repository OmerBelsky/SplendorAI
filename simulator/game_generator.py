from simulator.bots.buy_alot_bot import BuyAlotBot
from simulator.game_state import GameState
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player


def generate_games(count, player_count=4):
    bots = [BuyAlotBot(Player()) for i in range(player_count)]

    game = Game(bots)
    while game.winner is None:
        for bot in bots:
            """
                player: Player
    other_players: List[Player] = field(default_factory=list)
    deck_one: List[Card] = field(default_factory=list)
    deck_two: List[Card] = field(default_factory=list)
    deck_three: List[Card] = field(default_factory=list)
    coins: Dict[GemColor, int] = field(default_factory=dict)
    """
            represented_player = bot._represented_player
            game_state = GameState(
                player=represented_player,
                other_players=[player for player in game.players if player is not represented_player],
                deck_one=game.board.decks[0],
                deck_two=game.board.decks[1],
                deck_three=game.board.decks[2],
                coins=game.board.coins
            )
            turn = bot.turn(game_state)
    winner = game.winner
    print(f"the winner is {winner} with {winner.points} points")


if __name__ == '__main__':
    generate_games(10)
