import json
import itertools

from stealth import (
    GetExtInfo,
    ClientRequestObjectTarget,
    WaitForClientTargetResponse,
    GetTooltipRec,
    LastTarget,
    GetClilocByID,
    FindTypeEx,
    FindTypesArrayEx,
    GetFindedList,
    Backpack,
    Ground,
    Self,
    UseSkill,
    GetSkillID,
)


def item_to_dict(object_id):
    tooltips = GetTooltipRec(object_id)

    clilocs_ids = []
    clilocs_txt = []

    for tooltip in tooltips:
        clilocs_ids.append(str(tooltip.get("Cliloc_ID")))

    for cliloc_id in clilocs_ids:
        clilocs_txt.append(GetClilocByID(cliloc_id))

    clicoc_dict = dict(zip(clilocs_ids, clilocs_txt))

    return clicoc_dict


def examine_container(container_id):
    with open("../assets/metadata/equipments.json", "r") as file_descriptor:
        equipments = json.load(file_descriptor)

    found_items = []
    for name in equipments:
        FindTypeEx(int(equipments[name].get("type"), 16), 0xFFFF, container_id)
        found_items = found_items + GetFindedList()

    items_description = {}

    for item_id in found_items:
        items_description[item_id] = item_to_dict(item_id)

    return items_description


def save_to_file(old_clilocs, new_clilocs):
    _clilocs = {}
    for idx, text in new_clilocs.items():
        _clilocs[str(idx)] = text
    # print(len(old_clilocs))
    old_clilocs.update(_clilocs)
    # print(len(old_clilocs))
    with open("../assets/metadata/clilocs.json", "w+") as file_descriptor:
        json.dump(old_clilocs, file_descriptor)


def load_from_file():
    _clilocs = {}

    with open("../assets/metadata/clilocs.json", "r") as file_descriptor:
        _clilocs.update(json.load(file_descriptor))

    return _clilocs


def find_all_items():
    start = int("0x0", 16)
    end = int("0xffff", 16) + 1

    item_ids = []
    item_types = []

    for i in range(start, end):
        item_types.append(i)

    for chunk in chunked_iterable(item_types, 255):
        FindTypesArrayEx(chunk, [0xFFFF], [Ground(), Backpack(), Self()], True)
        item_ids += GetFindedList()

    return item_ids


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


def find_all_clilocs():
    start = int("0x7a120", 16)
    end = int("0x2df1d8", 16) + 1

    clilocs_dict = {}
    for i in range(start, end, 1):
        text = GetClilocByID(i)
        if text != "":
            print(i, text)
            clilocs_dict[str(i)] = {"original": text}
        else:
            print(i, "[empty]")

    return clilocs_dict


file_clilocs = load_from_file()
scan_clilocs = find_all_clilocs()
save_to_file(file_clilocs, scan_clilocs)
