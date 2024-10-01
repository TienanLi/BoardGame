from items import Item, kWeaponDict

class Player:
    # TODO: assert sum is 10
    def __init__(self, name, power, movement, bag_size):
        self.name_ = name
        self.power_ = power
        self.movement_ = movement
        self.bag_size_ = bag_size
        self.bag_ = []
        self.life_ = 10
        self.use_epinephrine_ = False
        self.is_ghost_ = False
        self.location_ = None

    def StatusString(self):
        print("Player ", self.name_, " current life ", self.life_, " and is a ", "ghost" if self.is_ghost_ else "human")

    def GeneUpgrade(self):
        self.power_ += 1
        self.movement_ += 1
        self.bag_size_ += 1

    def ReAssignGene(self, power, movement, bag_size):
        if power + movement + bag_size != self.power_ + self.movement_ + self.bag_size_:
            print("The new sum of values is not the same of the previous sum of values. Please re-input.\n")
            return False
        if bag_size < len(self.bag_):
            print("The new bag size is smaller than the number of item you already have in hand. Please re-input.\n")
            return False
        self.power_ = power
        self.movement_ = movement
        self.bag_size_ = bag_size
        return True

    def consumeEpinephrine(self):
        self.use_epinephrine_ = True

    def EpinephrineFade(self):
        self.use_epinephrine_ = False

    def ReduceLife(self, num_reduced):
        self.life_ -= num_reduced
        if self.use_epinephrine_:
            self.life_ = max(1, self.life_)
        if self.life_ <= 0:
            self.is_ghost_ = True
            self.life_ = 0

    def IncreaseLife(self, num_increased):
        self.life_ += num_increased
        self.life_ = min(self.life_, 10)
        if (self.is_ghost_ == True and self.life_ >= 2):
            self.is_ghost_ = False

    def ItemIdxInBag(self, item_name):
        for i in range(len(self.bag_)):
            if self.bag_[i].name_ == item_name:
                return i
        return -1

    def ItemInBag(self, item_name):
        return False if self.ItemIdxInBag(item_name) == -1 else True

    def UseItem(self, item_name):
        idx = self.ItemIdxInBag(item_name)
        # DCHECK(idx >= 0)
        self.bag_.pop(idx)
        return True

    def PickItem(self, item_name):
        if len(self.bag_) == self.bag_size_:
            print("Bag is already full. Can not pick this one.\n")
            return False
        self.bag_.append(Item(item_name))
        return True

    def PowerWithWeapon(self):
        temp_power = self.power_
        for item in self.bag_:
            if item.name_ in kWeaponDict:
                temp_power += kWeaponDict[item.name_]
        return temp_power

    def HasGun(self):
        for item in self.bag_:
            if item.is_gun():
                return True
        return False