from flask import Blueprint, jsonify, request
from models.player import Player
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