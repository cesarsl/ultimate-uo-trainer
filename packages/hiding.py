import time
import queue
import datetime as dt
import threading

from stealth import (
    UseSkill,
    ChangeSkillLockState,
    GetSkillCap,
    GetSkillValue,
    GetSkillCurrentValue,
)


class Hiding(threading.Thread):
    def __init__(self, window):
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
        self._start_time = dt.datetime.now()
        while self._running is True:
            self._timeout_start = dt.datetime.now()
            self._timeout_end = self._timeout_start + dt.timedelta(
                seconds=self._wait_time
            )
            UseSkill(self._skill)
            while self._timeout_end >= dt.datetime.now():
                self._now = dt.datetime.now()
                self._running_time = self._now - self._start_time
                self._window.Element("status_bar").Update(
                    f"Running for {int(self._running_time.total_seconds())} seconds"
                )
                self._window.Element("skill_current").Update(
                    GetSkillCurrentValue(self._skill)
                )
                self._window.Element("skill_real").Update(GetSkillValue(self._skill))
                self._window.Element("skill_cap").Update(GetSkillCap(self._skill))

    def terminate(self):
        self._timeout_end = dt.datetime.now()
        self._running = False
        self._window.Element("status_bar").Update("Stopped")

