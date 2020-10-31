import sys
import threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from mainwindow import Ui_MainWindow
import os
from playsound import playsound
import speech_recognition as sr
import time
import sys
import wikipedia
import datetime
import json
import re
import webbrowser
import requests
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch

class thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(thread, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class assistant():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.updateWidgets()
        self.callAssistant()
        self.MainWindow.show()
        sys.exit(app.exec_())

    def updateWidgets(self):
        self.MainWindow.setWindowTitle('Virtual Assistant- PyQT5')

    def callAssistant(self):
        self.ui.pushButton.pressed.connect(self.assistant)

    def assistant(self):
        self.threadpool = QThreadPool()
        self.ui.plainTextEdit.setPlainText("Xin Chào!")
        thread1 = thread(self.speak, "Xin Chào!")
        self.threadpool.start(thread1)
      
    def speak(self, text):
        tts = gTTS(text=text, lang="vi", slow=False)
        tts.save("sound.mp3")
        playsound("sound.mp3", False)
        os.remove("sound.mp3")


if __name__ == "__main__":
    assistant()

