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
from gtts import gTTS
from playsound import playsound
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from youtube_search import YoutubeSearch

from mainwindow import Ui_MainWindow

drive = "C:/"
chain = []


def find_app(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


class ThreadSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Thread, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        l = list(self.args)
        time.sleep(l[-1])
        l.pop()
        t = tuple(l)
        try:
            result = self.fn(*t, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


# ? Thead riêng tạm thời cho function dictionary (sử dụng vòng lặp while True)
# TODO thêm tính năng khi thoát phần mềm thì kill Thread translate đi vì translate dùng while True
class ThreadDSignals(QObject):
    result = pyqtSignal(object)


class ThreadD(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(ThreadD, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = ThreadDSignals()

    @pyqtSlot()
    def run(self):
        while True:
            try:
                result = self.fn(*self.args, **self.kwargs)
                self.signals.result.emit(result)
            except:
                self.run()
                break


class Assistant():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.threadpool = QThreadPool()
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

    # Đặt text cho PlainTextEdit
    def set_plain_text_edit(self, text):
        self.ui.plainTextEdit.setPlainText(text)

    # Đặt text cho Label
    def set_label(self, text):
        self.ui.label.setText(text)

    # Đặt text cho PlainTextEdit và Speak text đã đặt
    def response(self, text):
        self.set_plain_text_edit(text)
        self.speak(text)

    # Cho trợ lý ảo đọc text truyền vào
    def speak(self, text):
        while True:
            try:
                tts = gTTS(text=text, lang="vi", slow=False)
                tts.save("sound.mp3")
                playsound("sound.mp3", False)
                os.remove("sound.mp3")
                break
            except:
                self.speak(text)
                break

    # Chạy Thread nhận dạng giọng nói. Result được truyền vào function và thực hiện function sau sec (giây) đã đặt
    def get_text_from_audio(self, function, sec):
        worker = Thread(self.speech_recognition, sec)
        worker.signals.result.connect(function)
        self.threadpool.start(worker)

    # Speech to text
    def speech_recognition(self):
        self.set_label("Đang lắng nghe...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=5)
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
        playsound("notification.wav", False)
        self.set_plain_text_edit("Tôi có thể giúp gì cho bạn?")
        self.get_text_from_audio(self.request, 0.3)

    # Yêu cầu chức năng
    def request(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
            pass
        elif "trợ giúp" in text or "help" in text:
            self.help_me()
        elif "chào" in text or "hello" in text:
            self.greeting()
        elif "hôm nay" in text or "bữa nay" in text or "hiện tại" in text or "bây giờ" in text:
            self.get_time(text)
        elif "mở nhạc" in text or "mở video" in text:
            self.play_song()
        elif "thời tiết" in text:
            self.what_weather(text)
        elif "tin tức" in text:
            self.read_news()
        elif "tra cứu" in text:
            self.lookup_wikipedia()
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
        self.speak("Tôi có thể giúp bạn làm những việc sau đây.")
        self.set_plain_text_edit("""Tôi có thể giúp bạn thực hiện những việc sau đây:
        1. Hiển thị ngày giờ
        2. Mở video nhạc trên Youtube
        3. Xem dự báo thời tiết
        4. Đọc tin tức, thời sự
        5. Tra cứu định nghĩa với Wikipedia
        6. Mở ứng dụng, phần mềm
        7. Mở website
        8. Tra cứu từ điển
        9. Tìm kiếm từ khóa với Google""")

    # 2. Chào hỏi
    def greeting(self):
        day_time = int(strftime("%H"))
        if day_time < 12:
            self.response("Chào buổi sáng. Chúc bạn một ngày tốt lành!")
        elif 12 <= day_time < 18:
            self.response(
                "Chào buổi chiều. Bạn đã dự định gì cho chiều này chưa?")
        else:
            self.response("Chào buổi tối. Chúc bạn buổi tối vui vẻ.")

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
            pass

    # 4. Mở video trên Youtube
    def play_song(self):
        self.response("Bạn muốn nghe bài gì?")
        self.get_text_from_audio(self.search_music_thread, 1)

    def search_music_thread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = Thread(self.search_music, text, 0)
            worker.signals.finished.connect(self.play_song_complete)
            self.threadpool.start(worker)
            self.set_plain_text_edit("Đang mở. Vui lòng đợi...")

    def search_music(self, text):
        result = search_youtube([text])
        # result = YoutubeSearch(text, max_results=3).to_dict()
        url = "https://www.youtube.com/watch?v=" + result[0]["id"]
        # url = "https://www.youtube.com/" + result[0]["url_suffix"]
        webbrowser.open(url)

    def play_song_complete(self):
        self.speak("Đã mở bài hát bạn yêu cầu.")
        self.set_plain_text_edit("Đã mở bài hát bạn yêu cầu.")

    # 5. Xem dự báo thời tiết
    def what_weather(self, text):
        if "tỉnh" in text:
            reg_ex = re.search("tỉnh", text)
            if reg_ex:
                start = reg_ex.end() + 1
                end = len(text)
                city = text[start:end]
            else:
                city = "none"
        elif "thành phố" in text:
            reg_ex = re.search("thành phố", text)
            if reg_ex:
                start = reg_ex.end() + 1
                end = len(text)
                city = text[start:end]
            else:
                city = "none"
        else:
            city = "default"

        self.search_weather_thread(city)

    def search_weather_thread(self, text):
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")
        if "none" in text:
            self.response("Xin lỗi, không tìm thấy địa điểm đã nói.")
        elif "default" in text:
            worker = Thread(self.search_weather_default, 0)
            worker.signals.result.connect(self.what_weather_complete)
            self.threadpool.start(worker)
        else:
            worker = Thread(self.search_weather, text, 0)
            worker.signals.result.connect(self.what_weather_complete)
            self.threadpool.start(worker)

    def search_weather_default(self):
        get_IP = requests.get("https://api.myip.com").json()
        url = "https://ipinfo.io/{}/city?token=0b031e6458a2a9".format(
            get_IP["ip"])
        name_city = requests.get(url).text

        geolocator = Nominatim(user_agent="Virtual Assistant")
        location = geolocator.geocode(name_city)

        api = "4e7ced343986de64b7f54296a111c208"
        lat = location.latitude
        lon = location.longitude
        part = "minutely,hourly,daily,alerts"
        units = "metric"
        lang = "vi"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
        url_one_call = url.format(lat, lon, part, units, lang, api)
        response = requests.get(url_one_call).json()

        # c_lat = response["lat"]
        # c_lon = response["lon"]
        # c_cur_time = response["current"]["dt"]
        # c_sunrise = response["current"]["sunrise"]
        # c_sunset = response["current"]["sunset"]
        c_temp = response["current"]["temp"]
        # c_feel_like = response["current"]["feels_like"]
        c_presure = response["current"]["pressure"]
        c_humidity = response["current"]["humidity"]
        # c_dew_point = response["current"]["dew_point"]
        c_clouds = response["current"]["clouds"]
        # c_uvi = response["current"]["uvi"]
        # c_visibility = response["current"]["visibility"]
        c_wind_speed = response["current"]["wind_speed"]
        # c_wind_gust = response["current"]["wind_gust"]
        # c_wind_deg = response["current"]["wind_deg"]
        c_weather_id = response["current"]["weather"][0]["id"]
        c_weather_main = response["current"]["weather"][0]["main"]
        c_weather_description = response["current"]["weather"][0]["description"]
        c_weather_icon = response["current"]["weather"][0]["icon"]

        string = """Dự báo thời tiết {}:
    Nhiệt độ: {} độ C
    Độ ẩm: {}%
    Mây: {}%
    Tốc độ gió: {}m/s
    Tình trạng: {}.
    """

        result = {
            "weather": string.format(name_city, c_temp, c_humidity, c_clouds, c_wind_speed,
                                     c_weather_description),
            "string": "Dự báo thời tiết cho {} hôm nay.".format(name_city)
        }
        return result

    def search_weather(self, city):
        name_city = city
        geolocator = Nominatim(user_agent="Virtual Assistant")
        location = geolocator.geocode(name_city)

        api = "4e7ced343986de64b7f54296a111c208"
        lat = location.latitude
        lon = location.longitude
        part = "minutely,hourly,daily,alerts"
        units = "metric"
        lang = "vi"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
        url_one_call = url.format(lat, lon, part, units, lang, api)
        response = requests.get(url_one_call).json()

        # c_lat = response["lat"]
        # c_lon = response["lon"]
        # c_cur_time = response["current"]["dt"]
        # c_sunrise = response["current"]["sunrise"]
        # c_sunset = response["current"]["sunset"]
        c_temp = response["current"]["temp"]
        # c_feel_like = response["current"]["feels_like"]
        c_presure = response["current"]["pressure"]
        c_humidity = response["current"]["humidity"]
        # c_dew_point = response["current"]["dew_point"]
        c_clouds = response["current"]["clouds"]
        # c_uvi = response["current"]["uvi"]
        # c_visibility = response["current"]["visibility"]
        c_wind_speed = response["current"]["wind_speed"]
        # c_wind_gust = response["current"]["wind_gust"]
        # c_wind_deg = response["current"]["wind_deg"]
        c_weather_id = response["current"]["weather"][0]["id"]
        c_weather_main = response["current"]["weather"][0]["main"]
        c_weather_description = response["current"]["weather"][0]["description"]
        c_weather_icon = response["current"]["weather"][0]["icon"]

        string = """Dự báo thời tiết {}:
    Nhiệt độ: {} độ C
    Độ ẩm: {}%
    Mây: {}%
    Tốc độ gió: {}m/s
    Tình trạng: {}.
    """

        result = {
            "weather": string.format(name_city, c_temp, c_humidity,
                                     c_clouds, c_wind_speed, c_weather_description),
            "string": "Dự báo thời tiết cho {} hôm nay.".format(name_city)
        }
        return result

    def what_weather_complete(self, result):
        self.set_plain_text_edit(result["weather"])
        self.speak(result["string"])

    # 6. Đọc báo rss news
    def read_news(self):
        self.response("Bạn muốn xem tin tức gì?")
        self.get_text_from_audio(self.search_news_thread, 1.7)

    def search_news_thread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = Thread(self.search_news, text, 0)
            worker.signals.result.connect(self.read_news_complete)
            self.threadpool.start(worker)
            self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search_news(self, text):
        params = {
            "apiKey": "30d02d187f7140faacf9ccd27a1441ad",
            "q": text,
        }
        api_result = requests.get(
            "http://newsapi.org/v2/top-headlines?", params)
        api_response = api_result.json()
        content = ""

        for number, articles in enumerate(api_response["articles"], start=1):
            if number > 5:
                break
            else:
                string = "[No.{}]\n[Title] {}\n[Description] {}\n[Link] {}\n\n"
                news = string.format(
                    number, articles["title"], articles["description"], articles["url"])
                content = content + news

        if content == "":
            result = {
                "content": "Không tìm thấy tin tức về {}.".format(text),
                "string": "Không tìm thấy tin tức về {}.".format(text)
            }
        else:
            result = {
                "content": content,
                "string": "Đây là các tin tức về {}".format(text)
            }

        return result

    def read_news_complete(self, result):
        self.set_plain_text_edit(result["content"])
        self.speak(result["string"])

    # 7. Tìm kiếm định nghĩa wikipedia
    def lookup_wikipedia(self):
        self.response("Bạn muốn tra cứu từ gì?")
        self.get_text_from_audio(self.search_wiki_thread, 1.5)

    def search_wiki_thread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = Thread(self.search_wiki, text, 0)
            worker.signals.result.connect(self.lookup_wikipedia_complete)
            self.threadpool.start(worker)
            self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search_wiki(self, text):
        wikipedia.set_lang('vi')
        content = "[Wikipedia vi-VN]\n" + wikipedia.summary(text)
        result = {
            "content": content,
            "string": "Đây là kết quả từ Wikipedia"
        }

        return result

    def lookup_wikipedia_complete(self, result):
        self.set_plain_text_edit(result["content"])
        self.speak(result["string"])

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
            self.response("Không tìm thấy ứng dụng bạn yêu cầu.")

    def search_app_thread(self, fileName, fullName):
        worker = Thread(self.search_app, fileName, fullName, 0)
        worker.signals.result.connect(self.open_application_complete)
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
            self.response("Đã mở ứng dụng {}.".format(fullName))

    # 9. Mở website
    def open_website(self, text):
        self.search_web_thread(text)

    def search_web_thread(self, text):
        worker = Thread(self.search_web, text, 0)
        worker.signals.finished.connect(self.open_website_complete)
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

    # 10. Tìm kiếm bằng google engine của trình duyệt mặc định
    def search_default(self, text):
        self.search_thread(text)

    def search_thread(self, text):
        worker = Thread(self.search, text, 0)
        worker.signals.result.connect(self.search_default_complete)
        self.threadpool.start(worker)
        self.set_plain_text_edit("Đang tìm kiếm. Vui lòng đợi...")

    def search(self, text):
        service = build("customsearch", "v1",
                        developerKey="AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw")
        response = service.cse().list(q=text, cx="efcdf7a6d77b621bc", num="3", fields="context/title, items/displayLink, \
            items/formattedUrl, items/link, items/snippet, items/title, searchInformation/formattedSearchTime, \
                searchInformation/formattedTotalResults").execute()
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
        self.translate_thread()

    def translate_thread(self):
        worker = ThreadD(self.translate)
        worker.signals.result.connect(self.set_plain_text_edit)
        self.set_plain_text_edit("Đã bật từ điển.")
        self.threadpool.start(worker)

    # TODO Ghi nhớ clipboard do user copy vào 1 biến tạm, sau khi kết thúc thì đưa lại vào clipboard
    def translate(self):
        keyboard = Controller()
        translator = Translator()
        result = ""

        def on_move(x, y):
            global chain
            chain.append(2)

        def on_click(x, y, button, pressed):
            global chain
            if pressed:
                chain.append(1)
            else:
                chain.append(3)
                return False

        with mouse.Listener(on_move=on_move, on_click=on_click) as mouseListener:
            mouseListener.join()

        if chain[-2] != 1:
            keyboard.press(Key.ctrl)
            keyboard.press("c")
            keyboard.release(Key.ctrl)
            keyboard.release("c")
            time.sleep(0.05)

            str_from_clipboard = pyperclip.paste()

            if str_from_clipboard != "":
                content = translator.translate(str_from_clipboard, dest="vi")
                result = "[Nguồn] {0}\n[Đích] {1}\n[Kết quả]\n{2}".format(
                    content.src, content.dest, content.text)
            pyperclip.copy("")

        return result


#* ================================ FUNCITON MAIN ==================================== #


if __name__ == "__main__":
    Assistant()
