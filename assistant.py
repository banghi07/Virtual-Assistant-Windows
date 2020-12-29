import ctypes
import json
import os
import re
import sys
import traceback
import webbrowser

import feedparser
import pyperclip
import requests
import speech_recognition as sr
import wikipedia
from fast_youtube_search import search_youtube
from geopy.geocoders import Nominatim
from googletrans import Translator
from gtts import gTTS, gTTSError
from playsound import playsound
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key
from PyQt5.QtWidgets import *
from youtube_search import YoutubeSearch

from assistant_threads import *
from assistant_window import *
from google_trans_new import google_translator
from assistant_sys_tray_icon import SystemTrayIcon
from pprint import pprint


class Assistant:
    def __init__(self):
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        self.threadpool = QThreadPool()
        self.thread_list = []

        self.w = QWidget()
        self.tray_icon = SystemTrayIcon(self.w, self)
        self.tray_icon.activated.connect(self.activate)

        self.MainWindow = Window()
        self.FormTrans = Form()
        self.ui = UI_Windows()
        self.ui_button_connect()
        self.initial_assistant()

        sys.exit(app.exec_())

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.initial_assistant()

    def speak_thread(self, text):
        if text.isnumeric():
            self.thread = Thread(self.play_sound, text)
            self.threadpool.start(self.thread)
        else:
            self.thread = Thread(self.speak, text)
            self.threadpool.start(self.thread)

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang="vi", slow=False)
            tts.save("./audio/sound.mp3")
            playsound("./audio/sound.mp3", False)
            os.remove("./audio/sound.mp3")
        except:
            os.remove("./audio/sound.mp3")

    def play_sound(self, code):
        if "001" in code:
            playsound("./audio/001_didnt_hear.mp3")
        elif "002" in code:
            playsound("./audio/002_help_me.mp3")
        elif "003" in code:
            playsound("./audio/003_play_song.mp3")
        elif "004" in code:
            playsound("./audio/004_wikipedia.mp3")
        elif "005" in code:
            playsound("./audio/005_open_app.mp3")
        elif "006" in code:
            playsound("./audio/006_open_web.mp3")

    def get_text_from_audio_thread(self, function):
        self.thread = Thread(self.speech_recognition)
        self.thread.signals.result.connect(self.ui.update_bottom_bar)
        self.thread.signals.result.connect(self.user_request)
        self.threadpool.start(self.thread)

    def speech_recognition(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                return text.lower()
            except sr.UnknownValueError:
                return "..."
            except sr.RequestError:
                return "...."

    # * UI Button Connect
    def ui_button_connect(self):
        self.ui.button_close.clicked.connect(self.exit_application)
        self.ui.button_microphone.clicked.connect(self.initial_assistant)
        self.ui.topic_button_1.clicked.connect(lambda: self.search_news_thread(1))
        self.ui.topic_button_2.clicked.connect(lambda: self.search_news_thread(2))
        self.ui.topic_button_3.clicked.connect(lambda: self.search_news_thread(3))
        self.ui.topic_button_4.clicked.connect(lambda: self.search_news_thread(4))
        self.ui.topic_button_5.clicked.connect(lambda: self.search_news_thread(5))

    def exit_application(self):
        self.MainWindow.close()
        self.thread.kill()

    def close_window(self):
        self.MainWindow.close()

    def get_location_from_ip(self):
        url = "https://ipinfo.io/"

        try:
            response = requests.get(url, timeout=5).json()
        except:
            return 0
        else:
            city = response["city"]
            region = response["region"]
            location = response["loc"].split(",")
            lat = location[0]
            lon = location[1]
            result = {"city": city, "region": region, "lat": lat, "lon": lon}
            return result

    def find_app(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def lost_internet_connection(self):
        url = "./icon/no-wifi-256px.png"
        text = "Vui lòng kiểm tra lại Internet."
        self.ui.setupUI_response_window(self.MainWindow, url, text)

    # * Initial Assistant
    def initial_assistant(self):
        self.ui.setupUI_main_window(self.MainWindow)
        playsound("./audio/101_notification.wav", False)
        self.get_text_from_audio_thread(self.user_request)

    # * User Request
    def user_request(self, text):
        delay = ThreadDelay(1, text)
        if "..." in text:
            if len(text) == 3:
                delay.signals.non_args.connect(self.didnt_hear)
            else:
                delay.signals.non_args.connect(self.lost_internet_connection)
        elif "hôm nay" in text or "hiện tại" in text or "bây giờ" in text:
            if "giờ" in text:
                delay.signals.non_args.connect(self.get_time_thread)
            elif "ngày" in text or "thứ" in text:
                delay.signals.non_args.connect(self.get_date_thread)
            else:
                delay.signals.non_args.connect(self.search_default_thread)
        elif "mở video" in text or "mở bài" in text:
            delay.signals.args.connect(self.play_song_thread)
        elif "thời tiết" in text:
            delay.signals.args.connect(self.what_weather_thread)
        elif "tin tức" in text:
            delay.signals.non_args.connect(self.search_news_thread)
        elif "mở" in text:
            if "." in text:
                delay.signals.args.connect(self.open_website_thread)
            else:
                delay.signals.args.connect(self.open_application_thread)
        elif "tra cứu" in text:
            delay.signals.args.connect(self.lookup_wikipedia_thread)
        elif "từ điển" in text:
            delay.signals.non_args.connect(self.translation_thread)
        elif "trợ giúp" in text:
            delay.signals.non_args.connect(self.assistant_help_thread)
        else:
            delay.signals.args.connect(self.search_default_thread)

        self.threadpool.start(delay)

    def didnt_hear(self):
        url = "./icon/mute-microphone-256px.png"
        text = "Xin lỗi tôi không nghe rõ bạn nói gì."
        self.ui.setupUI_response_window(self.MainWindow, url, text)
        self.speak_thread("001")

    def get_time_thread(self):
        self.thread = Thread(self.get_time)
        self.thread.signals.result.connect(self.get_time_complete)
        self.threadpool.start(self.thread)

    def get_time(self):
        location = self.get_location_from_ip()

        api = "BL83E6LF3XI3"
        url = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}"

        if location:
            try:
                response = requests.get(
                    url.format(api, location["lat"], location["lon"]),
                    timeout=5,
                ).json()
            except:
                return 0
            else:
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
        if result:
            speech = "Hiện tại là {} giờ {} phút {} giây.".format(
                result["hour"], result["minute"], result["second"]
            )

            self.ui.setupUI_clock_window(self.MainWindow, result)
            self.speak_thread(speech)
        else:
            self.lost_internet_connection()

    def get_date_thread(self):
        self.thread = Thread(self.get_time)
        self.thread.signals.result.connect(self.get_date_complete)
        self.threadpool.start(self.thread)

    def get_date(self):
        location = self.get_location_from_ip()

        api = "BL83E6LF3XI3"
        url = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}"

        if location:
            try:
                response = requests.get(
                    url.format(api, location["lat"], location["lon"]),
                    timeout=5,
                ).json()
            except:
                return 0
            else:
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
        if result:
            speech = "Hôm nay là ngày {} tháng {} năm {}".format(
                result["day"], result["month"], result["year"]
            )

            self.ui.setupUI_date_window(self.MainWindow, result)
            self.speak_thread(speech)
        else:
            self.lost_internet_connection()

    def play_song_thread(self, text):
        if "mở video" in text:
            reg_ex = re.search("mở video", text)
            start = reg_ex.end() + 1
            end = len(text)
            song_name = text[start:end]
            if song_name == "":
                song_name = "none"
        elif "mở bài" in text:
            reg_ex = re.search("mở bài", text)
            start = reg_ex.end() + 1
            end = len(text)
            song_name = text[start:end]
            if song_name == "":
                song_name = "none"

        self.ui.update_bottom_bar()
        self.ui.setupUI_loading_window(self.MainWindow, "Đang mở video....")

        self.thread = Thread(self.play_song, song_name)
        self.thread.signals.result.connect(self.play_song_complete)
        self.threadpool.start(self.thread)

    def play_song(self, song_name):
        try:
            result = search_youtube([song_name])
        except:
            return 0
        else:
            url = "https://www.youtube.com/watch?v=" + result[0]["id"]
            webbrowser.open(url)
            return 1

    def play_song_complete(self, result):
        if result:
            self.thread = ThreadDelay(1)
            self.thread.signals.finished.connect(self.close_window)
            self.threadpool.start(self.thread)
        else:
            self.lost_internet_connection()

    def what_weather_thread(self, text):
        if "tỉnh" in text:
            reg_ex = re.search("tỉnh", text)
            start = reg_ex.end() + 1
            end = len(text)
            city = text[start:end]
            if city == "":
                city = "none"
        elif "thành phố" in text:
            reg_ex = re.search("thành phố", text)
            start = reg_ex.end() + 1
            end = len(text)
            city = text[start:end]
            if city == "":
                city = "none"
        else:
            city = "default"

        if "none" in city:
            self.search_default_thread(text)
        else:
            self.thread = Thread(self.what_weather, city)
            self.thread.signals.result.connect(self.what_weather_complete)
            self.threadpool.start(self.thread)

    def what_weather(self, city):
        if "default" in city:
            location = self.get_location_from_ip()

            if location:
                geolocator = Nominatim(user_agent="Virtual Assistant")
                display_name = geolocator.geocode(location["city"]).address

                lat = location["lat"]
                lon = location["lon"]

        else:
            geolocator = Nominatim(user_agent="Virtual Assistant")
            location = geolocator.geocode(city)

            display_name = location.address
            lat = location.latitude
            lon = location.longitude

        if location:
            api = "4e7ced343986de64b7f54296a111c208"
            part = "minutely,hourly,daily,alerts"
            units = "metric"
            lang = "vi"
            url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
            url_one_call = url.format(lat, lon, part, units, lang, api)

            try:
                response = requests.get(url_one_call, timeout=5).json()
            except:
                return 0
            else:
                c_cur_time = response["current"]["dt"]
                c_sunrise = response["current"]["sunrise"]
                c_sunset = response["current"]["sunset"]
                c_temp = response["current"]["temp"]
                c_feel_like = response["current"]["feels_like"]
                c_pressure = response["current"]["pressure"]
                c_humidity = response["current"]["humidity"]
                c_dew_point = response["current"]["dew_point"]
                c_clouds = response["current"]["clouds"]
                c_uvi = response["current"]["uvi"]
                c_visibility = response["current"]["visibility"]
                c_wind_speed = response["current"]["wind_speed"]
                c_wind_deg = response["current"]["wind_deg"]
                c_weather_id = response["current"]["weather"][0]["id"]
                c_weather_main = response["current"]["weather"][0]["main"]
                c_weather_description = response["current"]["weather"][0]["description"]
                c_weather_icon = response["current"]["weather"][0]["icon"]

                result = {
                    "city": display_name,
                    "icon": c_weather_icon,
                    "feel_like": c_feel_like,
                    "desc": c_weather_description,
                    "temp": c_temp,
                    "pressure": c_pressure,
                    "humidity": c_humidity,
                    "cloud": c_clouds,
                    "wind_deg": c_wind_deg,
                    "wind_speed": c_wind_speed,
                    "uvi": c_uvi,
                    "visibility": c_visibility,
                }
                return result

    def what_weather_complete(self, result):
        if result:
            speech = "Dự báo thời tiết cho {}. Nhiệt độ là {} độ C, {}.".format(
                result["city"], result["temp"], result["desc"]
            )
            self.ui.setupUI_weather_window(self.MainWindow, result)
            self.speak_thread(speech)
        else:
            self.lost_internet_connection()

    def search_news_thread(self, opt=0):
        self.thread = Thread(self.search_news, opt)
        self.thread.signals.result.connect(self.search_news_complete)
        self.threadpool.start(self.thread)

    def search_news(self, opt):
        def split_content(text):
            i_desc = text.rfind(">")
            i_start_img = text.rfind("src=")
            i_end_img = text.rfind("/>")

            if i_start_img == -1:
                image_cover = "none"
            else:
                link_image = text[i_start_img + 5 : i_end_img - 2]
                image_cover = link_image.replace("amp;", "")

            description = text[i_desc + 1 :]
            content = {"desc": description, "l_img": image_cover}

            return content

        if opt == 0:
            url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
            result = {
                "is_update": 0,
                "see_more": "https://vnexpress.net/tin-tuc-24h",
            }
        elif opt == 1:
            url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
            result = {
                "is_update": opt,
                "see_more": "https://vnexpress.net/tin-tuc-24h",
            }
        elif opt == 2:
            url = "https://vnexpress.net/rss/tin-noi-bat.rss"
            result = {
                "is_update": opt,
                "see_more": "https://vnexpress.net/tin-nong",
            }
        elif opt == 3:
            url = "https://vnexpress.net/rss/giai-tri.rss"
            result = {
                "is_update": opt,
                "see_more": "https://vnexpress.net/giai-tri",
            }
        elif opt == 4:
            url = "https://vnexpress.net/rss/the-thao.rss"
            result = {
                "is_update": opt,
                "see_more": "https://vnexpress.net/the-thao",
            }
        elif opt == 5:
            url = "https://vnexpress.net/rss/khoa-hoc.rss"
            result = {
                "is_update": opt,
                "see_more": "https://vnexpress.net/khoa-hoc",
            }

        try:
            feed = feedparser.parse(url)
        except:
            pass
        else:
            feed_entries = feed.entries

            i = 0
            for entry in feed_entries:
                if i == 10:
                    break

                article_title = entry.title
                article_link = entry.link
                content = split_content(entry.summary)

                filename = "./image/cover" + str(i) + ".jpg"
                img_url = content["l_img"]

                if "none" in img_url:
                    article = {
                        "title": article_title,
                        "cover_img": "./image/no_img.jpg",
                        "desc": content["desc"],
                        "link": article_link,
                    }

                else:
                    img_data = requests.get(img_url).content
                    with open(filename, "wb") as handler:
                        handler.write(img_data)

                    article = {
                        "title": article_title,
                        "cover_img": filename,
                        "desc": content["desc"],
                        "link": article_link,
                    }

                key = str(i)
                result.update({key: article})
                i += 1

            return result

    def search_news_complete(self, result):
        if result:
            if result["is_update"]:
                self.ui.update_topic_content(self.MainWindow, result)
                self.ui.update_topic_buttons(result["is_update"])
            else:
                self.ui.topic_button_1.setDisabled(True)
                self.ui.setupUI_news_window(self.MainWindow, result)
        else:
            self.lost_internet_connection()

    def open_website_thread(self, text):
        self.ui.update_bottom_bar()
        self.ui.setupUI_loading_window(self.MainWindow, "Đang mở website....")

        self.thread = Thread(self.open_website, text)
        self.thread.signals.result.connect(self.open_website_complete)
        self.threadpool.start(self.thread)

    def open_website(self, text):
        reg_ex = re.search("mở (.+)", text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)

    def open_website_complete(self):
        self.speak_thread("007")
        self.thread = ThreadDelay(1)
        self.thread.signals.finished.connect(self.close_window)
        self.threadpool.start(self.thread)

    def open_application_thread(self, text):
        if "edge" in text:
            file_name = "msedge.exe"
            full_name = "Microsoft Edge"
        elif "chrome" in text:
            file_name = "chrome.exe"
            full_name = "Google Chrome"
        elif "word" in text:
            file_name = "WINWORD.EXE"
            full_name = "Microsoft Word"
        elif "excel" in text:
            file_name = "EXCEL.EXE"
            full_name = "Microsoft Excel"
        elif "powerpoint" in text:
            file_name = "POWERPNT.EXE"
            full_name = "Microsoft PowerPoint"
        else:
            file_name = ""
            full_name = ""

        if file_name != "" and full_name != "":
            self.ui.update_bottom_bar()
            self.ui.setupUI_loading_window(
                self.MainWindow, "Đang mở phần mềm/ứng dụng...."
            )

            self.thread = Thread(self.open_application, file_name, full_name)
            self.thread.signals.result.connect(self.open_application_complete)
            self.threadpool.start(self.thread)
        else:
            self.search_default_thread(text)

    def open_application(self, file_name, full_name):
        path = self.find_app(file_name, "C:/")
        if path:
            os.startfile(path)
            return True
        else:
            return False

    def open_application_complete(self, result):
        if result:
            self.thread = ThreadDelay(1, "005")
            self.thread.signals.finished.connect(self.close_window)
            self.thread.signals.args.connect(self.speak_thread)
            self.threadpool.start(self.thread)

        else:
            url = "./icon/error-256px.png"
            text = "Phần mềm bạn yêu cầu chưa được cài đặt."
            self.ui.setupUI_response_window(self.MainWindow, url, text)
            self.speak_thread("006")

    def lookup_wikipedia_thread(self, text):
        reg_ex = re.search("tra cứu", text)
        start = reg_ex.end() + 1
        end = len(text)
        keyword = text[start:end]

        if len(keyword) > 0:
            self.thread = Thread(self.lookup_wikipedia, keyword)
            self.thread.signals.result.connect(self.lookup_wikipedia_complete)
            self.threadpool.start(self.thread)
        else:
            self.search_default_thread(text)

    def lookup_wikipedia(self, keyword):
        try:
            wikipedia.set_lang("vi")
        except:
            return 0
        else:
            result = {
                "keyword": keyword.title(),
                "meaning": wikipedia.summary(keyword),
            }
            return result

    def lookup_wikipedia_complete(self, result):
        if result:
            self.ui.setupUI_wikipedia_window(self.MainWindow, result)
            self.speak_thread("004")
        else:
            self.lost_internet_connection()

    def search_default_thread(self, text):
        self.thread = Thread(self.search_default, text)
        self.thread.signals.result.connect(self.search_default_complete)
        self.threadpool.start(self.thread)

    def search_default(self, text):
        api_cse = "AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw"
        cx_cse = "efcdf7a6d77b621bc"
        page = 1
        fields = "searchInformation(formattedTotalResults,formattedSearchTime),items(title,formattedUrl,snippet,link)"
        url_cse = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&start={}&q={}&fields={}"
        try:
            response = requests.get(
                url_cse.format(api_cse, cx_cse, page, text, fields), timeout=5
            ).json()
        except:
            return 0
        else:
            result = {}
            for i in range(10):
                key = str(i)

                values = {
                    "formatted_url": response["items"][i]["formattedUrl"]
                    if "formattedUrl" in response["items"][i]
                    else "",
                    "title": response["items"][i]["title"]
                    if "title" in response["items"][i]
                    else "",
                    "snippet": str(response["items"][i]["snippet"]).strip("\n")
                    if "snippet" in response["items"][i]
                    else "",
                    "link": response["items"][i]["link"]
                    if "link" in response["items"][i]
                    else "",
                }

                result.update({key: values})

            result.update({"text": text})

            about = "Khoảng {} kết quả ({} giây)\n\n".format(
                response["searchInformation"]["formattedTotalResults"],
                response["searchInformation"]["formattedSearchTime"],
            )
            result.update({"about": about})

            see_more = "https://www.google.com/search?q={}".format(text)
            result.update({"see_more": see_more})

            speech = "Đây là kết quả tìm kiếm cho {}".format(text)
            result.update({"speech": speech})

            return result

    def search_default_complete(self, result):
        if result:
            self.ui.setupUI_search_default_window(self.MainWindow, result)
            self.speak_thread(result["speech"])
        else:
            self.lost_internet_connection()

    def translation_thread(self):
        url = "./icon/select-256px.png"
        text = "Chọn từ hoặc câu cần dịch."
        self.ui.setupUI_response_window(self.MainWindow, url, text, 1)
        self.speak_thread(text)

        self.trans_thread = ThreadTrans(self.translation)
        self.trans_thread.signals.result.connect(self.translation_complete)
        self.threadpool.start(self.trans_thread)

        self.tray_icon.update_translation_action(1)

    def translation(self):
        keyboard = Controller()
        translator = google_translator()
        self.chain = []
        result = {
            "error": 2,
        }

        def on_move(x, y):
            self.chain.append(2)

        def on_click(x, y, button, pressed):
            if pressed:
                self.chain.append(1)
            else:
                self.chain.append(3)
                self.cursor_position = QPoint(x, y)
                return False

        with mouse.Listener(on_move=on_move, on_click=on_click) as mouseListener:
            mouseListener.join()

        if self.chain[-2] != 1:
            keyboard.press(Key.ctrl)
            keyboard.press("c")
            keyboard.release(Key.ctrl)
            keyboard.release("c")
            time.sleep(0.05)

            str_from_clipboard = pyperclip.paste()
            pyperclip.copy("")

            if str_from_clipboard != "":
                try:
                    dest = translator.translate(str_from_clipboard, lang_tgt="vi")
                    detect_lang = translator.detect(str_from_clipboard)
                except:
                    result = {
                        "error": 1,
                        "text": "Lỗi! Vui lòng thử lại lần nữa.",
                        "cursor_pos": self.cursor_position,
                    }
                else:
                    result = {
                        "error": 0,
                        "detect": str(detect_lang[1]).title(),
                        "src": str_from_clipboard,
                        "dest": dest,
                        "cursor_pos": self.cursor_position,
                    }
        return result

    def translation_complete(self, result):
        if result["error"] == 2:
            pass
        else:
            self.ui.setupUI_trans_window(self.FormTrans, result)

    def kill_translation_thread(self):
        self.trans_thread.kill()

    def assistant_help_thread(self):
        self.ui.setupUI_help_window(self.MainWindow)
        self.speak_thread("002")


if __name__ == "__main__":
    Assistant()
