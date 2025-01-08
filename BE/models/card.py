from app import db

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('Chance', 'Community Chest'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    action = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Card {self.id}>'