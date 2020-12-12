from PyQt5.QtCore import *
import time
import traceback
import sys


class WorkerKillException(Exception):
    pass


class ThreadSignals(QObject):
    running = pyqtSignal(str, int)
    finished = pyqtSignal()
    error = pyqtSignal()
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
        try:
            self.signals.running.emit(self.thread_name, 1)
            result = self.fn(*t, **self.kwargs)

            if self.is_kill:
                raise WorkerKillException

        except WorkerKillException:
            pass
        except:
            self.signals.error.emit()
        else:
            self.signals.result.emit(result)
            self.signals.running.emit(self.thread_name, 0)
            self.signals.finished.emit()

    def kill(self):
        self.is_kill = True


class ThreadDSignals(QObject):
    running = pyqtSignal(str, int)
    result = pyqtSignal(object)


class ThreadD(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.thread_name = list(self.args)[-1]
        self.signals = ThreadDSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        l.pop()
        t = tuple(l)
        while True:
            if self.is_kill:
                break
            self.signals.running.emit(self.thread_name, 1)
            result = self.fn(*t, **self.kwargs)
            self.signals.result.emit(result)
            self.signals.running.emit(self.thread_name, 0)

    def kill(self):
        self.is_kill = True


class ThreadDelaySignals(QObject):
    finished = pyqtSignal()


class ThreadDelay(QRunnable):
    def __init__(self, time_delay):
        super().__init__()
        self.time_delay = time_delay
        self.signals = ThreadDelaySignals()

    @pyqtSlot()
    def run(self):
        time.sleep(self.time_delay)
        self.signals.finished.emit()
