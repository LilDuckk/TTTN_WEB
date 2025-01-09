from flask import Blueprint, jsonify, request
from models.game_state import GameState
from models.player import Player
from models.property import Property
from models.board_square import BoardSquare
from models.card import Card
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

@game_routes.route('/move', methods=['POST'])
def move_player():
    data = request.json
    player_id = data['player_id']
    dice_roll = data['dice_roll']

    # Lấy thông tin người chơi
    player = Player.query.get_or_404(player_id)
    new_position = (player.position + sum(dice_roll)) % 40
    player.position = new_position

    # Lấy thông tin ô từ bảng Board
    square = BoardSquare.query.get(new_position)

    # Xử lý logic tùy theo loại ô
    if square.type == 'property':
        if not square.owner_id:
            return jsonify({'message': f'{player.name} can buy {square.name}.'})
        else:
            rent = square.rent
            player.pay(rent)
            owner = Player.query.get(square.owner_id)
            owner.receive(rent)
            return jsonify({'message': f'{player.name} paid ${rent} rent to {owner.name}.'})
    elif square.type == 'go_to_jail':
        player.position = 10  # Jail position
        player.jail = True
        db.session.commit()
        return jsonify({'message': f'{player.name} is sent to jail.'})
    elif square.type == 'start':
        player.money += 200
        db.session.commit()
        return jsonify({'message': f'{player.name} collected $200 for passing GO.'})
    elif square.type == 'chance':
        card = Card.query.filter_by(type='Chance').first()
        if card:
            return jsonify({'message': f'{player.name} drew a Chance card: {card.text}'})

    db.session.commit()
    return jsonify({'message': f'{player.name} moved to {square.name}.'})

