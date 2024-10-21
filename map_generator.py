# This class is for easier generation of customized map.
class MapGenerator:
    def __init__(self):
        pass

    # TODO: build adjacent matrix to determine the distance of rooms automatically (and add auto step num judgement).
    # create the adjacent matrix for rooms and the distance between rooms.
    def GenerateMap(self):
        print("Create the map.\n")
        level_num_above_ground = input("Enter the levels above the ground: ")
        level_num_under_ground = input("Enter the levels under the ground: ")
        for i in range(int(level_num_above_ground), -int(level_num_under_ground), -1):
            if i == 0:
                continue
            print("Level ", i, "\n")
            add_in_batch = input(
                "Add in batch? (Press Y to start or N to skip)"
            ).lower()
            if add_in_batch == "y":
                while True:
                    room_num_start = input(
                        "Add in batch. Enter the room start in level " + str(i) + ": "
                    )
                    if len(room_num_start) > 2:
                        room_num_start = room_num_start[-2:]
                    room_num_end = input(
                        "Add in batch. Enter the room end in level " + str(i) + ": "
                    )
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

                    finished_adding = input(
                        "Another batch? (Press Y to start or N to skip)"
                    ).lower()
                    if finished_adding == "n":
                        break

            add_by_individual = input(
                "Add by individual? (Press Y to start or N to skip)"
            ).lower()
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
                    finished_adding = input(
                        "Continue adding rooms in level "
                        + str(i)
                        + "? (Press Y to continue or N to skip)"
                    )
                    if finished_adding == "n":
                        break

    def BuildMapAdjMatrix(self):
        pass
