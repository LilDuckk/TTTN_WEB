def get_300(player):
    player.money += 300
    return 'player{} just got fre 300$'.format(player.id)


def lose_300(player):
    player.money -= 300
    return 'player{} just lost 300$'.format(player.id)


SURPRISES = [lose_300, get_300]