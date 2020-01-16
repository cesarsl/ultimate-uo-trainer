import datetime as dt
import threading

from logger import logger
from stealth import (
    GetSkillCap,
    GetSkillCurrentValue,
    GetSkillValue,
    UseSkill,
)


class Hiding(threading.Thread):
    """Hiding Skill Trainer Thread"""

    def __init__(self, window):
        super(Hiding, self).__init__(daemon=True)
        self._skill = "Hiding"
        self._wait_time = 11
        self._window = window
        self._initial = float(GetSkillValue(self._skill))
        self._current = self._initial
        self._gain = 0.0
        self._value = GetSkillValue(self._skill)
        self._cap = GetSkillCap(self._skill)
        self._running = True
        self._time_start = None
        self._time_now = None
        self._time_wait = None
        self._time_running = None

    def run(self):
        self._time_start = dt.datetime.now()
        while self._running is True:
            self._time_now = dt.datetime.now()
            self._time_wait = self._time_now + dt.timedelta(seconds=self._wait_time)

            UseSkill(self._skill)

            while self._time_wait >= dt.datetime.now():
                self._current = GetSkillValue(self._skill)
                self._time_running = dt.datetime.now() - self._time_start

                self._window.Element("status_bar").Update(
                    f"Running for {int(self._time_running.total_seconds())} seconds"
                )
                self._window.Element("skill_current").Update(
                    GetSkillCurrentValue(self._skill)
                )
                self._window.Element("skill_real").Update(self._current)
                self._window.Element("skill_cap").Update(GetSkillCap(self._skill))

                if self._current > self._initial:
                    self._gain = self._current - self._initial
                self._window.Element("skill_session").Update(
                    "{0:.1f}".format(self._gain)
                )

    def terminate(self):
        self._time_wait = dt.datetime.now()
        self._running = False
        self._window.Element("status_bar").Update("Stopped")
