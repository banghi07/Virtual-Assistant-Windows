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
# import win32clipboard
# from ctypes import windll
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

from assistant_sys_tray_icon import *
from assistant_threads import *
from assistant_window import Ui_MainWindow
from news import News
from weather import Weather
from trans import Trans

drive = "C:/"


def find_app(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


class Assistant():
    def __init__(self):
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        w = QWidget()
        tray_icon = SystemTrayIcon(w)
        tray_icon.activated.connect(self.activate)

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.threadpool = QThreadPool()
        self.worker_threads = []

        self.set_widgets()
        self.initial_assistant()

        self.MainWindow.show()
        sys.exit(app.exec_())

    #* ================================ SET & GET FUNCTIONS ==================================== #

    # Đặt title cho dialog
    def set_widgets(self):
        self.MainWindow.setWindowTitle('Virtual Assistant- PyQt5')
        self.MainWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.MainWindow.setFixedSize(
            self.MainWindow.width(), self.MainWindow.height())

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.set_plain_text_edit("")
            self.set_label("")
            self.MainWindow.show()

    # Đặt text cho PlainTextEdit
    def set_plain_text_edit(self, text):
        self.ui.plainTextEdit.setPlainText(text)

    # Đặt text cho Label
    def set_label(self, text):
        self.ui.label.setText(text)

    def update_worker_threads(self, text, status):
        if status:
            self.worker_threads.append(text)
        else:
            self.worker_threads.remove(text)
        print(self.worker_threads)

    # Đặt text cho PlainTextEdit và Speak text đã đặt
    def response(self, text):
        self.set_plain_text_edit(text)
        self.speak(text)

    # Cho trợ lý ảo đọc text truyền vào
    def speak(self, text):
        if text.isnumeric():
            worker = Thread(self.play_sound_thread, text, "speak")
            worker.signals.running.connect(self.update_worker_threads)
            self.threadpool.start(worker)
        else:
            worker = Thread(self.speak_thread, text, "speak")
            worker.signals.running.connect(self.update_worker_threads)
            self.threadpool.start(worker)

    def speak_thread(self, text):
        try:
            tts = gTTS(text=text, lang="vi", slow=False)
            tts.save("./audio/sound.mp3")
            playsound("./audio/sound.mp3", False)
            os.remove("./audio/sound.mp3")
        except:
            print("Error: Token Google Translate. Try again...")
            # os.remove("./audio/sound.mp3")
            self.speak_thread(text)

    def play_sound_thread(self, code):
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

    # Chạy Thread nhận dạng giọng nói (chuyển từ speech sang text)
    def get_text_from_audio(self, function):
        worker = Thread(self.speech_recognition, "get_text_from_audio")
        worker.signals.running.connect(self.update_worker_threads)
        worker.signals.result.connect(function)
        self.threadpool.start(worker)

    # Speech to text
    def speech_recognition(self):
        self.set_label("Đang lắng nghe...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                self.set_label(text.lower())
                return text.lower()
            except:
                self.set_label("...")
                return "none"

   #* ================================ CALL ASSISTANT ==================================== #

    # Khởi tạo ban đầu
    def initial_assistant(self):
        self.ui.pushButton.pressed.connect(self.call_assistant)

    # Gọi trợ lý ảo
    def call_assistant(self):
        playsound("./audio/101_notification.wav", False)
        self.set_plain_text_edit("Tôi có thể giúp gì cho bạn?")
        self.get_text_from_audio(self.request)

    # Yêu cầu chức năng
    def request(self, text):
        if "none" in text:
            self.set_plain_text_edit("Xin lỗi, tôi không nghe rõ bạn nói gì!")
            self.speak("001")
        elif "trợ giúp" in text or "help" in text:
            self.help_me()
        elif "chào" in text or "hello" in text:
            self.greeting()
        elif "hôm nay" in text or "bữa nay" in text or "hiện tại" in text or "bây giờ" in text:
            self.get_time(text)
        elif "mở nhạc" in text or "mở video" in text or "mở bài" in text:
            self.play_song(text)
        elif "thời tiết" in text:
            self.what_weather(text)
        elif "tin tức" in text:
            self.read_news()
        elif "tra cứu" in text:
            self.lookup_wikipedia(text)
        elif "mở" in text:
            if "." in text:
                self.open_website(text)
            else:
                self.open_application(text)
        elif "từ điển" in text:
            self.dictionary()
        else:
            self.search_default(text)

    #* ================================= ASSISTANT FUNCTIONS =================================== #

    # 1. Trợ giúp
    def help_me(self):
        text = """Tôi có thể giúp bạn thực hiện những việc sau đây:
    1. Hiển thị ngày giờ
    2. Mở video nhạc trên Youtube
    3. Xem dự báo thời tiết
    4. Đọc tin tức, thời sự
    5. Tra cứu định nghĩa với Wikipedia
    6. Mở ứng dụng, phần mềm
    7. Mở website
    8. Tra cứu từ điển
    9. Tìm kiếm từ khóa với Google
        """
        string = "Tôi có thể giúp bạn làm những việc sau đây."

        self.set_plain_text_edit(text)
        self.speak("002")

    # 2. Chào hỏi
    def greeting(self):
        day_time = int(strftime("%H"))
        if day_time < 12:
            # self.response("Chào buổi sáng. Chúc bạn một ngày tốt lành!")
            self.speak("003")
        elif 12 <= day_time < 18:
            # self.response(
            #     "Chào buổi chiều. Bạn đã dự định gì cho chiều này chưa?")
            self.speak("004")
        else:
            # self.response("Chào buổi tối. Chúc bạn buổi tối vui vẻ.")
            self.speak("005")

    # 3. Xem ngày giờ
    def get_time(self, text):
        now = datetime.datetime.now()
        if "giờ" in text:
            self.response("Hiện tại là {} giờ {} phút.".format(
                now.hour, now.minute))
        elif "ngày" in text:
            self.response("Hôm nay là ngày {} tháng {} năm {}.".format(
                now.day, now.month, now.year))
        else:
            self.set_plain_text_edit("Chưa xử lý code")

    # 4. Mở video trên Youtube
    def play_song(self, text):
        if "mở nhạc" in text:
            reg_ex = re.search("mở nhạc", text)
            start = reg_ex.end() + 1
            end = len(text)
            song_name = text[start:end]
            if song_name == "":
                song_name = "none"
        elif "mở video" in text:
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
        self.search_music_thread(song_name)

    def search_music_thread(self, text):
        if "none" in text:
            self.set_plain_text_edit("Chưa xử lý code")
        else:
            worker = Thread(self.search_music, text, "play_song")
            worker.signals.running.connect(self.update_worker_threads)
            worker.signals.finished.connect(self.play_song_complete)
            self.threadpool.start(worker)
            self.set_plain_text_edit("Đang mở. Vui lòng đợi...")

    def search_music(self, text):
        result = search_youtube([text])
        # result = YoutubeSearch(text, max_results=3).to_dict()
        url = "https://www.youtube.com/watch?v=" + result[0]["id"]
        # url = "https://www.youtube.com/" + result[0]["url_suffix"]
        webbrowser.open(url)
        print(text)

    def play_song_complete(self):
        self.speak("006")
        self.set_plain_text_edit("Đã mở bài hát bạn yêu cầu.")

    # 5. Xem dự báo thời tiết
    def what_weather(self, text):
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

        self.search_weather_thread(city)

    def search_weather_thread(self, text):
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")
        if "none" in text:
            self.response("Xin lỗi, không tìm thấy địa điểm đã nói.")
        elif "default" in text:
            worker = Thread(self.search_weather_default,
                            "what_weather_default")
            worker.signals.running.connect(self.update_worker_threads)
            worker.signals.result.connect(self.what_weather_complete)
            self.threadpool.start(worker)
        else:
            worker = Thread(self.search_weather, text, "what_weather")
            worker.signals.result.connect(self.what_weather_complete)
            worker.signals.running.connect(self.update_worker_threads)
            self.threadpool.start(worker)

    def search_weather_default(self):
        url = "https://ipinfo.io/"
        response = requests.get(url).json()
        city = response["city"]
        region = response["region"]
        location = response["loc"].split(",")

        geolocator = Nominatim(user_agent="Virtual Assistant")
        display_name = geolocator.geocode(city).address

        lat = location[0]
        lon = location[1]
        api = "4e7ced343986de64b7f54296a111c208"
        part = "minutely,hourly,daily,alerts"
        units = "metric"
        lang = "vi"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
        url_one_call = url.format(lat, lon, part, units, lang, api)
        response = requests.get(url_one_call).json()

        # c_lat = response["lat"]
        # c_lon = response["lon"]
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
        # c_wind_gust = response["current"]["wind_gust"]
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

    def search_weather(self, region):
        geolocator = Nominatim(user_agent="Virtual Assistant")
        location = geolocator.geocode(region)

        display_name = location.address
        lat = location.latitude
        lon = location.longitude
        api = "4e7ced343986de64b7f54296a111c208"
        part = "minutely,hourly,daily,alerts"
        units = "metric"
        lang = "vi"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
        url_one_call = url.format(lat, lon, part, units, lang, api)
        response = requests.get(url_one_call).json()

        # c_lat = response["lat"]
        # c_lon = response["lon"]
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
        # c_wind_gust = response["current"]["wind_gust"]
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
        self.MainWindow.close()
        self.weather_window = Weather(result)

    # 6. Đọc báo rss news
    def read_news(self):
        self.search_news_thread()

    def search_news_thread(self):
        worker = Thread(self.search_news, "read_news")
        worker.signals.running.connect(self.update_worker_threads)
        worker.signals.result.connect(self.read_news_complete)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search_news(self):
        url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

        def split_content(text):
            i_desc = text.rfind(">")
            i_start_img = text.rfind("src=")
            i_end_img = text.rfind("/>")

            if i_start_img == -1:
                image_cover = "none"
                print("none\n")
            else:
                link_image = text[i_start_img + 5 : i_end_img - 2]
                image_cover = link_image.replace("amp;", "")

            description = text[i_desc + 1 :]
            content = {"desc": description, "l_img": image_cover}

            return content

        def week_day(i):
            if i == 0:
                return "Chủ nhật"
            elif i == 1:
                return "Thức hai"
            elif i == 2:
                return "Thứ ba"
            elif i == 3:
                return "Thứ tư"
            elif i == 4:
                return "Thứ năm"
            elif i == 5:
                return "Thứ sáu"
            elif i == 6:
                return "Thứ bảy"

        def time_format(s_time):
            # wday = week_day(s_time.tm_wday)
            wday = str(s_time.tm_wday)
            t = time.strftime("%d-%m-%Y, %H:%M:%S")
            temp = wday + " " + t
            return temp

        feed = feedparser.parse(url)
        feed_entries = feed.entries

        i = 0
        text = ""
        result = {}

        for entry in feed_entries:
            if i == 5:
                break

            article_title = entry.title
            article_link = entry.link
            article_published_at = entry.published
            article_published_at_parsed = entry.published_parsed  # Time object
            # article_published_at = time_format(article_published_at_parsed)
            content = split_content(entry.summary)

            filename = "./image/cover" + str(i) + ".jpg"
            img_url = content["l_img"]

            if "none" in img_url:
                article = {
                    "title": article_title,
                    "published_at": article_published_at,
                    "cover_img": "./image/no_img.jpg",
                    "description": content["desc"],
                    "link": article_link,
                }

            else:
                img_data = requests.get(img_url).content
                with open(filename, "wb") as handler:
                    handler.write(img_data)

                article = {
                    "title": article_title,
                    "published_at": article_published_at_parsed,
                    "cover_img": filename,
                    "description": content["desc"],
                    "link": article_link,
                }

            key = "no_" + str(i)
            result.update({key: article})
            i += 1

        return result        

    def read_news_complete(self, result):
        self.MainWindow.close()
        self.NewsWindow = News(result)

    # 7. Tìm kiếm định nghĩa wikipedia
    def lookup_wikipedia(self, text):
        reg_ex = re.search("tra cứu", text)
        if reg_ex:
            start = reg_ex.end() + 1
            end = len(text)
            words = text[start:end]
            self.search_wiki_thread(words)
        else:
            # Chưa xử lý.
            self.search_default(text)

    def search_wiki_thread(self, text):
        worker = Thread(self.search_wiki, text, "lookup_wikipedia")
        worker.signals.result.connect(self.lookup_wikipedia_complete)
        worker.signals.running.connect(self.update_worker_threads)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search_wiki(self, text):
        wikipedia.set_lang('vi')
        content = "[Wikipedia vi-VN]\n" + wikipedia.summary(text)
        result = {
            "content": content,
            "string": "Đây là kết quả tìm kiếm từ Wikipedia"
        }
        return result

    def lookup_wikipedia_complete(self, result):
        self.set_plain_text_edit(result["content"])
        # self.speak(result["string"])
        self.speak("007")

    # 8. Mở phần mềm ứng dụng
    def open_application(self, text):
        if "edge" in text:
            self.search_app_thread("msedge.exe", "Microsoft Edge")
        elif "chrome" in text:
            self.search_app_thread("chrome.exe", "Google Chrome")
        elif "word" in text:
            self.search_app_thread("WINWORD.EXE", "Microsoft Word")
        elif "excel" in text:
            self.search_app_thread("EXCEL.EXE", "Microsoft Excel")
        elif "powerpoint" in text:
            self.search_app_thread("POWERPNT.EXE", "Microsoft PowerPoint")
        else:
            self.search_default(text)

    def search_app_thread(self, fileName, fullName):
        worker = Thread(self.search_app, fileName,
                        fullName, "open_application")
        worker.signals.result.connect(self.open_application_complete)
        worker.signals.running.connect(self.update_worker_threads)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang mở ứng dụng. Vui lòng đợi...")

    def search_app(self, fileName, fullName):
        path = find_app(fileName, drive)
        if path:
            os.startfile(path)
        else:
            fullName = "none"
        return fullName

    def open_application_complete(self, fullName):
        if "none" in fullName:
            self.response("Ứng dụng bạn yêu cầu chưa được cài đặt.")
        else:
            # self.response("Đã mở ứng dụng {}.".format(fullName))
            self.speak("008")

    # 9. Mở website
    def open_website(self, text):
        self.search_web_thread(text)

    def search_web_thread(self, text):
        worker = Thread(self.search_web, text, "open_website")
        worker.signals.finished.connect(self.open_website_complete)
        worker.signals.running.connect(self.update_worker_threads)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang mở Website. Vui lòng đợi...")

    def search_web(self, text):
        reg_ex = re.search("mở (.+)", text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)
            return True
        else:
            return False

    def open_website_complete(self):
        self.response("Đã mở trang web bạn yêu cầu.")
        self.speak("009")

    # 10. Tìm kiếm bằng google engine của trình duyệt mặc định
    def search_default(self, text):
        self.search_thread(text)

    def search_thread(self, text):
        worker = Thread(self.search_gg, text, "search_default")
        worker.signals.running.connect(self.update_worker_threads)
        worker.signals.result.connect(self.search_default_complete)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search_gg(self, text):
        service = build("customsearch", "v1",
                        developerKey="AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw")
        response = service.cse().list(q=text, cx="efcdf7a6d77b621bc", num="3", fields="context/title,\
                                        items/displayLink, items/formattedUrl, items/link, items/snippet, items/title,\
                                        searchInformation/formattedSearchTime, searchInformation/formattedTotalResults").execute()
        content = "[{}]\nKhoảng {} kết quả ({} giây)\n\n".format(response["context"]["title"], response["searchInformation"]["formattedTotalResults"],
                                                                 response["searchInformation"]["formattedSearchTime"])

        for i in range(3):
            content = content + "[{num}] {displayLink}\n[Title] {title}\n[Snippet] {snippet}\n[FormattedUrl] {formattedUrl}\n\n".format(num=i+1,
                                                                                                                                        title=response["items"][i]["title"], displayLink=response[
                                                                                                                                            "items"][i]["displayLink"],
                                                                                                                                        snippet=response["items"][i]["snippet"], formattedUrl=response["items"][i]["formattedUrl"])

        result = {
            "content": content + "[See more] https://www.google.com/search?q={}".format(text),
            "string": "Đây là kết quả tìm kiếm cho {}".format(text)
        }

        return result

    def search_default_complete(self, result):
        self.set_plain_text_edit(result["content"])
        self.speak(result["string"])

    # 11. Dịch nghĩa sang tiếng Việt
    def dictionary(self):
        self.MainWindow.close()
        self.translate_thread()

    def translate_thread(self):
        worker = ThreadD(self.translate, "dictionary")
        worker.signals.result.connect(self.translate_complete)
        # worker.signals.result.connect(self.set_plain_text_edit)
        worker.signals.running.connect(self.update_worker_threads)
        self.set_plain_text_edit("Đã bật từ điển.")
        self.threadpool.start(worker)

    # TODO Ghi nhớ clipboard do user copy vào 1 biến tạm, sau khi kết thúc thì đưa lại vào clipboard
    def translate(self):
        keyboard = Controller()
        translator = Translator()
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
                    content = translator.translate(
                        str_from_clipboard, dest="vi")
                except:
                    result = {
                        "error": 1,
                        "text": "Lỗi! Hãy thử lại.",
                        "cursor_pos": self.cursor_position 
                    }
                else:
                    result = {
                        "error": 0,
                        "src": content.src,
                        "dest": content.dest,
                        "text": content.text,
                        "cursor_pos": self.cursor_position 
                    }
        
        return result

    def translate_complete(self, result):
        if result["error"] == 2:
            pass
        else:
            self.trans_window = Trans(result)
        

#* ================================ FUNCITON MAIN ==================================== #


if __name__ == "__main__":
    Assistant()
