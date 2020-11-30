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
        super(Thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.thread_name = list(self.args)[-1]
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        # time.sleep(l[-1])
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
        finally:
            self.signals.running.emit(self.thread_name, 0)
            self.signals.finished.emit()

    def kill(self):
        self.is_kill = True


# ? Thead riêng tạm thời cho function dictionary (sử dụng vòng lặp while True)
# TODO thêm tính năng khi thoát phần mềm thì kill Thread translate đi vì translate dùng while True
class ThreadDSignals(QObject):
    running = pyqtSignal(str, int)
    result = pyqtSignal(object)


class ThreadD(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(ThreadD, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_kill = False
        self.thread_name = list(self.args)[-1]
        self.signals = ThreadDSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        # # time.sleep(l[-1])
        l.pop()
        t = tuple(l)
        while True:
            self.signals.running.emit(self.thread_name, 1)
            result = self.fn(*t, **self.kwargs)
            self.signals.result.emit(result)
            self.signals.running.emit(self.thread_name, 0)
            if self.is_kill:
                raise WorkerKillException

    def kill(self):
        self.is_kill = True