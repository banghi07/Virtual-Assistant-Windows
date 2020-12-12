import ctypes
import datetime
import json
import os
import re
import smtplib
import sys
import time
import traceback
import urllib
import urllib.request as urllib2
import webbrowser
from time import strftime

import feedparser
import pyperclip
import requests
import speech_recognition as sr
import wikipedia
from fast_youtube_search import search_youtube
from geopy.geocoders import Nominatim
from googleapiclient.discovery import build
from googletrans import Translator
from gtts import gTTS, gTTSError
from playsound import playsound
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key
from PyQt5.QtWidgets import *
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from youtube_search import YoutubeSearch

from assistant_threads import *
from assistant_window import *


class Assistant:
    def __init__(self):
        app = QApplication(sys.argv)

        self.threadpool = QThreadPool()
        self.thread_list = []

        self.MainWindow = Window()
        self.ui = UI_Windows()
        self.ui_button_connect()
        self.initial_assistant()

        sys.exit(app.exec_())

    def update_thread_list(self, text, status):
        if status:
            self.thread_list.append(text)
        else:
            self.thread_list.remove(text)
        print(self.thread_list)

    def speak_thread(self, text):
        if text.isnumeric():
            s = "play_sound_" + text
            self.thread = Thread(self.play_sound, text, s)
            self.thread.signals.running.connect(self.update_thread_list)
            self.threadpool.start(self.thread)
        else:
            self.thread = Thread(self.speak, text, "speak")
            self.thread.signals.running.connect(self.update_thread_list)
            self.threadpool.start(self.thread)

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang="vi", slow=False)
            tts.save("./audio/sound.mp3")
            playsound("./audio/sound.mp3", False)
            os.remove("./audio/sound.mp3")
        except:
            print("Error: Token Google Translate. Try again...")
            os.remove("./audio/sound.mp3")
            self.speak(text)

    def play_sound(self, code):
        if "001" in code:
            playsound("./audio/001_none.mp3")
        elif "002" in code:
            playsound("./audio/002_help_me.mp3")
        elif "003" in code:
            playsound("./audio/003_good_mor.mp3")
        elif "004" in code:
            playsound("./audio/004_good_aft.mp3")
        elif "005" in code:
            playsound("./audio/005_good_night.mp3")
        elif "006" in code:
            playsound("./audio/006_play_song.mp3")
        elif "007" in code:
            playsound("./audio/007_wikipedia.mp3")
        elif "008" in code:
            playsound("./audio/008_open_app.mp3")
        elif "009" in code:
            playsound("./audio/009_open_web.mp3")

    def get_text_from_audio_thread(self, function):
        self.thread = Thread(self.speech_recognition, "speech_recognition")
        self.thread.signals.running.connect(self.update_thread_list)
        self.thread.signals.result.connect(self.ui.update_bottom_bar)
        self.thread.signals.result.connect(self.user_request)
        self.threadpool.start(self.thread)

    def speech_recognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                return text.lower()
            except:
                return "..."

    def close_window(self):
        self.thread.kill()
        QCoreApplication.exit()

    def ui_button_connect(self):
        self.ui.button_close.clicked.connect(self.close_window)
        self.ui.button_microphone.clicked.connect(self.initial_assistant)

    def initial_assistant(self):
        self.ui.setupUI_main_window(self.MainWindow)
        playsound("./audio/101_notification.wav", False)
        self.get_text_from_audio_thread(self.user_request)

    def user_request(self, text):
        delay = ThreadDelay(1)
        if "..." in text:
            delay.signals.finished.connect(self.didnt_hear)

        self.threadpool.start(delay)

    def didnt_hear(self):
        url = "./icon/mute-microphone-256px.png"
        text = "Xin lỗi tôi không nghe rõ bạn nói gì."
        self.ui.setupUI_simple_window(self.MainWindow, url, text)
        self.speak_thread("001")


if __name__ == "__main__":
    Assistant()
