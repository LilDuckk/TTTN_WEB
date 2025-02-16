from app import db
from app.game.constants import STATUS_WAITING


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mode = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(16), nullable=False, default=STATUS_WAITING)
    isHost = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Game: code: {}, user_id: {}, id: {}>'.format(self.code, self.user_id, self.id)
