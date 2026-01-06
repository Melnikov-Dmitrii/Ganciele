import random


class Player:
    id_counter = 0

    def __init__(self):
        Player.id_counter += 1
        self.id = Player.id_counter
        self.has_secret = 0
        self.secret = None

    def set_secret(self, secret):
        self.has_secret = 1
        self.secret = secret


class Game:
    
    id_counter = 0
    
    def __init__(self):
        Game.id_counter += 1
        self.id = Game.id_counter
        self.players = []
        self.stage = 0
        """
        0: start
        1: recruiting
        2: receiving secrets
        3: sending
        """

    def add_player(self, player):
        if self.stage == 1:
            self.players.append(player)
        else:
            print("add_player: wrong stage!")

    def remove_player(self, playerID):
        if self.stage == 1:
            self.players = [p for p in self.players if p.id != playerID]
        else:
            print("remove_player: wrong stage!")

    def randomise_circle(self):
        random.shuffle(self.players)

    def set_secret_from_player(self, secret, playerID):
        if self.stage == 2:
            for i in range(len(self.players)):
                if self.players[i].id == playerID:
                    self.players[i - 1].set_secret(secret)
        else:
            print("set_secret_from_player: wrong stage!")

    def get_secrets_for_player(self, playerID):
        res = []
        for player in self.players:
            if player.id != playerID:
                res.append((player.id, player.secret))
        return res
        
    def get_secrets_for_players(self):
        res = []
        for player in self.players:
            res.append((player.id, self.get_secrets_for_player(player.id)))
        return res
        
    def print_secrets(self):
        for player in self.players:
            print(player.id, " ", player.secret)

    def check_secrets(self):
        for player in self.players:
            if player.has_secret == 0:
                return False
        return True
        