import json
import queue
import threading
import PySimpleGUI as sg

from typing import Dict, List

from py_stealth import CharName, GetSkillCap, GetSkillCurrentValue, GetSkillValue

from packages.hiding import Hiding

from gui.app import ASSETS_DEFAULT_FLAG, MAIN_LAYOUT, MAIN_SIZE, MAIN_TITLE

# Constants

ASSETS_SKILLS = "../assets/metadata/skills.json"

# Main App


class UltimateUOTrainer:
    def __init__(self, layout: List) -> None:
        with open(ASSETS_SKILLS, "r") as f:
            self._skills_info = json.load(f)

        self._window = sg.Window(
            title=MAIN_TITLE, size=MAIN_SIZE, layout=layout
        ).Finalize()

        self._combo_list = [
            self._skills_info.get(x).get("name") for x in self._skills_info
        ]
        self._combo_list.insert(0, "Choose a skill...")
        self._window.Element("skill_combo").Update(values=self._combo_list)
        self._window.Element("status_bar").Update(f"Character: {CharName()}")
        self._queue = queue.Queue()
        self._thread = None

    def start(self):
        while True:
            event, values = self._window.read()
            print(event, values)

            if event is None or event == "Exit":
                break

            if event == "skill_combo":
                choice = values.get("skill_combo")
                self._update_requirements(choice)
                self._update_info(choice)

            if event == "Start":
                choice = values.get("skill_combo")
                if choice == "Hiding":
                    self._thread = Hiding(self._queue)
                    self._thread.start()
            
            if event == "Stop":
                if self._thread != None:
                    self._thread.terminate()

            try:
                message = self._queue.get_nowait()
            except queue.Empty:
                message = None

        self._window.close()

    def _update_requirements(self, skill: str) -> None:
        if skill != "Choose a skill...":
            self._window.Element("requirements_text").Update(
                self._skills_info.get(str.lower(skill)).get("requirements")
            )
            self._window.Element("skill_name").Update(
                self._skills_info.get(str.lower(skill)).get("name")
            )
        else:
            self._window.Element("requirements_text").Update(
                "Select a skill before proceeding."
            )
            self._window.Element("skill_name").Update("")

    def _update_info(self, skill: str) -> None:
        if skill != "Choose a skill...":
            self._window.Element("skill_flag").Update(
                filename=self._skills_info.get(str.lower(skill)).get("flag"),
                size=(304, 32),
            )
            self._window.Element("skill_current").Update(GetSkillCurrentValue(skill))
            self._window.Element("skill_real").Update(GetSkillValue(skill))
            self._window.Element("skill_cap").Update(GetSkillCap(skill))
        else:
            self._window.Element("skill_flag").Update(
                filename=ASSETS_DEFAULT_FLAG, size=(304, 32)
            )
            self._window.Element("skill_current").Update("")
            self._window.Element("skill_real").Update("")
            self._window.Element("skill_cap").Update("")


if __name__ == "__main__":
    app = UltimateUOTrainer(MAIN_LAYOUT)
    app.start()
    pass
