from collections import defaultdict
from random import shuffle

from game_map import GameMap
from player import Player

# Big TODO: use a graphic interface.
class Game:
    def __init__(self):
        self.map_ = GameMap()
        # self.map_.GenerateMap()
        self.round_count_ = 0
        self.GeneratePlayers()
        # round 0, 1, 2, 3, 4, 5, 6
        self.toxic_strengths_ = [0, 1, 2, 2, 3, 3, 4]
        # for recycling machine.
        self.used_consumables = []
        self.bazooka_level_and_room_num_ = None

    def GeneratePlayers(self):
        player_num = input("Enter the player num: ")
        self.players_ = []
        for i in range(int(player_num)):
            print("\nPlayer", i, " please input your initial gene." )
            name = input("Enter your name: ")
            while True:
                power = int(input("Decide your power capability: "))
                movement = int(input("Decide your movement capability: "))
                bag_size = int(input("Decide your bag size: "))
                if power + movement + bag_size == 10:
                    break
                print("Sum is not 10. Please re-input.\n")
            self.players_.append(Player(name, int(power), int(movement), int(bag_size)))


    def SelectPlayerBornLocation(self):
        for player in self.players_:
            print("\n Player", player.name_)
            born_room = input("Decide your born room: ").lower()
            # remove all spaces between characters
            born_room = "".join(born_room.split())
            # check in the map if the born room type is BORN_ROOM
            born_level_num, born_room_num = self.map_.ParseRoomString(born_room)
            while not self.map_.RoomIsBornRoom((born_level_num, born_room_num)):
                born_room = input("Invalid born room. Please re-enter your born room: ").lower()
                born_level_num, born_room_num = self.map_.ParseRoomString(born_room)
            self.map_.PlayerBorn(player, (born_level_num, born_room_num))

    def Proceed(self):
        while self.round_count_ < 6:
            # Initial round 0
            if self.round_count_ == 0:
                self.SelectPlayerBornLocation()
                self.GetRoundResults()
            self.ProcceedOneRound()
            self.GetRoundResults()
        print("Game finished!")

    def ProcceedOneRound(self):
        self.round_count_ += 1
        # Randomly shuffle the player action order.
        shuffle(self.players_)
        print("\nRound ", self.round_count_, "\nThe order of player execution in this round is: ")
        for player in self.players_:
            print(player.name_)

        # TODO: Players in the same group to swap items.

        # Players actions.
        self.vote_count_for_toxic_ = defaultdict(int)
        self.bazooka_level_and_room_num_ = None
        for player in self.players_:
            # Player moves.
            print("\n Player", player.name_)
            while True:
                room = input("Decide your target room: ").lower()
                level, target_room_num = self.map_.ParseRoomString(room)
                if self.map_.PlayerMove(player, (level, target_room_num)):
                    break

            # TODO: automatically do lottery.
            # Moderator help do the lottery and player pick items from the room.
            while True:
                item_name = input("Enter the item name, if you pick any: (Press enter to skip)")
                if not item_name:
                    break
                player.PickItem(item_name)

            # Player use special item.
            if player.ItemInBag("bazooka"):
                room = input("Decide your target attack room num using bazooka: ").lower()
                level, target_room_num = self.map_.ParseRoomString(room)
                self.bazooka_level_and_room_num_ = (level, target_room_num)

            # Vote for toxicant level.
            while True:
                level = input("Vote for the level you want to toxify: ")
                if level not in self.map_.toxicant_level_:
                    break
                print("This level is already filled with toxic gas. Please re-input.\n")
            self.vote_count_for_toxic_[level] += 1
        # Epinephrine faded our after the player moves.
        self.AllPlayerEpinephrineFade()
        # Make some levels filled with toxic gas.
        self.ToxifySomeLevels()

    def AllPlayerEpinephrineFade(self):
        for player in self.players_:
            player.EpinephrineFade()

    def ToxifySomeLevels(self):
        max_vote_num = 0
        most_voted_level = []
        for level, vote in self.vote_count_for_toxic_.items():
            if vote > max_vote_num:
                max_vote_num = vote
                most_voted_level = [level]
            elif vote == max_vote_num:
                most_voted_level.append(level)

        for level in most_voted_level:
            self.map_.toxicant_level_.append(level)


    def GetRoundResults(self):
        if self.round_count_ != 0:
            # Water and Food. (Input)
            if self.round_count_ >= 2:
                self.WaterAndFood()
            # Pills and Epinephrine. (Input)
            self.PillAndEpinephrine()

        # Toxic gas.
        self.map_.PlayerHurtByToxicGas(toxic_strength=self.toxic_strengths_[self.round_count_])

        # Other Special logics.
        if self.bazooka_level_and_room_num_:
            self.map_.RoomAttackedByBazooka(self.bazooka_level_and_room_num_)

        # Trigger fights (human and ghost) and update player information if players are in the same room.
        self.map_.TriggerFight()

        self.FinalizeAllPlayersStatus()

        self.ShowResults()

    def FinalizeAllPlayersStatus(self):
        for player in self.players_:
            player.FinalizeLife()

    def WaterAndFood(self):
        for player in self.players_:
            if player.is_ghost_:
                continue
            print("\n Player", player.name_)
            # The special version from airdrop.
            use_water_and_food = False
            if player.ItemInBag("water_and_food"):
                use_water_and_food = input("Do you want to use the water_and_food? (Press enter to skip)")
                if use_water_and_food:
                    player.IncreaseLife(2)
                    player.UseItem("water_and_food")
            # Regular version.
            if not use_water_and_food and player.ItemInBag("water"):
                use_water = input("Do you want to use water? (Press enter to skip)")
                if use_water:
                    player.IncreaseLife(1)
                    player.UseItem("water")
            if not use_water_and_food and player.ItemInBag("food"):
                use_food = input("Do you want to use food? (Press enter to skip)")
                if use_food:
                    player.IncreaseLife(1)
                    player.UseItem("food")

    def PillAndEpinephrine(self):
        for player in self.players_:
            if player.is_ghost_:
                continue
            print("\n Player", player.name_)
            if player.ItemInBag("pill"):
                use_pill = input("Do you want to use pill? (Press enter to skip)")
                if use_pill:
                    player.IncreaseLife(2)
                    player.UseItem("pill")
            if player.ItemInBag("epinephrine"):
                use_epinephrine = input("Do you want to use epinephrine? (Press enter to skip)")
                if use_epinephrine:
                    player.UseItem("epinephrine")
                    player.consumeEpinephrine()

    def ShowResults(self):
        print("\n Result of round ", self.round_count_)
        for player in self.players_:
            player.StatusString()
        level_string = ""
        for level in self.map_.toxicant_level_:
            level_string += level + " "
        print("Toxic gas are filled in level: ", level_string)


if __name__ == '__main__':
    new_game = Game()
    new_game.Proceed()