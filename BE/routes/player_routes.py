from flask import Blueprint, jsonify, request
from models.player import Player

player_routes = Blueprint('player_routes', __name__)

# Danh sách người chơi tạm thời
players = []

@player_routes.route('/', methods=['GET'])
def get_players():
    return jsonify([player.__dict__ for player in players])

@player_routes.route('/', methods=['POST'])
def add_player():
    data = request.json
    player = Player(
        id=len(players) + 1,
        name=data['name'],
        color=data['color']
    )
    players.append(player)
    return jsonify(player.__dict__), 201
