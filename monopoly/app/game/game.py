from typing import Union
from random import randint, choice
from app.game.fields import *
from app.game.surprises import SURPRISES
from app.auth.models import User

class Player:
    colors = ['#ED553B', '#F6B55C', '#3CAEA3', '#20639B']

    def __init__(self, pid: int, username: str = None):
        self.money = 3000
        self.current_field_id = 0
        self.id = pid
        self.username = username
        self.owned_fields = []
        self.color = self.colors[self.id]
        self.db_id = None
        self.in_jail = False
        self.jail_turns = 0

    def display_name(self):
        return f'<span style="color: {self.color};">{self.username if self.username else f"Người chơi {self.id}"}</span>'

    def move(self, steps: int):
        if self.in_jail:
            if self.jail_turns < 2 and steps != 12:
                self.jail_turns += 1
                return '{} đang ở trong tù'.format(self.display_name())
            elif steps == 12:
                self.in_jail = False
                self.jail_turns = 0
                return '{} đã thoát khỏi tù bằng cách xúc xắc ra 12'.format(self.display_name())
            else:
                return '{} đang ở trong tù'.format(self.display_name())

        old_field_index = self.current_field_id
        if self.current_field_id + steps > len(FIELDS) - 1:
            self.current_field_id = self.current_field_id - len(FIELDS) - 2 + steps
        else:
            self.current_field_id += steps
        print(self.current_field_id)

        new_field_index = self.current_field_id
        if new_field_index < old_field_index:
            self.money += 300


class PlaceholderField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']

    def on_enter(self, player: Player, game):
        return '{} đã đi vào ô {}'.format(player.display_name(), self.label)

class PowerplantField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']
        self.owner = None
        self.price = 300

    def on_enter(self, player: Player, game):
        if not self.owner and player.money > self.price:
            game.can_buy = True
            return '{} có thể mua ô {}'.format(player.display_name(), self.label)
        if self.owner and self.owner != player:
            powerplants_count = len([f for f in self.owner.owned_fields if f.type == POWERPLANT])
            price = 10 * randint(2, 12)
            if powerplants_count > 1:
                price = price * 2
            player.money -= price
            self.owner.money += price
            return '{} vừa trả {}$ cho {}'.format(player.display_name(), price, self.owner.display_name())
        return '{} đã đi vào ô {}'.format(player.display_name(), self.label)

class TrainField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']
        self.owner = None
        self.price = 400

    def on_enter(self, player: Player, game):
        if not self.owner and player.money > self.price:
            game.can_buy = True
            return '{} có thể mua ô {}'.format(player.display_name(), self.label)
        if self.owner and self.owner != player:
            trains_count = len([f for f in self.owner.owned_fields if f.type == TRAIN])
            price = 50
            for _ in range(trains_count - 1):
                price = price * 2
            player.money -= price
            self.owner.money += price
            return '{} vừa trả {}$ cho {}'.format(player.display_name(), price, self.owner.display_name())
        return '{} đã đi vào ô {}'.format(player.display_name(), self.label)

class SurpriseField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']

    def on_enter(self, player: Player, game):
        return choice(SURPRISES)(player)

class FineField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']

    def on_enter(self, player: Player, game):
        player.money -= 300
        return '{} bị phạt 300$'.format(player.display_name())

class CityField:
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.label = data['label']
        self.price = data['price']
        self.build_price = data['build_price']
        self.pricing = data['pricing']
        self.owner = None
        self.build = '0'

    def on_enter(self, player: Player, game):
        if not self.owner and player.money > self.price:
            game.can_buy = True
        if self.owner and self.owner != player:
            price = self.pricing[self.build]
            player.money -= price
            self.owner.money += price
        return '{} đã đi vào ô {}'.format(player.display_name(), self.label)

class GotoField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']

    def on_enter(self, player: Player, game):
        player.current_field_id = next(field.id for field in game.board if field.type == PRISON)
        player.in_jail = True
        return '{} đã bị chuyển đến tù'.format(player.display_name())

class JailField:
    def __init__(self, data):
        self.id = data['id']
        self.label = data['label']
        self.type = data['type']

    def on_enter(self, player: Player, game):
        if player.in_jail:
            return '{} đang ở trong tù'.format(player.display_name())
        return '{} đã đi vào ô {}'.format(player.display_name(), self.label)

class Game:
    def __init__(self, players_count: int, db_id: int = None):
        self.players = []
        self.current_player_index = 0
        self.board = []
        self.msgs = []
        self.can_buy = False
        self.winner = None

        for i, _ in enumerate(range(players_count)):
            if i == 0 and db_id:
                user = User.query.get(db_id)
                p = Player(i, username=user.username)
                p.db_id = db_id
            else:
                p = Player(i)
            self.players.append(p)

        self._render_board()

    def pvp_add_joining_player(self, db_id: int):
        for p in self.players:
            if p.db_id:
                continue
            else:
                user = User.query.get(db_id)
                p.db_id = db_id
                p.username = user.username
                break

    def next_turn(self, payload):
        
        if payload['buy']:
            self._sell_field(self.players[self.current_player_index],
                             self.board[self.players[self.current_player_index].current_field_id])
        if payload['build']:
            print(payload['build'])
            for field_id in payload['build']:
                self._updated_field_build(field_id)
        
        self._next_player()
        move = randint(2, 12)
        player = self.players[self.current_player_index]
        self._add_message('{} xúc xắc ra {}'.format(player.display_name(), move))
        if player.in_jail == True:
            if payload['pay_to_get_out'] == '1':
                self.pay_to_get_out_of_jail()
            else:
                msg = player.move(move)
        else:
            msg = player.move(move)
        if not msg:
            msg = self.board[player.current_field_id].on_enter(player, self)
        self._add_message(msg)
        self._check_finish()
        print(payload)

    def pay_to_get_out_of_jail(self):
        if self.in_jail and self.money >= 300:
            self.money -= 300
            self.in_jail = False
            self.jail_turns = 0
            return '{} đã trả 300$ để thoát khỏi tù'.format(self.display_name())
        return '{} không đủ tiền để trả 300$ để thoát khỏi tù'.format(self.display_name())

    def _check_finish(self):
        for player in self.players:
            if player.money < 0:
                self.winner = self.players[player.id - 1]

    def _updated_field_build(self, field_id: str):
        field_id = int(field_id)
        for field in self.board:
            if field.id == field_id:
                if field.build == '4': field.build = 'h'
                if field.build == '3': field.build = '4'
                if field.build == '2': field.build = '3'
                if field.build == '1': field.build = '2'
                if field.build == '0': field.build = '1'

                field.owner.money -= field.build_price

    def _sell_field(self, player: Player, field: Union[CityField, TrainField]):
        player.money -= field.price
        player.owned_fields.append(field)
        field.owner = player

    def _add_message(self, msg):
        self.msgs.append(msg)

    def _next_player(self):
        if self.current_player_index + 1 == len(self.players):
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.can_buy = False

    def _render_board(self):
        for field in FIELDS:
            if field['type'] == CITY:
                f = CityField(field)
            elif field['type'] == FINE:
                f = FineField(field)
            elif field['type'] == SECRET:
                f = SurpriseField(field)
            elif field['type'] == TRAIN:
                f = TrainField(field)
            elif field['type'] == POWERPLANT:
                f = PowerplantField(field)
            elif field['type'] == GOTO:
                f = GotoField(field)
            elif field['type'] == PRISON:
                f = JailField(field)
            else:
                f = PlaceholderField(field)

            self.board.append(f)

