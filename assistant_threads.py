from PyQt5.QtCore import *
import time
import traceback
import sys
import requests


class WorkerKillException(Exception):
    pass


class LostInternetConnection(Exception):
    pass


class ThreadSignals(QObject):
    running = pyqtSignal(str, int)
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
        self.thread_name = list(self.args)[-1]
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        l.pop()
        t = tuple(l)
        url = "http://www.google.com/"
        try:
            try:
                response = requests.get(url)
            except:
                self.signals.error_internet.emit(1)
            else:
                try:
                    self.signals.running.emit(self.thread_name, 1)
                    result = self.fn(*t, **self.kwargs)

                    if self.is_kill:
                        raise WorkerKillException

                except WorkerKillException:
                    pass
                else:
                    self.signals.result.emit(result)
                    self.signals.running.emit(self.thread_name, 0)
                    self.signals.finished.emit()
        except:
            pass

    def kill(self):
        self.is_kill = True


class ThreadTransSignals(QObject):
    running = pyqtSignal(str, int)
    result = pyqtSignal(object)
    error_internet = pyqtSignal(int)


class ThreadTrans(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.thread_name = list(self.args)[-1]
        self.signals = ThreadTransSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        l.pop()
        t = tuple(l)
        url = "http://www.google.com/"
        try:
            try:
                response = requests.get(url)
            except:
                self.signals.error_internet.emit(1)
            else:
                while True:
                    self.signals.running.emit(self.thread_name, 1)
                    result = self.fn(*t, **self.kwargs)
                    self.signals.running.emit(self.thread_name, 0)
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
