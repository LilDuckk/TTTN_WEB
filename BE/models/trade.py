from app import db

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    initiator = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    money_offer = db.Column(db.Numeric(10, 2), default=0.00)
    money_request = db.Column(db.Numeric(10, 2), default=0.00)
    properties_offer = db.Column(db.Text, nullable=True)  # JSON format
    properties_request = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending')

    def __repr__(self):
        return f'<Trade {self.id}>'