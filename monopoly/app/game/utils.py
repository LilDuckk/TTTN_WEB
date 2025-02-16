import os
import pickle
from typing import Union
from app.game.game import Game


def get_games_dir():
    return os.path.abspath(os.getcwd()) + '/app/game/save_files'


def delete_game(code: str):
    filename = get_games_dir() + '/{}.pkl'.format(code)
    os.remove(filename)


def save_game(game: Game, code: str) -> str:
    filename = get_games_dir() + '/{}.pkl'.format(code)

    with open(filename, 'wb') as f:
        pickle.dump(game, f, pickle.HIGHEST_PROTOCOL)

    return code


def load_game(code: str) -> Union[Game, None]:
    filename = get_games_dir() + '/{}.pkl'.format(code)
    try:
        f = open(filename, 'rb')
        g = pickle.load(f)
        f.close()
        return g
    except FileNotFoundError:
        return None
