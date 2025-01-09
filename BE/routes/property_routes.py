from flask import Blueprint, jsonify, request
from models.property import Property
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