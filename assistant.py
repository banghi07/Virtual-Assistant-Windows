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

    # * UI Button Connect
    def ui_button_connect(self):
        self.ui.button_close.clicked.connect(self.close_window)
        self.ui.button_microphone.clicked.connect(self.initial_assistant)

    def close_window(self):
        QCoreApplication.exit()
        self.thread.kill()

    # * Initial Assistant
    def initial_assistant(self):
        self.ui.setupUI_main_window(self.MainWindow)
        playsound("./audio/101_notification.wav", False)
        self.get_text_from_audio_thread(self.user_request)

    def get_location_from_ip(self):
        url = "https://ipinfo.io/"
        response = requests.get(url).json()
        city = response["city"]
        region = response["region"]

        location = response["loc"].split(",")
        lat = location[0]
        lon = location[1]

        result = {"city": city, "region": region, "lat": lat, "lon": lon}
        return result

    # * User Request
    def user_request(self, text):
        delay = ThreadDelay(1, text)
        if "..." in text:
            delay.signals.finished.connect(self.didnt_hear)
        elif "hôm nay" in text or "hiện tại" in text or "bây giờ" in text:
            if "giờ" in text:
                delay.signals.finished.connect(self.get_time_thread)
            elif "ngày" in text or "thứ" in text:
                delay.signals.finished.connect(self.get_date_thread)

        self.threadpool.start(delay)

    # * func_no1:
    def didnt_hear(self):
        url = "./icon/mute-microphone-256px.png"
        text = "Xin lỗi tôi không nghe rõ bạn nói gì."
        self.ui.setupUI_simple_window(self.MainWindow, url, text)
        self.speak_thread("001")

    # * func_no2:
    def get_time_thread(self):
        self.thread = Thread(self.get_time, "get_time")
        self.thread.signals.running.connect(self.update_thread_list)
        self.thread.signals.result.connect(self.get_time_complete)
        self.threadpool.start(self.thread)

    def get_time(self):
        location = self.get_location_from_ip()

        api = "BL83E6LF3XI3"
        url = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}"
        response = requests.get(
            url.format(api, location["lat"], location["lon"])
        ).json()

        u = int(response["gmtOffset"]) / 3600
        if u >= 0:
            utc = "+" + "{:.0f}".format(u)
        else:
            utc = str("{:.0f}".format(u))

        t = response["formatted"]
        year = t[0:4]
        month = t[5:7]
        day = t[8:10]
        hour = t[11:13]
        minute = t[14:16]
        second = t[17:19]

        result = {
            "city": location["city"],
            "zone_name": response["zoneName"],
            "utc": utc,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
        }

        return result

    def get_time_complete(self, result):
        speech = "Hiện tại là {} giờ {} phút {} giây.".format(
            result["hour"], result["minute"], result["second"]
        )

        self.ui.setupUI_clock_window(self.MainWindow, result)
        self.speak_thread(speech)

    def get_date_thread(self):
        self.thread = Thread(self.get_time, "get_date")
        self.thread.signals.running.connect(self.update_thread_list)
        self.thread.signals.result.connect(self.get_date_complete)
        self.threadpool.start(self.thread)

    def get_date(self):
        location = self.get_location_from_ip()

        api = "BL83E6LF3XI3"
        url = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}"
        response = requests.get(
            url.format(api, location["lat"], location["lon"])
        ).json()

        u = int(response["gmtOffset"]) / 3600
        if u >= 0:
            utc = "+" + "{:.0f}".format(u)
        else:
            utc = str("{:.0f}".format(u))

        t = response["formatted"]
        year = t[0:4]
        month = t[5:7]
        day = t[8:10]
        hour = t[11:13]
        minute = t[14:16]
        second = t[17:19]

        result = {
            "city": location["city"],
            "zone_name": response["zoneName"],
            "utc": utc,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
        }

        return result

    def get_date_complete(self, result):
        speech = "Hôm nay là ngày {} tháng {} năm {}".format(
            result["day"], result["month"], result["year"]
        )

        self.ui.setupUI_date_window(self.MainWindow, result)
        self.speak_thread(speech)


if __name__ == "__main__":
    Assistant()
