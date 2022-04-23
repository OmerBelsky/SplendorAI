from simulator.actions.purchase_card_action import PurchaseCardAction
from simulator.actions.take_coins_action import TakeCoinsAction
from simulator.bots.buy_alot_bot import BuyAlotBot
from simulator.game_state import GameState
from splendor_ai.game.game import Game
from splendor_ai.game.player import Player


def generate_games(count, player_count=4):
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
    winner = game.winner
    print(f"the winner is {winner} with {winner.points} points")


if __name__ == '__main__':
    generate_games(10)
