from secrets import token_hex
from turtle import goto
from flask import Blueprint, render_template, flash, redirect, url_for, request, make_response
from flask_login import current_user
from flask_socketio import emit, join_room, send
from app import db, socketio
from app.game.game import Game
from app.game.utils import save_game, load_game, delete_game
from app.game.models import Game as GameModel
from app.game.constants import HOT_SEATS_MODE, PVP_MODE, STATUS_ACTIVE, STATUS_FINISHED, PVAI_MODE
from app.game.fields import FIELDS
from app.game.ai import ai_move
from app.game.forms import JoinGameForm
from app.models import User

game = Blueprint('game', __name__)


@game.route('/')
def home():
    users_count = User.query.count()
    return render_template('game/home.html', users_count=users_count)


@game.route('/menu')
def menu():
    return render_template('game/menu.html')


@game.route('/hot_seats')
@game.route('/hot_seats/<code>', methods=['POST', 'GET'])
def hot_seats(code=None):
    payload = {
        'buy': bool(int(request.form.get('buy'))) if request.form.get('buy') else None,
        'build': request.form.get('build').split(';')[0:-1] if request.form.get('build') else None
    }
    if code:
        if request.form.get('next_turn'):
            g = load_game(code)
            g.next_turn(payload)
            if g.winner:
                game_in_db = GameModel.query.filter_by(code=code).first()
                game_in_db.status = STATUS_FINISHED
                db.session.commit()
                delete_game(code)

                flash('player {} have won!!'.format(g.winner.id), 'success')
                return redirect(url_for('game.home'))
            save_game(g, code)
        else:
            g = load_game(code)
    else:
        code = token_hex(16)
        g = Game(2)
        g.next_turn(payload)
        save_game(g, code)

        game_in_db = GameModel(code=code, user_id=current_user.id, mode=HOT_SEATS_MODE, status=STATUS_ACTIVE)
        db.session.add(game_in_db)
        db.session.commit()

    return render_template('game/board/board.html', game=g, code=code)


@game.route('/field_info/<field_id>')
def field_info(field_id):
    field_id = int(field_id)
    field_data = None
    for field in FIELDS:
        if field['id'] == field_id:
            field_data = field

    if not field_data:
        return make_response('not found'), 404

    return make_response(field_data), 200


@game.route('/vs_ai')
@game.route('/vs_ai/<code>', methods=['POST', 'GET'])
def vs_ai(code=None):
    payload = {
        'buy': bool(int(request.form.get('buy'))) if request.form.get('buy') else None,
        'build': request.form.get('build').split(';')[0:-1] if request.form.get('build') else None
    }
    if code:
        if request.form.get('next_turn'):
            g = load_game(code)
            g.next_turn(payload)
            ai_payload = ai_move(g)
            g.next_turn(ai_payload)
            if g.winner:
                game_record = GameModel.query.filter_by(code=code).first()
                game_record.status = STATUS_FINISHED
                db.session.commit()
                delete_game(code)
                flash('player {} have won!!'.format(g.winner.id), 'success')
                return redirect(url_for('game.home'))
            save_game(g, code)
        else:
            g = load_game(code)
    else:
        code = token_hex(16)
        g = Game(2)
        g.next_turn(payload)
        save_game(g, code)

        game_in_db = GameModel(code=code, user_id=current_user.id, mode=PVAI_MODE, status=STATUS_ACTIVE)
        db.session.add(game_in_db)
        db.session.commit()

    return render_template('game/board/board.html', game=g, code=code)


@game.route('/init_pvp')
def init_pvp():
    code = token_hex(16)
    g = Game(2, current_user.id)
    save_game(g, code)

    game_record = GameModel(code=code, user_id=current_user.id, mode=PVP_MODE, isHost=True)
    db.session.add(game_record)
    db.session.commit()

    return redirect(url_for('game.waiting_room', code=code))


@game.route('/waiting_room/<code>', methods=['POST', 'GET'])
def waiting_room(code):
    if request.method == 'POST':
        partner_has_joined: bool = bool(GameModel.query.filter_by(code=code, isHost=False).first())
        print(partner_has_joined)
        if partner_has_joined:
            game_record = GameModel.query.filter_by(code=code, isHost=True).first()
            game_record.status = STATUS_ACTIVE
            db.session.commit()
            return redirect(url_for('game.play_pvp', code=code))
        else:
            flash('You can not start the game, no player has joined.', 'danger')

    return render_template('game/waiting_room.html', code=code, is_host=True)


@game.route('/join_game', methods=['POST', 'GET'])
def join_game():
    form = JoinGameForm()
    if form.validate_on_submit():
        code = form.join_code.data
        game_records_count = GameModel.query.filter_by(code=code).count()
        if game_records_count == 1:
            g = load_game(code)
            g.pvp_add_joining_player(current_user.id)
            save_game(g, code)

            new_game_record = GameModel(code=code, user_id=current_user.id, mode=PVP_MODE)
            db.session.add(new_game_record)
            db.session.commit()
            return redirect(url_for('game.guest_waiting_room', code=code))
        else:
            flash('you can not join this game.', 'danger')

    return render_template('game/join_game.html', form=form)


@game.route('/guest_waiting_room/<code>', methods=['POST', 'GET'])
def guest_waiting_room(code):
    if request.method == 'POST':
        game_record = GameModel.query.filter_by(code=code, isHost=True).first()
        if game_record.status == STATUS_ACTIVE:
            return redirect(url_for('game.play_pvp', code=code))

    flash('now, wait for host to start the game.', 'primary')
    return render_template('game/waiting_room.html', is_host=False)


@game.route('/play_pvp/<code>', methods=['POST', 'GET'])
def play_pvp(code):
    payload = {
        'buy': bool(int(request.form.get('buy'))) if request.form.get('buy') else None,
        'build': request.form.get('build').split(';')[0:-1] if request.form.get('build') else None
    }
    g = load_game(code)
    if g.winner:
        socketio.emit('gameover', data={'msg': '{} won.'.format('You have' if current_user.id == g.winner.db_id else 'Enemy has')})
        flash('{} won.'.format('Enemy has' if current_user.id == g.winner.db_id else 'You have'))
        return redirect(url_for('game.home'))
    if request.form.get('next_turn'):
        last_player = g.players[g.current_player_index].db_id
        g.next_turn(payload)
        if g.winner:
            save_game(g, code)
            game_record = GameModel.query.filter_by(code=code, isHost=True)
            game_record.status = STATUS_FINISHED
            db.session.commit()
            socketio.emit('gameover', data={'msg': '{} won.'.format('You have' if current_user.id == g.winner.db_id else 'Enemy has')})
            flash('{} won.'.format('Enemy has' if current_user.id == g.winner.db_id else 'You have'))
            return redirect(url_for('game.home'))
        save_game(g, code)
        socketio.emit('refresh', data={'last_player': last_player}, broadcast=True)

    is_active = current_user.id == g.players[g.current_player_index].db_id

    return render_template(
        'game/board/board.html',
        game=g, code=code,
        pvp=True,
        is_active=is_active
        )


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

    send('', room=room)
