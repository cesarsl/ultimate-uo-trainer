import json
import re
import itertools

from stealth import (
    GetTooltipRec,
    FindTypesArrayEx,
    GetFindedList,
    Ground,
    Backpack,
    Self,
    GetType,
    GetName,
    GetTooltip,
)

CLILOCS = None

with open("../assets/metadata/cliloc.json", "r", encoding="utf-8") as fpointer:
    CLILOCS = json.load(fpointer)


def remove_variables(label):
    pattern = re.compile(r"\s?~[0-9]_.+~%?\s?")
    result = re.sub(pattern, "", label)
    return result


def parse_clilocs(old):
    new_cliloc = {}
    for idx, _cliloc in old.items():
        new_cliloc[idx] = {
            "name": remove_variables(_cliloc.get("original")),
            "raw": _cliloc.get("original"),
        }
    return new_cliloc


def update_file():
    cliloc = parse_clilocs(CLILOCS)

    with open("../assets/metadata/cliloc.json", "w+", encoding="utf-8") as fpointer:
        json.dump(cliloc, fpointer)


def get_item_properties(obj_id):
    # weapon_ids = list(range(1029556, 1029599 + 1))
    # weapon_ids += list(range(1030100, 1030235))
    # handle_ids = [1061824, 1061171]
    # skill_req_ids = list(range(1061172, 1061175 + 1))
    # skill_req_ids += [1112075]

    tooltips = GetTooltipRec(obj_id)
    properties = {}

    for tip in tooltips:
        _id = str(tip.get("Cliloc_ID"))
        _name = CLILOCS.get(_id).get("name")
        _params = tip.get("Params")

        # if int(_id) in weapon_ids:
        #     properties["name"] = _name
        # elif int(_id) in handle_ids:
        #     properties["handle"] = _name
        # elif int(_id) in skill_req_ids:
        #     properties["skill required"] = _name.split(": ")[1]
        if _name == "weapon speed":
            properties[_name] = _params[0][:-1]
        elif _name == "weapon damage":
            properties[_name] = {
                "min": _params[0],
                "max": _params[1],
            }
        elif _name == "durability":
            properties[_name] = {
                "curr": _params[0],
                "total": _params[1],
            }
        else:
            if len(_params) > 0:
                properties[_name] = _params[0]
            else:
                properties[_name] = ""

    return properties


# print(get_item_properties(0x42E2D0E2))


def create_equipment_json():
    _equipments = {}
    with open("../assets/metadata/equipments.json", "r") as fpointer:
        _equipments = json.load(fpointer)

    weapon_ids = list(range(1029556, 1029599 + 1))
    weapon_ids += list(range(1030100, 1030235))

    weapon_names = []
    for idx in weapon_ids:
        indice = str(idx).strip("\n")
        entry = CLILOCS.get(indice)
        if entry != None:
            weapon_names.append(entry.get("name"))

    for weapon in weapon_names:
        _equip = {
            weapon: {"name": str(weapon).title(), "type": "weapon", "type_id": "0x0",}
        }
        _equipments.update(_equip)

    with open("../assets/metadata/equipments.json", "w+") as fpointer:
        json.dump(_equipments, fpointer)


# create_equipment_json()
# print(CLILOCS.get())
# print(CLILOCS.get("1029599"))


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def find_item_types():
    _types = list(range(0x0, 0xFFFF + 1))
    _finded_list = []
    _equipments = {}

    for chunk in chunked_iterable(_types, 255):
        FindTypesArrayEx(chunk, [0xFFFF], [Ground(), Backpack(), Self()], True)
        _finded_list += GetFindedList()

    for item in _finded_list:
        if item != Self():
            _type = hex(GetType(item))
            _tooltip = GetTooltip(item).split("|")
            _name = _tooltip[0].casefold()

            _equipments.update(
                {_name: {"name": _name.title(), "type": "", "type_id": _type}}
            )

    with open("../assets/metadata/equipments.json", "r", encoding="utf-8") as fpointer:
        _old_equipments = json.load(fpointer)

    _old_equipments.update(_equipments)

    with open("../assets/metadata/equipments.json", "w+", encoding="utf-8") as fpointer:
        json.dump(_old_equipments, fpointer)



