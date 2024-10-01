# TODO: add a full item list, return false if the input is not in the legal list.
kWeaponDict = {"gun": 2, "knife": 2, "double_knife": 4, "double_gun": 4, "shotgun": 4}

class Item:
    def __init__(self, name):
        self.name_ = name
        self.power_add = 0 if not self.is_weapon(name) else kWeaponDict[name]

    def is_gun(self):
        return "gun" in self.name_

    @staticmethod
    def is_weapon(self, name):
        return True if name in kWeaponDict else False