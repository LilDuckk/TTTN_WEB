from flask import Blueprint, jsonify, request
from models.player import Player
from models.property import Property
from app import db

player_routes = Blueprint('player_routes', __name__)

@player_routes.route('/', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([player.__dict__ for player in players])

@player_routes.route('/', methods=['POST'])
def add_player():
    data = request.json
    new_player = Player(
        name=data['name'],
        color=data['color']
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player.__dict__), 201

@player_routes.route('/<int:player_id>/bankrupt', methods=['POST'])
def bankrupt_player(player_id):
    player = Player.query.get_or_404(player_id)

    # Chuyển tài sản của người chơi cho chủ nợ
    if player.creditor:
        creditor = Player.query.get(player.creditor)
        for property_ in Property.query.filter_by(owner_id=player_id).all():
            property_.owner_id = creditor.id
            db.session.commit()

    # Xóa người chơi khỏi trò chơi
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': f'Player {player_id} is bankrupt and removed from the game.'})