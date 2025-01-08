from flask import Blueprint, jsonify
from models.game import Game

game_routes = Blueprint('game_routes', __name__)

game = Game()

@game_routes.route('/roll', methods=['GET'])
def roll_dice():
    dice = game.roll_dice()
    return jsonify({'die1': dice[0], 'die2': dice[1]})

@game_routes.route('/next', methods=['POST'])
def next_turn():
    game.next_turn()
    return jsonify({'current_turn': game.current_turn})
