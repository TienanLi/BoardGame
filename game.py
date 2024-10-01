from collections import defaultdict
from random import shuffle

from game_map import GameMap
from player import Player

# Big TODO: use a graphic interface.
class Game:
    def __init__(self, player_num):
        self.map_ = GameMap()
        self.round_count_ = 0
        self.GeneratePlayers(player_num)
        # round 0, 1, 2, 3, 4, 5, 6
        self.toxic_strengths_ = [0, 1, 2, 2, 3, 3, 3]

    def GeneratePlayers(self, player_num):
        self.players_ = []
        for i in range(player_num):
            print("\nPlayer", i, " please input your initial gene." )
            name = input("Enter your name: ")
            power = input("Decide your power capability: ")
            movement = input("Decide your movement capability: ")
            bag_size = input("Decide your bag size: ")
            self.players_.append(Player(name, int(power), int(movement), int(bag_size)))

    def SelectPlayerBornLocation(self):
        for player in self.players_:
            print("\n Player", player.name_)
            # TODO: make level and room_num auto-extracted from an input string.
            level = input("Decide your born level: ")
            born_room_num = input("Decide your born room num: ")
            self.map_.PlayerBorn(player, (level, born_room_num))

    def Proceed(self):
        while self.round_count_ < 6:
            # Initial round 0
            if (self.round_count_ == 0):
                self.SelectPlayerBornLocation()
                self.GetRoundResults()
            self.ProcceedOneRound()
            self.GetRoundResults()
        print("Game finished!")

    # TODO
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
        for player in self.players_:
            # Player moves.
            print("\n Player", player.name_)
            level = input("Decide your target level: ")
            target_room_num = input("Decide your target room num: ")
            self.map_.PlayerMove(player, (level, target_room_num))
            # TODO: automatically do lottery.
            # Moderator help do the lottery and player pick items from the room.
            while True:
                item_name = input("Enter the item name, if you pick any: (Press enter to skip)")
                if not item_name:
                    break
                player.PickItem(item_name)
            # TODO: player use special item.

            # Vote for toxicant level.
            # TODO: do not allow voting for the same levels.
            level = input("Vote for the level you want to toxify: ")
            self.vote_count_for_toxic_[level] += 1

        # Make some levels filled with toxic gas.
        self.ToxifySomeLevels()

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
            for player in self.players_:
                print("\n Player", player.name_)
                use_water = input("Do you want to use water? (Press enter to skip)")
                if use_water:
                    player.IncreaseLife(1)
                    player.UseItem("water")
                use_food = input("Do you want to use food? (Press enter to skip)")
                if use_food:
                    player.IncreaseLife(1)
                    player.UseItem("food")
            # Pills and Epinephrine. (Input)
            for player in self.players_:
                print("\n Player", player.name_)
                use_pill = input("Do you want to use pills? (Press enter to skip)")
                if use_pill:
                    player.IncreaseLife(2)
                    player.UseItem("pill")
                use_epinephrine = input("Do you want to use Epinephrine? (Press enter to skip)")
                if use_epinephrine:
                    player.UseItem("use_epinephrine")
                    # TODO: make it funcational

        # Trigger fights (human and ghost) and update player information if players are in the same room.
        self.map_.TriggerFight()

        # Toxic gas.
        self.map_.PlayerHurtByToxicGas(toxic_strength=self.toxic_strengths_[self.round_count_])

        # Other Special logics.
        # Missile.

        self.ShowResults()

    def ShowResults(self):
        print("\n Result of round ", self.round_count_)
        for player in self.players_:
            player.StatusString()
        level_string = ""
        for level in self.map_.toxicant_level_:
            level_string += level + " "
        print("Toxic gas are filled in level: ", level_string)


if __name__ == '__main__':
    player_num = input("Enter the player num: ")
    new_game = Game(int(player_num))
    new_game.Proceed()