import os
from app import create_app, db, socketio
from app.game.utils import get_games_dir
from app.game.models import Game

app = create_app()

print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")

@app.cli.command('create_db')
def create_db():
    print("Creating database...")
    db.create_all()
    print("Database created.")

@app.cli.command('clear_saves')
def clear_saves():
    files = os.listdir(get_games_dir())
    for f in files:
        _, ext = os.path.splitext(f)
        if ext == '.pkl':
            os.remove(get_games_dir()+'/'+f)

    try:
        db.session.query(Game).delete()
        db.session.commit()
    except:
        db.session.rollback()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
