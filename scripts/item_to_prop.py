import re

import stealth

from assets.metadata.cliloc import CLILOC, SKILLS_REQ, SLAYERS, HANDLE, NAMES, BOOLEANS


class Item:
    def __init__(self, obj_id):
        self.obj_id = int(obj_id, 16)
        self._tooltips = stealth.GetTooltipRec(self.obj_id)
        self.properties = {}

        for tip in self._tooltips:
            cliloc_id = str(tip.get("Cliloc_ID"))
            cliloc_params = tip.get("Params")
            prop_key = re.sub(
                re.compile(r"<.*?>"),
                "",
                CLILOC.get(cliloc_id).get("name").replace(" ", "_").casefold(),
            )
            prop_params = []
            for param in cliloc_params:
                prop_params.append(self._param_parser(param))

            if cliloc_id == "1053099":
                setattr(self, "material", prop_params[0])
                setattr(self, "type", prop_params[1])
            elif cliloc_id == "1072789":
                setattr(self, "weight", prop_params[0])
            elif int(cliloc_id) in BOOLEANS:
                setattr(self, prop_key, True)
            elif int(cliloc_id) in NAMES:
                setattr(self, "name", prop_key.replace("_", " ").title())
            elif int(cliloc_id) in SLAYERS:
                setattr(self, "slayer", prop_key.split("_")[0])
            elif int(cliloc_id) in SKILLS_REQ:
                setattr(
                    self,
                    "skill_required",
                    CLILOC.get(cliloc_id).get("name").split(": ")[1],
                )
            elif int(cliloc_id) in HANDLE:
                setattr(
                    self,
                    "handling",
                    CLILOC.get(cliloc_id).get("name").replace("_", " "),
                )
            elif cliloc_id == "1060639":
                setattr(
                    self,
                    "durability",
                    {"current": prop_params[0], "total": prop_params[1]},
                )
            elif prop_key != "":
                print(prop_key, prop_params)
                if len(prop_params) == 1:
                    setattr(self, prop_key, prop_params[0])

        self._collect_props()

    def _param_parser(self, param):
        if "#" in param:
            return CLILOC.get(param[1:]).get("name")
        if param.isdigit():
            return int(param)
        if re.match(r"[0-9]+[\.\,]?[0-9]+s|[0-9]+s", param):
            return float(param.replace("s", "").replace(",", "."))
        return str(param)

    def _collect_props(self):
        props = {}
        attributes = [
            attr
            for attr in dir(self)
            if not attr.startswith("_")
            and getattr(self, attr) is not None
            and attr != "all_props"
            and attr != "properties"
        ]
        for attr in attributes:
            props.update({attr: getattr(self, attr)})
        self.properties = props

    @property
    def all_props(self):
        return self.properties


# equip_02 = Item("0x415B7910")
# print(equip_02.weapon_speed)
# print(equip_02.type)
# print(equip_02.material)

print(stealth.GetTooltipRec(0x40000108))
equip_01 = Item("0x40000108")
print(equip_01.all_props)

print(stealth.GetTooltipRec(0x40000105))
equip_02 = Item("0x40000105")
print(equip_02.all_props)
