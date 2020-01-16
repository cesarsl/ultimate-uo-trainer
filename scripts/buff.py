import json

from stealth import Cast, GetBuffBarInfo, GetExtInfo, GetMana, Self


with open("../assets/metadata/magic.json") as doc:
    magic_list = json.load(doc)


def cast_buff(magic):
    buffs = GetBuffBarInfo()
    mana_curr = GetMana(Self())
    lmc_curr = GetExtInfo.get("Lower_Mana_Cost")
    mana_cost = (lmc_curr * magic_list.get("magic").get("mana_min")) / 100

    if len(buffs) != 0:
        buff = buff_info(magic, buffs)
        if buff:
            if buff.get("Seconds") <= 1:
                if mana_curr > mana_cost:
                    Cast(magic)
    else:
        if mana_curr > mana_cost:
            Cast(magic)



def buff_info(name, buffs):
    for buff in buffs:
        buff_id = buff.get("Attribute_ID")
        buff_cd = buff.get("Seconds")

        if buff_id == magic_list.get("name").get("id"):
            return buff
        
        return None
        
