from game_map import GameMap
from player import Player

# Big TODO: use a graphic interface.
class Game:
    def __init__(self, player_num):
        self.map_ = GameMap()
        self.round_count_ = 0
        self.GeneratePlayers(player_num)
        # round 0, 1, 2, 3, 4, 5, 6
        self.toxic_strengths = [0, -1, -2, -2, -3, -3, -3]

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
        # Randomly generate the player action order.

        # Players in the same group to swap items.

        # Players actions. (make move, do lottery if needed, use special items if has);

        # Make some levels toxicant.
        return

    # TODO
    def GetRoundResults(self):
        # Water and Food. (Input)

        # Pills and Epinephrine. (Input)

        # note: do the above two procedures first to avoid underlying player life becoming negative then positive again.

        # Trigger fights (human and ghost) and update player information if players are in the same room.
        self.map_.TriggerFight()

        # Toxic gas.
        self.map_.CountToxicGas(toxic_strength=self.toxic_strengths[self.round_count_])

        # Other Special logics.
        # Missile.

        self.ShowResults()

    def ShowResults(self):
        print("\n Result of round ", self.round_count_)
        for player in self.players_:
            player.StatusString()



if __name__ == '__main__':
    player_num = input("Enter the player num: ")
    new_game = Game(int(player_num))
    new_game.Proceed()