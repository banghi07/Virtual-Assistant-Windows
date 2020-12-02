# import ctypes
# import datetime
# import json
# import os
# import re
# import smtplib
import sys

# import time
# import traceback
# import urllib
# import urllib.request as urllib2
# import webbrowser
# from time import strftime

# import feedparser
# import pyperclip
# import requests
# import speech_recognition as sr
# import wikipedia
# from fast_youtube_search import search_youtube
# from geopy.geocoders import Nominatim
# from googleapiclient.discovery import build
# from googletrans import Translator
# from gtts import gTTS, gTTSError
# from playsound import playsound
# from pynput import keyboard, mouse
# from pynput.keyboard import Controller, Key
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from youtube_search import YoutubeSearch

from assistant_sys_tray_icon import *
from assistant_threads import *


class Assistant(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        tray_icon = SystemTrayIcon(self.widget)
        tray_icon.activated.connect(self.tray_icon_activate)

        self.set_main_window()

        self.show()

    def tray_icon_activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def center_screen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_main_window(self):
        self.setWindowTitle("Virtual Assistant - PyQt5")
        self.setFixedSize(500, 350)
        self.center_screen()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setStyleSheet(open("./themes/dark.css").read())

        widget = QWidget()
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = Assistant()
    sys.exit(app.exec_())