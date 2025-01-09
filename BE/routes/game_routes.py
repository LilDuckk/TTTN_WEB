from flask import Blueprint, jsonify, request
from models.game_state import GameState
from app import db

game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/state', methods=['GET'])
def get_game_state():
    state = GameState.query.first()
    if not state:
        return jsonify({'error': 'Game state not initialized.'}), 404
    return jsonify(state.__dict__)

@game_routes.route('/state', methods=['POST'])
def set_game_state():
    data = request.json
    state = GameState.query.first()
    if not state:
        state = GameState()
    state.current_turn = data.get('current_turn', state.current_turn)
    state.double_roll_count = data.get('double_roll_count', state.double_roll_count)
    db.session.add(state)
    db.session.commit()
    return jsonify(state.__dict__)