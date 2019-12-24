import time
import queue
import threading

from stealth import (
    UseSkill,
    ChangeSkillLockState,
    GetSkillCap,
    GetSkillValue,
    GetSkillCurrentValue,
)


class Hiding(threading.Thread):
    def __init__(self, queue, window):
        super(Hiding, self).__init__(daemon=True)
        self._skill = "Hiding"
        self._wait_time = 11
        self._queue = queue
        self._window = window
        self._current = GetSkillCurrentValue("Hiding")
        self._value = GetSkillValue("Hiding")
        self._cap = GetSkillCap("Hiding")
        self._running = True

    def run(self):
        while self._running is True:
            UseSkill(self._skill)
            self._queue.put_nowait("Teste")
            self._window.Element("skill_current").Update(
                GetSkillCurrentValue(self._skill)
            )
            self._window.Element("skill_real").Update(GetSkillValue(self._skill))
            self._window.Element("skill_cap").Update(GetSkillCap(self._skill))
            time.sleep(self._wait_time)

    def terminate(self):
        self._running = False
        self._queue.put("Hiding ended")

