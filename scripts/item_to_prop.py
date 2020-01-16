import json
import re

import stealth

PROPERTIES = [
    "antique",
    "assassin honed",
    "balanced",
    "bane",
    "battle lust",
    "berserk",
    "blood drinker",
    "bone breaker",
    "brittle",
    "casting focus",
    "chaos damage",
    "craft bonus",
    "craft exceptional bonus",
    "curse removal",
    "cursed",
    "damage",
    "damage eater",
    "damage increase",
    "damage modifier",
    "defense chance increase",
    "dexterity bonus",
    "durability",
    "durability bonus",
    "enhance potions",
    "faster cast recovery",
    "faster casting",
    "hit area damage",
    "hit chance increase",
    "hit curse",
    "hit dispel",
    "hit fatigue",
    "hit fireball",
    "hit harm",
    "hit life leech",
    "hit lightning",
    "hit lower attack",
    "hit lower defense",
    "hit magic arrow",
    "hit mana drain",
    "hit mana leech",
    "hit point increase",
    "hit point regeneration",
    "hit stamina leech",
    "intelligence bonus",
    "last parry chance",
    "lower ammo cost",
    "lower mana cost",
    "lower reagent cost",
    "lower requirements",
    "luck",
    "mage armor",
    "mage weapon",
    "mana increase",
    "mana phase",
    "mana regeneration",
    "massive",
    "night sight",
    "prized",
    "random killer",
    "random protection",
    "random summoner",
    "reactive paralyze",
    "reflect physical damage",
    "replenish charges",
    "resist",
    "resonance",
    "self repair",
    "skill bonus",
    "slayer",
    "soul charge",
    "sparks",
    "spell channeling",
    "spell damage increase",
    "spell focusing",
    "splintering weapon",
    "stamina increase",
    "stamina regeneration",
    "strength bonus",
    "strength requirement",
    "swarm",
    "swing speed increase",
    "unwieldy",
    "use best weapon skill",
    "velocity",
    "ward removal",
    "weapon speed",
    "weight",
    "weight reduction",
    "wildfire removal",
]


class Item:
    def __init__(self):
        self.properties = {}
        for prop in PROPERTIES:
            self.properties.update({prop: None})

    def get_prop(self, name):
        print(self.properties.get(name))

    def set_prop(self, name, value):
        self.properties.update({name: value})

    def print_props(self):
        for idx, prop in self.properties.items():
            print(idx, prop)


def item_to_dict(obj_id):
    cliloc = {}

    with open("../assets/metadata/cliloc.json", "r", encoding="utf-8") as fpointer:
        cliloc.update(json.load(fpointer))

    tooltips = stealth.GetTooltipRec(int(obj_id, 16))

    item = Item()

    for tip in tooltips:
        cliloc_id = str(tip.get("Cliloc_ID"))
        cliloc_params = tip.get("Params")

        key = cliloc.get(cliloc_id)
        params = []

        for param in cliloc_params:
            params.append(param_parser(cliloc, param))

        if key == "weapon speed":
            print(key, params)
            item.set_prop("weapon speed", params[0])

    print(item.print_props())


def param_parser(cloc, param):
    if "#" in param:
        return cloc.get(param[1:]).get("name")
    if param.isdigit():
        return int(param)
    if re.match(r"\d.?\d+?s", param):
        return float(param.replace("s", ""))
    return str(param)


item_to_dict("0x42E2D0E2")
# item_to_dict("0x4070D4B7")
# item_to_dict("0x415B7910")
