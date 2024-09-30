class Player:
    # TODO: assert sum is 10
    def __init__(self, name, power, movement, bag_size):
        self.name_ = name
        self.power_ = power
        self.movement_ = movement
        self.bag_size_ = bag_size
        self.bag_ = []
        self.life_ = 10
        self.is_ghost_ = False

    def StatusString(self):
        print("Player ", self.name_, " current life ", self.life_, " and is a ", "ghost" if self.is_ghost_ else "human")

    def GeneUpgrade(self):
        self.power_ += 1
        self.movement_ += 1
        self.bag_size_ += 1

    # TODO: assert total the same as previous
    # TODO: assert bag_size does not exceed current num of items in bag
    def ReAssignGene(self, power, movement, bag_size):
        self.power_ = power
        self.movement_ = movement
        self.bag_size_ = bag_size

    def ReduceLife(self, num_reduced):
        self.life_ -= num_reduced
        if (self.life_ <= 0):
            self.is_ghost_ = True
            self.life_ = 0

    def IncreaseLife(self, num_increased):
        self.life_ += num_increased
        if (self.is_ghost_ == True and self.life_ >= 2):
            self.is_ghost_ = False
