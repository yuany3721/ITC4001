from time import sleep, time
from datetime import datetime
import threading


class Timer(object):

    def __init__(self, function, interval: int, *args, **kwargs):
        self._timer = None
        # function to run
        self.function = function
        # running interval ms
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.isRunning = False
        self.nextCall = time()

    def _run(self):
        self.isRunning = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.isRunning:
            self.nextCall += self.interval/1000.0
            self._timer = threading.Timer(self.nextCall - time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.isRunning = False


if __name__ == "__main__":
    def test():
        print(datetime.now())

    tt = Timer(test, 50)
    try:
        tt.start()
        sleep(2)
    finally:
        tt.stop()
