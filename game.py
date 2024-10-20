from collections import defaultdict
from random import shuffle

from game_map import GameMap
from player import Player
from util import get_gene_input


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
        self.vote_count_for_toxic_ = defaultdict(int)

    def GeneratePlayers(self):
        while True:
            player_num = input("Enter the player num: ")
            try:
                player_num = int(player_num)
                break
            except:
                continue
        self.players_ = []
        for i in range(player_num):
            print("\nPlayer", i, " please input your initial gene.")
            name = input("Enter your name: ")
            power, movement, bag_size = get_gene_input()
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
                born_room = input(
                    "Invalid born room. Please re-enter your born room: "
                ).lower()
                born_level_num, born_room_num = self.map_.ParseRoomString(born_room)
            self.map_.PlayerBorn(player, (born_level_num, born_room_num))

    def Proceed(self):
        while self.round_count_ < 6:
            # Initial round 0
            if self.round_count_ == 0:
                self.SelectPlayerBornLocation()
                self.GetRoundResults()
            # In Proceed:
            # Action 0: next round. Action 1: Save, Action 2: load (save, modify, and load to conduct adjustment)
            self.ProcceedOneRound()
        print("Game finished!")

    def ProcceedOneRound(self):
        # In one round:
        # Action 0.n: player moves -> select player
        # Action 1: Get round result (can not do this if not all players current_round is round_count)
        self.round_count_ += 1
        # Randomly shuffle the player action order.
        shuffle(self.players_)
        print(
            "\nRound ",
            self.round_count_,
            "\nThe order of player execution in this round is: ",
        )
        for player in self.players_:
            print(player.name_)

        # Players actions.
        self.vote_count_for_toxic_ = defaultdict(int)
        self.bazooka_level_and_room_num_ = None
        for player in self.players_:
            print("\n Player", player.name_)
            # Update the player status to this round
            player.current_round_ = self.round_count_

            # Report the item exchanges.
            if self.round_count_ > 1:
                self.ReportItemChange(player)

            # Player moves.
            while True:
                room = input("Decide your target room: ").lower()
                level, target_room_num = self.map_.ParseRoomString(room)
                if self.map_.PlayerMove(player, (level, target_room_num)):
                    break

            # TODO: automatically do lottery.
            # Moderator help do the lottery and player pick items from the room.
            while True:
                item_name = input(
                    "Enter the item name, if you pick any: (Press enter to skip)"
                )
                if not item_name:
                    break
                player.PickItem(item_name)

            # Player use special item.
            if player.ItemInBag("bazooka"):
                room = input(
                    "Decide your target attack room num using bazooka: "
                ).lower()
                level, target_room_num = self.map_.ParseRoomString(room)
                self.bazooka_level_and_room_num_ = (level, target_room_num)

            # Vote for toxicant level.
            while True:
                level = input("Vote for the level you want to toxify: ")
                if level is not None and int(level) not in self.map_.toxicant_level_:
                    break
                print("This level is already filled with toxic gas. Please re-input.\n")
            self.vote_count_for_toxic_[level] += 1

        self.GetRoundResults()

    def GetPlayer(self, player_name):
        for player in self.players_:
            if player.name_ == player_name:
                return player
        return None

    # TODO: make it a stand-alone/jump-in section?
    def ReportItemChange(self, player):
        while True:
            exchange_type = input(
                "Do you want to report give/receive/exchange (please input one of the type)?"
            )
            # TODO: add anti-duplication (aka. two player both reported the same thing) mechanism.
            if not exchange_type:
                return
            elif exchange_type == "give":
                to_player = input("To whom?")
                item = input("What item?")
                self.PlayerGiveItem(player, self.GetPlayer(to_player), item)
            elif exchange_type == "receive":
                from_player = input("From whom?")
                item = input("What item?")
                self.PlayerGiveItem(self.GetPlayer(from_player), player, item)
            elif exchange_type == "exchange":
                exchange_player = input("With whom?")
                item_give = input("What item you give?")
                item_receive = input("What item you receive?")
                self.PlayerExchangeItem(
                    player, self.GetPlayer(exchange_player), item_give, item_receive
                )
            else:
                print("Please input one of the exchange types.")

    def PlayerGiveItem(self, from_player, to_player, item):
        if not from_player or not to_player:
            print("Player name does not exist.")
            return
        if from_player == to_player:
            print("You are giving items to yourself.")
        if not from_player.ItemInBag(item):
            print(item, " not in ", from_player.name_, "'s bag.")
            return
        if len(to_player.bag_) >= to_player.bag_size_:
            print(to_player.name_, "'s bag is full.")
            return
        from_player.UseItem(item)
        to_player.PickItem(item)
        print(
            f"===PRIVATE NEWS: {from_player.name_} gives item {item} to {to_player.name_}.==="
        )

    def PlayerExchangeItem(
        self, player1, player2, player1_give_item, player2_give_item
    ):
        if not player1 or not player2:
            print("Player name does not exist.")
            return
        if player1 == player2:
            print("You are exchanging items with yourself.")
        if not player1.ItemInBag(player1_give_item):
            print(player1_give_item, " not in ", player1.name_, "'s bag.")
            return
        if not player2.ItemInBag(player2_give_item):
            print(player2_give_item, " not in ", player2.name_, "'s bag.")
            return
        player1.UseItem(player1_give_item)
        player2.PickItem(player1_give_item, allow_exceeding_limit=True)
        player2.UseItem(player2_give_item)
        player1.PickItem(player2_give_item)
        print(
            f"===PRIVATE NEWS: {player1.name_} gives item {player1_give_item} to {player2.name_}.==="
        )
        print(
            f"===PRIVATE NEWS: {player2.name_} gives item {player2_give_item} to {player1.name_}.==="
        )

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
            self.map_.toxicant_level_.append(int(level))

    def GetRoundResults(self):
        for player in self.players_:
            if player.current_round_ != self.round_count_:
                print(
                    f"Player {player.name_} has not moved in this run. Can not get round result."
                )
                return False

        # Epinephrine faded our after the player moves.
        self.AllPlayerEpinephrineFade()
        # Make some levels filled with toxic gas.
        self.ToxifySomeLevels()

        if self.round_count_ != 0:
            # TODO: add alcohol.
            # Water and Food. (Input)
            if self.round_count_ >= 2:
                self.WaterAndFood()
            # Pills and Epinephrine. (Input)
            self.PillAndEpinephrine()

        self.PlayerHurtByPassingLaserRoom()

        # Toxic gas.
        self.map_.PlayerHurtByToxicGas(
            toxic_strength=self.toxic_strengths_[self.round_count_]
        )

        # Other Special logics.
        if self.bazooka_level_and_room_num_:
            self.map_.RoomAttackedByBazooka(self.bazooka_level_and_room_num_)

        # Trigger fights (human and ghost) and update player information if players are in the same room.
        self.map_.TriggerFight()

        self.FinalizeAllPlayersStatus()

        self.ShowResults()

    def PlayerHurtByPassingLaserRoom(self):
        for player in self.players_:
            if player.pass_laser_room_:
                player.pass_laser_room_ = False
                player.ReduceLife(1)
                print(
                    f"===PRIVATE NEWS: {player.name_} hurt by 1 life due to passing by the laser room.==="
                )

    def FinalizeAllPlayersStatus(self):
        for player in self.players_:
            if player.FinalizeLife():
                player.CleanBag()
                self.map_.PlayerMoveToDeathRoom(player)

    def WaterAndFood(self):
        for player in self.players_:
            if player.is_ghost_:
                continue
            print("\n Player", player.name_)
            if self.map_.PlayerInRestaurant(player):
                print(
                    f"===PRIVATE NEWS: {player.name_} in restaurant, no need to submit water and food.==="
                )
                return
            # The special version from airdrop.
            use_water_and_food = False
            if player.ItemInBag("water_and_food"):
                use_water_and_food = input(
                    "Do you want to use the water_and_food? (Press enter to skip)"
                )
                if use_water_and_food:
                    player.IncreaseLife(2)
                    player.UseItem("water_and_food")
                    print(
                        f"===PUBLIC NEWS: {player.name_} submits a water_and_food. Add 2 Life.==="
                    )
            # Regular version.
            if not use_water_and_food and player.ItemInBag("water"):
                use_water = input("Do you want to use water? (Press enter to skip)")
                if use_water:
                    player.IncreaseLife(1)
                    player.UseItem("water")
                    print(
                        f"===PUBLIC NEWS: {player.name_} submits a water. Add 1 life.==="
                    )
            if not use_water_and_food and player.ItemInBag("food"):
                use_food = input("Do you want to use food? (Press enter to skip)")
                if use_food:
                    player.IncreaseLife(1)
                    player.UseItem("food")
                    print(
                        f"===PUBLIC NEWS: {player.name_} submits a food. Add 1 life.==="
                    )
            player.ReduceLife(2)
            print(f"===PUBLIC NEWS: {player.name_} reduces 2 life.===")

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
                    print(f"===PUBLIC NEWS: {player.name_} uses a pill.===")
            if player.ItemInBag("epinephrine"):
                use_epinephrine = input(
                    "Do you want to use epinephrine? (Press enter to skip)"
                )
                if use_epinephrine:
                    player.UseItem("epinephrine")
                    player.consumeEpinephrine()
                    print(f"===PUBLIC NEWS: {player.name_} uses am epinephrine.===")

    # TODO: add output string in every calculation step, for moderator usage.
    def ShowResults(self):
        print("\n Result of round ", self.round_count_)
        for player in self.players_:
            player.StatusString()
        level_string = ""
        for level in self.map_.toxicant_level_:
            level_string += str(level) + " "
        print(f"===PUBLIC NEWS: Toxic gas are filled in level: {level_string}.===")


if __name__ == "__main__":
    new_game = Game()
    new_game.Proceed()
