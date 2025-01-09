from flask import Blueprint, jsonify, request
from models.property import Property
from models.player import Player
from app import db

property_routes = Blueprint('property_routes', __name__)

@property_routes.route('/', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([prop.__dict__ for prop in properties])

@property_routes.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property_ = Property.query.get_or_404(property_id)
    return jsonify(property_.__dict__)

@property_routes.route('/', methods=['POST'])
def add_property():
    data = request.json
    new_property = Property(
        name=data['name'],
        color=data['color'],
        price=data['price'],
        baserent=data['baserent']
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify(new_property.__dict__), 201

@property_routes.route('/<int:property_id>/build', methods=['POST'])
def build_house(property_id):
    data = request.json
    player_id = data['player_id']
    property_ = Property.query.get_or_404(property_id)

    if property_.owner_id != player_id:
        return jsonify({'error': 'You do not own this property.'}), 403

    if property_.houses < 4:
        property_.houses += 1
        cost = property_.houseprice
    elif property_.houses == 4 and not property_.hotel:
        property_.hotel = True
        cost = property_.houseprice
    else:
        return jsonify({'error': 'Maximum houses and hotel already built.'}), 400

    player = Player.query.get(player_id)
    if not player.pay(cost):
        return jsonify({'error': 'Not enough money to build.'}), 400

    db.session.commit()
    return jsonify({'message': f'Built on {property_.name} successfully.'})
