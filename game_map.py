from player import Player

class Room:
    def __init__(self, level, room_num):
        self.level_ = level
        self.room_num_ = room_num
        # Helicopter station is auto anti-toxic
        self.is_anti_toxic_ = True if (level == 2 and room_num == 2) else False
        self.player_in_ = []

    def MakeAntiToxic(self):
        self.is_anti_toxic_ = True

    def PlayerJoin(self, player):
        self.player_in_.append(player)

    def PlayerLeft(self, player):
        self.player_in_.remove(player)

    def TriggerFight(self):
        if len(self.player_in_) <= 1:
            return
        elif len(self.player_in_) == 2:
            self.PlayersDeuce()
        else:
            self.PlayersBrawl()

    # TODO
    def PlayersDeuce(self):
        return

    # TODO
    def PlayersBrawl(self):
        return
        # Find highest-power-score player

class GameMap:
    def __init__(self):
        self.room_list_ = {}
        self.toxicant_level = []

    # TODO
    def playerBorn(self):
        return

    # TODO: build adjacent matrix to determine the distance of rooms automatically (and add auto step num judgement).
    # TODO: make level and room_num auto-extracted from an input string.
    def PlayerMove(self, player, original_level_and_num, target_level_and_num):
        self.room_list_[original_level_and_num].PlayerLeft(player)
        if target_level_and_num not in self.room_list_:
            self.room_list_[target_level_and_num] = Room(target_level_and_num[0], target_level_and_num[1])
        self.room_list_[target_level_and_num].PlayerJoin(player)

    def TriggerFight(self):
        for _, room in self.room_list_:
            room.TriggerFight()

