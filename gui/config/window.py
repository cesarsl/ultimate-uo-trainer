import os
from typing import Dict, Tuple

TITLE: str = "Ultimate UO Trainer v1.0"
SIZE: Tuple[int, int] = (640, 480)
TEXTS: Dict[str, str] = {
    "default_requirements": "Select a skill before proceding.",
    "default_skill_name": "",
    "default_skill_current": "",
    "default_skill_real": "",
    "default_skill_cap": "",
    "default_skill_session": "",
}
IMAGES: Dict[str, str] = {
    "default_flag": "../assets/img/flag_blank.png",
}

print(os.curdir)
