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
    def __init__(self, obj_id):
        self.obj_id = int(obj_id, 16)
        self.cliloc = {}

        with open("../assets/metadata/cliloc.json", "r", encoding="utf-8") as fpointer:
            self.cliloc.update(json.load(fpointer))

        for prop in PROPERTIES:
            setattr(self, prop.replace(" ", "_"), None)

        self.tooltips = stealth.GetTooltipRec(self.obj_id)

        for tip in self.tooltips:
            cliloc_id = str(tip.get("Cliloc_ID"))
            cliloc_params = tip.get("Params")
            prop_key = self.cliloc.get(cliloc_id).get("name").replace(" ", "_")
            prop_params = []
            for param in cliloc_params:
                prop_params.append(self.param_parser(param))

            if prop_key == "weapon_speed":
                print(prop_key, prop_params)
                setattr(self, prop_key, prop_params[0])
            elif prop_key != "":
                if len(prop_params) == 1:
                    setattr(self, prop_key, prop_params[0])

    def param_parser(self, param):
        if "#" in param:
            return self.cliloc.get(param[1:]).get("name")
        if param.isdigit():
            return int(param)
        if re.match(r"[0-9]+\.?[0-9]+s|[0-9]s", param):
            return float(param.replace("s", ""))
        return str(param)

    def props(self):
        props = {}
        for prop in PROPERTIES:
            prop_key = prop.replace(" ", "_")
            props.update({prop_key: getattr(self, prop_key)})

        return props


equip_01 = Item("0x42E2D0E2")
print(equip_01.weapon_speed)
# equip_02 = Item("0x4070D4B7")
# print(equip_02.weapon_speed)

equip_03 = Item("0x415B7910")
print(equip_03.weapon_speed)
print(equip_03.props())
