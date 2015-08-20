class Player:
    pass

class Enemy(Player):
    pass

class GameObject(Player, Enemy):
    pass

g = GameObject()
print 33
