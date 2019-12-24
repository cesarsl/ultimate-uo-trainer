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
    def __init__(self, queue):
        super(Hiding, self).__init__()
        self._queue = queue
        self._current = GetSkillCurrentValue("Hiding")
        self._value = GetSkillValue("Hiding")
        self._cap = GetSkillCap("Hiding")
        self._running = True

    def run(self):
        while self._running is True:
            UseSkill("Hiding")
            time.sleep(7)

    def terminate(self):
        self._running = False
        if self._queue:
            self._queue.put("DONE")

