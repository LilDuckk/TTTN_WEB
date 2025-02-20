def get_300(player):
    player.money += 300
    return '<span style="color: {};">Người chơi {}</span> nhặt được 300$'.format(player.color, player.id)

def lose_300(player):
    player.money -= 300
    return '<span style="color: {};">Người chơi {}</span> làm rơi 300$'.format(player.color, player.id)

def get_150_wedding(player):
    player.money += 150
    return '<span style="color: {};">Người chơi {}</span> nhận 150$ tiền cưới'.format(player.color, player.id)

def lose_300_investment(player):
    player.money -= 300
    return '<span style="color: {};">Người chơi {}</span> đầu tư thua lỗ 300$'.format(player.color, player.id)

def lose_100_wedding(player):
    player.money -= 100
    return '<span style="color: {};">Người chơi {}</span> đi ăn cưới mất 100$'.format(player.color, player.id)

def get_250_investment(player):
    player.money += 250
    return '<span style="color: {};">Người chơi {}</span> đầu tư lời được 250$'.format(player.color, player.id)

SURPRISES = [lose_300, get_300, get_150_wedding, lose_300_investment, lose_100_wedding, get_250_investment]