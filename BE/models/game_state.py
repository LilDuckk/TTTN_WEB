from app import db

class GameState(db.Model):
    __tablename__ = 'game_state'

    id = db.Column(db.Integer, primary_key=True)
    current_turn = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    double_roll_count = db.Column(db.Integer, default=0)
    auction_queue = db.Column(db.Text, nullable=True)  # JSON format
    chance_deck = db.Column(db.Text, nullable=True)
    community_chest_deck = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<GameState {self.id}>'