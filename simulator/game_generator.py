from simulator.actions.purchase_card_action import PurchaseCardAction
from simulator.actions.take_coins_action import TakeCoinsAction
from simulator.bots.buy_alot_bot import BuyAlotBot
from simulator.game_state import GameState
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player
from timeit import default_timer as timer


def generate_games(player_count=4, suppress_logs=False):
    bots = [BuyAlotBot(Player()) for i in range(player_count)]

    game = Game([bot._represented_player for bot in bots])
    while game.winner is None:
        for bot in bots:
            represented_player = bot._represented_player
            game_state = GameState(
                player=represented_player,
                other_players=[player for player in game.players if player is not represented_player],
                open_cards=game.board.open_cards,
                coins=game.board.coins
            )
            action = bot.turn(game_state)
            if not suppress_logs:
                print(f"action: {action}")
            if isinstance(action, PurchaseCardAction):
                level, index = game.card_to_level_index(card=action.card)
                game.buy_deck_card(action.player, level, index, action.payment)
            elif isinstance(action, TakeCoinsAction):
                game.take_coins(action.player, action.coins_taken, action.coins_returned)
            else:
                raise ValueError("Unknown action")
            if game.winner is not None:
                break
    return game.winner


if __name__ == '__main__':
    times = []
    for i in range(10):
        start = timer()
        winner = generate_games(suppress_logs=True)
        end = timer()
        elapsed = end - start
        times.append(elapsed)
        print(f"time for game: {elapsed}")  # Time in seconds, e.g. 5.38091952400282
        print("------------------------------------")
        print(f"the winner of game with {winner.points} points is {winner}")
    print(f"avg time for game: {sum(times) / len(times)}")
