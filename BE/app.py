from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Cài đặt các thư viện cần thiết
#pip install flask flask-sqlalchemy flask-migrate mysqlclient
#Tạo database monôply_web trong MariaDB
#Khởi tạo database và migrations
#flask db init
#flask db migrate -m "Initial migration"
#flask db upgrade

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/monopoly_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models (used for migrations)
from models.player import Player
from models.property import Property
from models.auction import Auction
from models.trade import Trade
from models.card import Card
from models.game_state import GameState
from models.game import Game

# Import routes
from routes.player_routes import player_routes
from routes.property_routes import property_routes
from routes.auction_routes import auction_routes
from routes.trade_routes import trade_routes
from routes.card_routes import card_routes
from routes.game_routes import game_routes

# Register routes
app.register_blueprint(player_routes, url_prefix='/api/players')
app.register_blueprint(property_routes, url_prefix='/api/properties')
app.register_blueprint(auction_routes, url_prefix='/api/auctions')
app.register_blueprint(trade_routes, url_prefix='/api/trades')
app.register_blueprint(card_routes, url_prefix='/api/cards')
app.register_blueprint(game_routes, url_prefix='/api/game')

if __name__ == '__main__':
    app.run(debug=True)
