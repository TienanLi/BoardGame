from ctypes.wintypes import tagMSG
from enum import Enum

class RoomType(Enum):
    NO_TYPE = 0
    BORN_ROOM = 1
    OPERATING_ROOM = 2
    HELICOPTER_STATION = 3
    DEATH_ROOM = 4
    # TODO: add more types

kSpecialRoomDict = {(-2, 202): RoomType.OPERATING_ROOM, (2, 202): RoomType.HELICOPTER_STATION,
                    (-1, 103): RoomType.BORN_ROOM, (-3, 303): RoomType.BORN_ROOM, (-4, 402): RoomType.BORN_ROOM,
                    (-6, 603): RoomType.BORN_ROOM, (-3, 307): RoomType.BORN_ROOM, (1, 103): RoomType.BORN_ROOM,
                    (-7, 701): RoomType.DEATH_ROOM}

class Room:
    def __init__(self, level, room_num):
        self.level_ = level
        self.room_num_ = room_num
        self.player_in_ = []
        self.item_in_ = []
        self.type_ = self.AssignRoomType((level, room_num))
        self.is_anti_toxic_ = True if self.type_ == RoomType.HELICOPTER_STATION else False
        # i need a map that maps the room index to the room level and room number
        self.room_index2levelroom_map_ = {}
        self.room_levelroom2index_map_ = {}
        # i need a map that maps the room index to the room object
        self.room_levelroom2object_map_ = {}

    def AssignRoomType(self, level_and_num):
        if level_and_num in kSpecialRoomDict:
            return kSpecialRoomDict[level_and_num]
        return RoomType.NO_TYPE

    def MakeAntiToxic(self):
        self.is_anti_toxic_ = True

    def PlayerJoin(self, player):
        self.player_in_.append(player)

    def PlayerLeft(self, player):
        self.player_in_.remove(player)

    def TriggerFight(self):
        if (self.type_ == RoomType.OPERATING_ROOM) and (self.CountHuman() == 2):
            # Special logic for the operation room.
            self.Operation()
        elif self.HasAnyoneHasGun():
            self.HumanBrawlWithGun()
        else:
            self.HumanBrawlWithoutGun()
        self.GhostBloodSucking()

    def CountHuman(self):
        count = 0
        for player in self.player_in_:
            if not player.is_ghost_:
                count += 1
        return count

    def Operation(self):
        for player in self.player_in_:
            if not player.is_ghost_:
                player.IncreaseLife(4)

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
        # We only support [-9,9] levels and [00,99] rooms.`
        self.map_adj_matrix_ = {}

    def RoomIsBornRoom(self, level_and_num):
        if level_and_num not in self.room_list_:
            self.room_list_[level_and_num] = Room(level_and_num[0], level_and_num[1])
        return self.room_list_[level_and_num].type_ == RoomType.BORN_ROOM

    def PlayerBorn(self, player, level_and_num):
        if level_and_num not in self.room_list_:
            self.room_list_[level_and_num] = Room(level_and_num[0], level_and_num[1])
        self.room_list_[level_and_num].PlayerJoin(player)
        player.location_ = level_and_num

    def ParseRoomString(self, room_input_str):
        if not room_input_str:
            return None, None
        if room_input_str[0].isdigit():
            level = int(room_input_str[0])
            room  = int(room_input_str)
        else:
            level = -int(room_input_str[1])
            room  = int(room_input_str[1:])
        return level, room

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

    def PlayerMoveToDeathRoom(self, player):
        self.PlayerMove(player, (-7, 701))

    def TriggerFight(self):
        for _, room in self.room_list_.items():
            room.TriggerFight()

    def PlayerHurtByToxicGas(self, toxic_strength):
        for level_and_num, room in self.room_list_.items():
            if level_and_num[0] in self.toxicant_level_ and not room.is_anti_toxic_:
                for player in room.player_in_:
                    player.ReduceLife(toxic_strength)

    def RoomAttackedByBazooka(self, level_and_num):
        if level_and_num not in self.room_list_:
            return
        for player in self.room_list_[level_and_num].player_in_:
            player.ReduceLife(4)