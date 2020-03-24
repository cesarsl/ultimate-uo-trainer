import itertools
import json

import stealth

from packages.items import Item

# equip_02 = Item("0x415B7910")
# print(equip_02.weapon_speed)
# print(equip_02.type)
# print(equip_02.material)

# print(stealth.GetTooltipRec(0x40000108))
# equip_01 = Item("0x40000108")
# print(equip_01.all_props)

# print(stealth.GetTooltipRec(0x40000105))
# equip_02 = Item("0x40000105")
# print(equip_02.all_props)


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def find_item_types(container):
    _types = list(range(int("0x0", 16), int("0xFFFF", 16) + 1))
    _finded_list = []
    _equipments = {}

    for chunk in chunked_iterable(_types, 255):
        stealth.FindTypesArrayEx(chunk, [0xFFFF], [container.get("ID")], True)
        _finded_list += stealth.GetFindedList()

    return _finded_list
    # for item in _finded_list:
    #     if item != Self():
    #         _type = hex(GetType(item))
    #         _tooltip = GetTooltip(item).split("|")
    #         _name = _tooltip[0].casefold()

    #         _equipments.update(
    #             {_name: {"name": _name.title(), "type": "", "type_id": _type}}
    #         )

    # with open("../assets/metadata/equipments.json", "r", encoding="utf-8") as fpointer:
    #     _old_equipments = json.load(fpointer)

    # _old_equipments.update(_equipments)

    # with open("../assets/metadata/equipments.json", "w+", encoding="utf-8") as fpointer:
    #     json.dump(_old_equipments, fpointer)


stealth.ClientRequestObjectTarget()

while not stealth.ClientTargetResponsePresent():
    stealth.Wait(1)

items = find_item_types(stealth.ClientTargetResponse())

equipments = {}

for item in items:
    tmp = Item(hex(item))
    equipments.update(
        {
            tmp.name.casefold().replace(" ", "_"): {
                "name": tmp.name,
                "type": "weapon",
                "type_id": tmp.type_id,
            }
        }
    )

with open("../assets/metadata/equipments.json", "r") as fpointer:
    old_equipments = json.load(fpointer)

old_equipments.update(equipments)

with open("../assets/metadata/equipments.json", "w+", encoding="utf-8") as fpointer:
    json.dump(old_equipments, fpointer)

saferoom = {
    "positions": [
        {"x_ini": 498, "x_end": 501, "y_ini": 364, "y_end": 374,},
        {"x_ini": 488, "x_end": 497, "y_ini": 364, "y_end": 379,},
        {"x_ini": 479, "x_end": 487, "y_ini": 364, "y_end": 376,},
    ],
}
