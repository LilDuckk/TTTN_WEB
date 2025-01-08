from flask import Blueprint, jsonify

property_routes = Blueprint('property_routes', __name__)

# Danh sách tài sản tạm thời
properties = []

@property_routes.route('/', methods=['GET'])
def get_properties():
    return jsonify([prop.__dict__ for prop in properties])
