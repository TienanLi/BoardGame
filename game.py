from game_map import GameMap
from player import Player

# Big TODO: use a graphic interface.
class Game:
    def __init__(self, player_num):
        self.map_ = GameMap()
        self.round_count_ = 0
        self.GeneratePlayers(player_num)

    def GeneratePlayers(self, player_num):
        self.player_ = []
        for i in range(player_num):
            print("\nPlayer", i, " please input your initial gene." )
            name = input("Enter your name: ")
            power = input("Decide your power capability: ")
            movement = input("Decide your movement capability: ")
            bag_size = input("Decide your bag size: ")
            self.player_.append(Player(name, int(power), int(movement), int(bag_size)))

    # TODO
    def ProcceedARound(self):
        return
        # Randomly generate the player action order.


        # Players in the same group to swap items.


        # Player actions. (make move, do lottery if needed, use special items if has);

    # TODO
    def GetRoundResults(self):
        return

        # Water and Food. (Input)

        # Pills and Epinephrine. (Input)

        # note: do the above two procedures first to avoid underlying player life becoming negative then positive again.

        # Trigger fights (human and ghost) and update player information if players are in the same room.

        # Toxic gas.

        # Other Special logics.
        # Missile.


        self.round_count_ += 1
        if (self.round_count_ > 6):
            print("Game finish.")
            # Show Results.



if __name__ == '__main__':
    player_num = input("Enter the player num: ")
    Game(int(player_num))