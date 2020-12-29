import sys
import time
import traceback

import requests
from PyQt5.QtCore import *


class WorkerKillException(Exception):
    pass


class LostInternetConnection(Exception):
    pass


class ThreadSignals(QObject):
    finished = pyqtSignal()
    error_internet = pyqtSignal(int)
    result = pyqtSignal(object)


class Thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        url = "http://www.google.com/"
        try:
            try:
                response = requests.get(url, timeout=2)
            except TimeoutError:
                self.signals.error_internet.emit(1)
            except:
                self.signals.error_internet.emit(1)
            else:
                try:
                    result = self.fn(*self.args, **self.kwargs)

                    if self.is_kill:
                        raise WorkerKillException

                except WorkerKillException:
                    pass
                else:
                    self.signals.result.emit(result)
                    self.signals.finished.emit()
        except:
            pass

    def kill(self):
        self.is_kill = True


class ThreadTransSignals(QObject):
    result = pyqtSignal(object)
    error_internet = pyqtSignal(int)


class ThreadTrans(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.signals = ThreadTransSignals()

    @pyqtSlot()
    def run(self):
        url = "http://www.google.com/"
        try:
            try:
                response = requests.get(url, timeout=2)
            except TimeoutError:
                self.signals.error_internet.emit(1)
            except:
                self.signals.error_internet.emit(1)
            else:
                while True:
                    result = self.fn(*self.args, **self.kwargs)
                    if self.is_kill:
                        break
                    else:
                        self.signals.result.emit(result)
        except:
            pass

    def kill(self):
        self.is_kill = True


class ThreadDelaySignals(QObject):
    args = pyqtSignal(object)
    finished = pyqtSignal()
    error_internet = pyqtSignal(int)


class ThreadDelay(QRunnable):
    def __init__(self, time_delay, *args):
        super().__init__()
        self.time_delay = time_delay
        self.args = args
        self.signals = ThreadDelaySignals()

    @pyqtSlot()
    def run(self):
        try:
            time.sleep(self.time_delay)
            self.signals.finished.emit()
            if len(self.args) > 0:
                self.signals.args.emit(*self.args)
        except:
            pass
