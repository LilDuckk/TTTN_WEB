from app import db

class BoardSquare(db.Model):
    __tablename__ = 'board'

    position = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(
        'start', 'property', 'chance', 'community_chest', 'tax', 
        'jail', 'go_to_jail', 'free_parking', 'other'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    rent = db.Column(db.Numeric(10, 2), nullable=True)
    group_id = db.Column(db.Integer, nullable=True)
    special_action = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<BoardSquare {self.name} (Position: {self.position})>'
