# define all sorts of items.

kWeaponDict = {"gun": 2, "knife": 2, "double_knife": 4, "double_gun": 4, "shotgun": 4}

class Item:
    def __init__(self, name):
        self.name_ = name
        self.power_add = 0 if name not in kWeaponDict else kWeaponDict[name]

    def is_gun(self):
        return "gun" in self.name_