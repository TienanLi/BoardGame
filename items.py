# TODO: add a full item list, return false if the input is not in the legal list.
kItemList = [
    "water",
    "food",
    "pill",
    "epinephrine",
    "alcohol",
    "gold",
    "knife",
    "gun",
    "shotgun",
    "rope",
    "anti-toxic mask",
    "bazooka",
    "high-dimension pocket",
    "recycling machine",
    "trash",
    "double_knife",
    "double_alcohol",
    "water_and_food",
]
kWeaponDict = {"gun": 2, "knife": 2, "double_knife": 4, "double_gun": 4, "shotgun": 4}


class Item:
    def __init__(self, name):
        self.name_ = name
        self.power_add = 0 if not self.is_weapon(name) else kWeaponDict[name]

    def is_gun(self):
        return "gun" in self.name_

    @staticmethod
    def is_weapon(name):
        return True if name in kWeaponDict else False
