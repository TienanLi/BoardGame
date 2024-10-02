from enum import Enum

class RoomType(Enum):
    NO_TYPE = 0
    BORN_ROOM = 1
    OPERATING_ROOM = 2
    HELICOPTER_STATION = 3
    # TODO: add more types

class Room:
    def __init__(self, level, room_num):
        self.level_ = level
        self.room_num_ = room_num
        # Helicopter station is auto anti-toxic
        self.is_anti_toxic_ = True if (level == 2 and room_num == 2) else False
        self.player_in_ = []
        self.item_in_ = []
        self.type_ = RoomType.NO_TYPE
        # i need a map that maps the room index to the room level and room number
        self.room_index2levelroom_map_ = {}
        self.room_levelroom2index_map_ = {}
        # i need a map that maps the room index to the room object
        self.room_levelroom2object_map_ = {}

    def MakeAntiToxic(self):
        self.is_anti_toxic_ = True

    def PlayerJoin(self, player):
        self.player_in_.append(player)

    def PlayerLeft(self, player):
        self.player_in_.remove(player)

    def TriggerFight(self):
        # TODO: operation room mechanism.
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
        # We only support [-9,9] levels and [00,99] rooms.`
        self.map_adj_matrix_ = {}

    def RoomIsBornRoom(self, level_and_num):
        if level_and_num not in self.room_list_:
            self.room_list_[level_and_num] = Room(level_and_num[0], level_and_num[1])
        self.room_list_[level_and_num].type_ = RoomType.BORN_ROOM

    def PlayerBorn(self, player, level_and_num):
        if level_and_num not in self.room_list_:
            self.room_list_[level_and_num] = Room(level_and_num[0], level_and_num[1])
        self.room_list_[level_and_num].PlayerJoin(player)
        player.location_ = level_and_num

    def ParseRoomString(self, room_input_str):
        if room_input_str[0].isdigit():
            level = int(room_input_str[0])
            room  = int(room_input_str)
        else:
            level = -int(room_input_str[1])
            room  = int(room_input_str[1:])
        print("Level: ", level, " Room: ", room)
        return level, room

    # TODO: build adjacent matrix to determine the distance of rooms automatically (and add auto step num judgement).
    # Also need to consider epinephrine in the step judge.
    # create the adjacent matrix for rooms and the distance between rooms.
    def GenerateMap(self):
        print("Create the map.\n")
        level_num_above_ground = input("Enter the levels above the ground: ")
        level_num_under_ground = input("Enter the levels under the ground: ")
        for i in range(int(level_num_above_ground), -int(level_num_under_ground), -1):
            if i == 0:
                continue
            print("Level ", i, "\n")
            add_in_batch = input("Add in batch? (Press Y to start or N to skip)").lower()
            if add_in_batch == "y":
                while True:
                    room_num_start = input("Add in batch. Enter the room start in level " + str(i) + ": ")
                    if len(room_num_start) > 2:
                        room_num_start = room_num_start[-2:]
                    room_num_end = input("Add in batch. Enter the room end in level " + str(i) + ": ")
                    if len(room_num_end) > 2:
                        room_num_end = room_num_end[-2:]
                    # flip start and end if start is larger than end
                    if int(room_num_start) > int(room_num_end):
                        room_num_start, room_num_end = room_num_end, room_num_start
                    # add rooms to the map
                    room_list_temp = ""
                    for j in range(int(room_num_start), int(room_num_end) + 1):
                        if i < 0:
                            room_list_temp += "B%d%02d " % (abs(i), j)
                        else:
                            room_list_temp += "%i%02d " % (i, j)
                        pass
                    print("Rooms added: ", room_list_temp)

                    finished_adding = input("Another batch? (Press Y to start or N to skip)").lower()
                    if finished_adding == "n":
                        break

            add_by_individual = input("Add by individual? (Press Y to start or N to skip)").lower()
            if add_by_individual == "y":
                while True:
                    room_num = input("Enter the room num in level " + str(i) + ": ")
                    if len(room_num) > 2:
                        room_num = room_num[-2:]
                    if i < 0:
                        print("Rooms added: B%d%02d " % (abs(i), int(room_num)))
                    else:
                        print("Rooms added: %d%02d " % (i, int(room_num)))
                    pass
                    # add room to the map
                    finished_adding = input("Continue adding rooms in level " + str(i) + "? (Press Y to continue or N to skip)")
                    if finished_adding == "n":
                        break

    def BuildMapAdjMatrix(self):
        pass

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

    def RoomAttackedByBazooka(self, level_and_num):
        if level_and_num not in self.room_list_:
            return
        for player in self.room_list_[level_and_num].player_in_:
            player.ReduceLife(4)