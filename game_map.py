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

    # TODO: add control room mechanism.
    def MakeAntiToxic(self):
        self.is_anti_toxic_ = True
        print(f"===PRIVATE NEWS: {self.room_num_} at level {self.level_} is now anti-toxic.===")

    def PlayerJoin(self, player):
        self.player_in_.append(player)
        print(f"===PRIVATE NEWS: {player.name_} join {self.room_num_} at level {self.level_}.===")

    def PlayerLeft(self, player):
        self.player_in_.remove(player)
        print(f"===PRIVATE NEWS: {player.name_} left {self.room_num_} at level {self.level_}.===")

    def TriggerFight(self):
        if len(self.player_in_) <= 1:
            return
        self.GhostBloodSucking()
        if (self.type_ == RoomType.OPERATING_ROOM) and (self.CountHuman() == 2):
            # Special logic for the operation room.
            self.Operation()
        elif self.HasAnyoneHasGun():
            self.HumanBrawlWithGun()
        else:
            self.HumanBrawlWithoutGun()

    def CountHuman(self):
        count = 0
        for player in self.player_in_:
            if not player.is_ghost_:
                count += 1
        return count

    def Operation(self):
        debug = []
        for player in self.player_in_:
            if not player.is_ghost_:
                player.IncreaseLife(4)
                debug.append(player.name_)
        print(f"===PRIVATE NEWS: operation occurs and adds 4 life for both {debug[0]} and {debug[1]}.===")

    def HasAnyoneHasGun(self):
        for player in self.player_in_:
            if player.HasGun():
                return True
        return False

    def HumanBrawlWithGun(self):
        print(f"===PRIVATE NEWS: {self.room_num_} at level {self.level_} has a fight involving gun.===")
        player_with_gun = []
        for player in self.player_in_:
            if player.HasGun():
                player_with_gun.append(player)
        highest_power = 0
        highest_power_player = []
        for player in player_with_gun:
            if player.PowerWithWeapon() > highest_power:
                highest_power = player.PowerWithWeapon()
                highest_power_player = [player]
            elif player.PowerWithWeapon() == highest_power:
                highest_power_player.append(player)
        print("===PRIVATE NEWS: highest power man with gun are", [player.name_ for play in highest_power_player],
              f"with {highest_power} power.===")
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            player_power = player.PowerWithWeapon() if player.HasGun() else 0
            player_lose = highest_power - player_power
            player.ReduceLife(player_lose)
            print(f"===PRIVATE NEWS: {player.name_} loses {player_lose} life",
                  "without gun.===" if player_power == 0 else "with gun.===")

    def HumanBrawlWithoutGun(self):
        print(f"===PRIVATE NEWS: {self.room_num_} at level {self.level_} has a fight not involving gun.===")
        highest_power = 0
        highest_power_player = []
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            if player.PowerWithWeapon() > highest_power:
                highest_power = player.PowerWithWeapon()
                highest_power_player = [player]
            elif player.PowerWithWeapon() == highest_power:
                highest_power_player.append(player)
        print("===PRIVATE NEWS: highest power man are", [player.name_ for play in highest_power_player],
              f"with {highest_power} power.===")
        for player in self.player_in_:
            if player.is_ghost_:
                continue
            player_lose = highest_power - player.PowerWithWeapon()
            player.ReduceLife(player_lose)
            print(f"===PRIVATE NEWS: {player.name_} loses {player_lose} life.===")

    def GhostBloodSucking(self):
        ghosts = [player for player in self.player_in_ if player.is_ghost_]
        humans = [player for player in self.player_in_ if not player.is_ghost_]
        print(f"===PRIVATE NEWS: {len(ghosts)} ghosts and {len(humans)} humans in "
              f"{self.room_num_} at level {self.level_}.===")
        if len(ghosts) > 0 and len(humans) > 0:
            for ghost in ghosts:
                ghost.IncreaseLife(len(humans))
                print(f"===PRIVATE NEWS: ghost {ghost.name_} increases {len(humans)} life.===")
            for human in humans:
                human.ReduceLife(len(ghosts))
                print(f"===PRIVATE NEWS: human {human.name_} loses {len(ghosts)} life.===")


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
                    print(f"===PUBLIC NEWS: player {player.name_} hurts by toxic gas in {self.room_num_}"
                          f"at level {self.level_} for {toxic_strength} life")


    def RoomAttackedByBazooka(self, level_and_num):
        if level_and_num not in self.room_list_:
            return
        for player in self.room_list_[level_and_num].player_in_:
            player.ReduceLife(4)
        print(f"===PUBLIC NEWS: player {player.name_} hurts by bazooka in {self.room_num_}"
              f"at level {self.level_} for 4 life")