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

    # Kiểm tra nếu người chơi đi qua ô "GO"
    if player.position > new_position:  # Đi qua "GO"
        player.money += 200  # Thêm $200 vào tài khoản người chơi

    player.position = new_position

    # Lấy thông tin ô từ bảng `Board`
    square = BoardSquare.query.get(new_position)

    # Xử lý tùy theo loại ô
    if square.type == 'START':
        player.money += 200  # Nếu dừng trực tiếp tại "GO", nhận thêm $200
        db.session.commit()
        return jsonify({'message': f'{player.name} collected $200 for landing on GO.', 'money': player.money})
    elif square.type == 'CITY':
        # Xử lý logic cho ô tài sản
        rent = json.loads(square.rent)['0']  # Tiền thuê cấp 0
        if square.price is None:  # Ô chưa có chủ sở hữu
            return jsonify({'message': f'{player.name} can buy {square.label}.'})
        else:
            player.pay(rent)
            db.session.commit()
            return jsonify({'message': f'{player.name} paid ${rent} rent.'})
    elif square.type == 'GOTO':
        player.position = 10  # Jail position
        player.jail = True
        db.session.commit()
        return jsonify({'message': f'{player.name} is sent to jail.'})
    
    elif square.type == 'CHANCE':
        # Rút lá bài từ bộ bài Chance
        card = Card.query.filter_by(type='Chance').first()
        if not card:
            return jsonify({'message': f'{player.name} landed on Chance but no cards are available.'}), 404

        # Thực hiện hành động từ lá bài
        action = card.action  # Giả định `action` chứa logic (vd: "advance_to_go")
        message = f'{player.name} drew a Chance card: {card.text}'
        
        # Hành động đặc biệt: ví dụ "Đi tới ô GO"
        if action == 'advance_to_go':
            player.position = 0
            player.money += 200
            message += " and moved to GO, collecting $200."

        # Xóa lá bài khỏi bộ bài sau khi rút
        db.session.delete(card)
        db.session.commit()
        return jsonify({'message': message})
    
    db.session.commit()
    return jsonify({'message': f'{player.name} moved to {square.label}.'})

