import json

CLILOC = {}

SKILLS_REQ = [1061172, 1061173, 1061174, 1061175, 1112075]

MATERIALS = [1071428, 1071429, 1071430, 1071431, 1071432, 1071433]

SLAYERS = [
    1060457,
    1060458,
    1060459,
    1060460,
    1060461,
    1060462,
    1060463,
    1060464,
    1060465,
    1060466,
    1060467,
    1060468,
    1060469,
    1060470,
    1060471,
    1060472,
    1060473,
    1060474,
    1060475,
    1060476,
    1060477,
    1060478,
    1060479,
    1060480,
]

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
    "crafted by",
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
    "exceptional",
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
    "material",
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

NAMES = [
    1061248,
    1030146,
    1030147,
    1030148,
    1030151,
    1030153,
    1030155,
    1030156,
    1030157,
    1030159,
    1025040,
    1025046,
    1025049,
    1025177,
    1025179,
    1029914,
    1025181,
    1025182,
    1029915,
    1029916,
    1025185,
    1029917,
    1025187,
    1029918,
    1023909,
    1029919,
    1023911,
    1029920,
    1023913,
    1029921,
    1023915,
    1023917,
    1023922,
    1060024,
    1023932,
    1023934,
    1023937,
    1023938,
    1061593,
    1061594,
    1061595,
    1061596,
    1061597,
    1061598,
    1061599,
    1061600,
    1025115,
    1025119,
    1025121,
    1025123,
    1025125,
    1061088,
    1025127,
    1061601,
    1061106,
    1061107,
    1061108,
    1061109,
    1061110,
    1061111,
    1060860,
]

HANDLING = [1061171, 1061824]

BOOLEANS = [
    1061682,
    1060636,
    1060400,
]

with open("../assets/metadata/cliloc.json", "r", encoding="utf-8") as fpointer:
    CLILOC.update(json.load(fpointer))
