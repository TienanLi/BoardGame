from player import Player

class Room:
    def __init__(self, level, room_num):
        self.level_ = level
        self.room_num_ = room_num
        # Helicopter station is auto anti-toxic
        self.is_anti_toxic_ = True if (level == 2 and room_num == 2) else False
        self.player_in_ = []
        self.item_in_ = []

    def MakeAntiToxic(self):
        self.is_anti_toxic_ = True

    def PlayerJoin(self, player):
        self.player_in_.append(player)

    def PlayerLeft(self, player):
        self.player_in_.remove(player)

    def TriggerFight(self):
        if self.HasAnyoneHasGun():
            self.HumanBrawlWithGun()
        else:
            self.HumanBrawlWithoutGun()
        self.GhostBloodSucking()

    def HasAnyoneHasGun(self):
        for player in self.player_in_:
            if player.HasGun():
                return True
        return False

    def HumanBrawlWithGun(self):
        player_with_gun = []
        for player in self.player_in_:
            if player.HasGun():
                player_with_gun.append(player)
        highest_power = 0
        for player in player_with_gun:
            highest_power = max(highest_power, player.PowerWithWeapon())
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            player.ReduceLife(highest_power - (player.PowerWithWeapon() if player.HasGun() else 0))

    def HumanBrawlWithoutGun(self):
        highest_power = 0
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            highest_power = max(highest_power, player.PowerWithWeapon())
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            player.ReduceLife(highest_power - player.PowerWithWeapon())
    
    def GhostBloodSucking(self):
        ghosts = [player for player in self.player_in_ if player.is_ghost_]
        humans = [player for player in self.player_in_ if not player.is_ghost_]
        for ghost in ghosts:
            ghost.IncreaseLife(len(humans))
        for human in humans:
            human.ReduceLife(len(ghosts))
    
class GameMap:
    def __init__(self):
        self.room_list_ = {}
        self.toxicant_level_ = []

    def PlayerBorn(self, player, level_and_num):
        if level_and_num not in self.room_list_:
            self.room_list_[level_and_num] = Room(level_and_num[0], level_and_num[1])
        self.room_list_[level_and_num].PlayerJoin(player)
        player.location_ = level_and_num

    # TODO: build adjacent matrix to determine the distance of rooms automatically (and add auto step num judgement).
    def PlayerMove(self, player, target_level_and_num):
        original_level_and_num = player.location_
        if original_level_and_num == target_level_and_num:
            print("Can not stay in the same room. Please re-input.\n")
            return False
        self.room_list_[original_level_and_num].PlayerLeft(player)
        if target_level_and_num not in self.room_list_:
            self.room_list_[target_level_and_num] = Room(target_level_and_num[0], target_level_and_num[1])
        self.room_list_[target_level_and_num].PlayerJoin(player)
        player.location_ = target_level_and_num
        return True

    def TriggerFight(self):
        for _, room in self.room_list_.items():
            # TODO: exclude operating room
            room.TriggerFight()

    def PlayerHurtByToxicGas(self, toxic_strength):
        for level_and_num, room in self.room_list_.items():
            if level_and_num[0] in self.toxicant_level_ and not room.is_anti_toxic_:
                for player in room.player_in_:
                    player.ReduceLife(toxic_strength)
