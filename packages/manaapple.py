import datetime as dt
import threading

from stealth import UseObject, Wait


class ManaApple(threading.Thread):
    def __init__(self):
        super(ManaApple, self).__init__(daemon=True)
        self._running = True
        self._start_time = None
        self._stop_time = None

    def run(self):
        while self._running is True:
            UseObject(0000000000)  # ID da maça ou findtype, não sei
            self._start_time = dt.datetime.now()
            self._stop_time = self._start_time + dt.timedelta(seconds=11)
            while self._stop_time > self._stop_time:
                Wait(1)

    def terminate(self):
        self._running = False
