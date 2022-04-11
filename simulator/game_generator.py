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
                deck_one=game.board.decks[0],
                deck_two=game.board.decks[1],
                deck_three=game.board.decks[2],
                coins=game.board.coins
            )
            action = bot.turn(game_state)
            print(f"action: {action}")
            if isinstance(action, PurchaseCardAction):
                level, index = game.card_to_level_index(card=action.card)
                game.buy_deck_card(action.player, level, index, action.payment)
            if isinstance(action, TakeCoinsAction):
                coins_taken = sum(action.coins_taken.values())
                if coins_taken == 2:
                    game.take_double_coins(action.player, action.coins_taken, action.coins_returned)
                if coins_taken == 3:
                    game.take_three_coins(action.player, action.coins_taken, action.coins_returned)
                raise ValueError(f"Illegal TakeCoinsAction amount {coins_taken}")
    winner = game.winner
    print(f"the winner is {winner} with {winner.points} points")


if __name__ == '__main__':
    generate_games(10)
