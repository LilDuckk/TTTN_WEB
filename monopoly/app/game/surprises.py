def get_300(player):
    player.money += 300
    return 'Người chơi {} nhặt được 300$'.format(player.id)

def lose_300(player):
    player.money -= 300
    return 'Người chơi {} làm rơi 300$'.format(player.id)

def get_150_wedding(player):
    player.money += 150
    return 'Người chơi {} nhận 150$ tiền cưới'.format(player.id)

def lose_300_investment(player):
    player.money -= 300
    return 'Người chơi {} đầu tư thua lỗ 300$'.format(player.id)

def lose_100_wedding(player):
    player.money -= 100
    return 'Người chơi {} đi ăn cưới mất 100$'.format(player.id)

def get_250_investment(player):
    player.money += 250
    return 'Người chơi {} đầu tư lời được 250$'.format(player.id)

SURPRISES = [lose_300, get_300, get_150_wedding, lose_300_investment, lose_100_wedding, get_250_investment]