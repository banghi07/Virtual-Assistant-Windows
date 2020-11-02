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
from googleapiclient.discovery import build
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from youtube_search import YoutubeSearch

from mainwindow import Ui_MainWindow

# from ctypes import windll

drive = "C:/"


def findApp(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


class threadSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class thread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(thread, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = threadSignals()

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


class assistant():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.threadpool = QThreadPool()
        self.setWidgets()
        self.initialAssistant()
        self.MainWindow.show()
        sys.exit(app.exec_())

    # ================================ SET & GET FUNCTIONS ==================================== #

    # Đặt title cho dialog
    def setWidgets(self):
        self.MainWindow.setWindowTitle('Virtual Assistant- PyQt5')
        self.MainWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.MainWindow.setFixedSize(
            self.MainWindow.width(), self.MainWindow.height())

    # Đặt text cho PlainTextEdit
    def setPlainTextEdit(self, text):
        self.ui.plainTextEdit.setPlainText(text)

    # Đặt text cho Label
    def setLabel(self, text):
        self.ui.label.setText(text)

    # Đặt text cho PlainTextEdit và Speak text đã đặt
    def response(self, text):
        self.setPlainTextEdit(text)
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

    # Chạy thread nhận dạng giọng nói. Result được truyền vào function và thực hiện function sau sec (giây) đã đặt
    def getTextFromAudio(self, function, sec):
        worker = thread(self.speechRecognition, sec)
        worker.signals.result.connect(function)
        self.threadpool.start(worker)

    # Speech to text
    def speechRecognition(self):
        self.setLabel("Đang lắng nghe...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                self.setLabel(text.lower())
                return text.lower()
            except:
                self.setLabel("...")
                return "none"

   # ================================ CALL ASSISTANT ==================================== #

    # Khởi tạo ban đầu
    def initialAssistant(self):
        self.ui.pushButton.pressed.connect(self.callAssistant)

    # Gọi trợ lý ảo
    def callAssistant(self):
        playsound("notification.wav", False)
        self.setPlainTextEdit("Tôi có thể giúp gì cho bạn?")
        self.getTextFromAudio(self.request, 0.3)

    # Yêu cầu chức năng
    def request(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
            pass
        elif "trợ giúp" in text or "help" in text:
            self.helpMe()
        elif "chào" in text or "hello" in text:
            self.greeting()
        elif "hôm nay" in text or "bữa nay" in text or "hiện tại" in text or "bây giờ" in text:
            self.getTime(text)
        elif "mở nhạc" in text or "mở video" in text:
            self.playSong()
        elif "thời tiết" in text:
            self.whatWeather()
        elif "tin tức" in text:
            self.readNews()
        elif "tra cứu" in text:
            self.lookupWikipedia()
        elif "mở" in text:
            if "." in text:
                self.openWebsite(text)
            else:
                self.openApplication(text)
        elif "từ điển" in text:
            self.translation()
        else:
            self.searchDefault(text)
    # ================================= ASSISTANT FUNCTIONS =================================== #

    # 1. Trợ giúp
    def helpMe(self):
        self.speak("Tôi có thể giúp bạn làm những việc sau đây.")
        self.setPlainTextEdit("""Tôi có thể giúp bạn thực hiện những việc sau đây:
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
    def getTime(self, text):
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
    def playSong(self):
        self.response("Bạn muốn nghe bài gì?")
        self.getTextFromAudio(self.searchMusicThread, 1)

    def searchMusicThread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = thread(self.searchMusic, text, 0)
            worker.signals.finished.connect(self.playSongComplete)
            self.threadpool.start(worker)
            self.setPlainTextEdit("Đang mở. Vui lòng đợi...")

    def searchMusic(self, text):
        result = search_youtube([text])
        # result = YoutubeSearch(text, max_results=3).to_dict()
        url = "https://www.youtube.com/watch?v=" + result[0]["id"]
        # url = "https://www.youtube.com/" + result[0]["url_suffix"]
        webbrowser.open(url)

    def playSongComplete(self):
        self.speak("Đã mở bài hát bạn yêu cầu.")
        self.setPlainTextEdit("Đã mở bài hát bạn yêu cầu.")

    # 5. Xem dự báo thời tiết
    def whatWeather(self):
        self.response("Bạn muốn xem thời tiết ở đâu?")
        self.getTextFromAudio(self.searchWeatherThread, 2)

    def searchWeatherThread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = thread(self.searchWeather, text, 0)
            worker.signals.result.connect(self.whatWeatherComplete)
            self.threadpool.start(worker)
            self.setPlainTextEdit("Đang tìm kiếm. Vui lòng đợi...")

    def searchWeather(self, city):
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            ccurrent_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.datetime.now()

            result = {
                "content": "Ngày {day} tháng {month} năm {year}\nNhiệt độ trung bình: {temp} độ C\nÁp suất không khí: {pressure} hPa\nĐộ ẩm: {humidity}%\nDự báo: {description}.".format(
                    city=city, day=now.day, month=now.month, year=now.year, temp=current_temperature,
                    pressure=current_pressure, humidity=ccurrent_humidity, description=weather_description),

                "string": "Dự báo thời tiết {city} hôm nay".format(city=city)
            }
        else:
            result = {
                "content": "Không tìm thấy địa chỉ mà bạn nói!",
                "string": "Không tìm thấy địa chỉ mà bạn nói!"
            }

        return result

    def whatWeatherComplete(self, result):
        self.setPlainTextEdit(result["content"])
        self.speak(result["string"])

    # 6. Đọc báo rss news
    def readNews(self):
        self.response("Bạn muốn xem tin tức gì?")
        self.getTextFromAudio(self.searchNewsThread, 1.7)

    def searchNewsThread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = thread(self.searchNews, text, 0)
            worker.signals.result.connect(self.readNewsComplete)
            self.threadpool.start(worker)
            self.setPlainTextEdit("Đang tìm kiếm. Vui lòng đợi...")

    def searchNews(self, text):
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
                news = "[No.{number}]\n[Title] {title}\n[Description] {description}\n[Link] {url}\n\n".format(number=number,
                                                                                                              title=articles["title"], description=articles["description"], url=articles["url"])
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

    def readNewsComplete(self, result):
        self.setPlainTextEdit(result["content"])
        self.speak(result["string"])

    # 7. Tìm kiếm định nghĩa wikipedia
    def lookupWikipedia(self):
        self.response("Bạn muốn tra cứu từ gì?")
        self.getTextFromAudio(self.searchWikiThread, 1.5)

    def searchWikiThread(self, text):
        if "none" in text:
            self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
        else:
            worker = thread(self.searchWiki, text, 0)
            worker.signals.result.connect(self.lookupWikipediaComplete)
            self.threadpool.start(worker)
            self.setPlainTextEdit("Đang tìm kiếm. Vui lòng đợi...")

    def searchWiki(self, text):
        wikipedia.set_lang('vi')
        content = "[Wikipedia vi-VN]\n" + wikipedia.summary(text)
        result = {
            "content": content,
            "string": "Đây là kết quả từ Wikipedia"
        }

        return result

    def lookupWikipediaComplete(self, result):
        self.setPlainTextEdit(result["content"])
        self.speak(result["string"])

    # 8. Mở phần mềm ứng dụng
    def openApplication(self, text):
        if "edge" in text:
            self.searchAppThread("msedge.exe", "Microsoft Edge")
        elif "chrome" in text:
            self.searchAppThread("chrome.exe", "Google Chrome")
        elif "word" in text:
            self.searchAppThread("WINWORD.EXE", "Microsoft Word")
        elif "excel" in text:
            self.searchAppThread("EXCEL.EXE", "Microsoft Excel")
        elif "powerpoint" in text:
            self.searchAppThread("POWERPNT.EXE", "Microsoft PowerPoint")
        else:
            self.response("Không tìm thấy ứng dụng bạn yêu cầu.")

    def searchAppThread(self, fileName, fullName):
        worker = thread(self.searchApp, fileName, fullName, 0)
        worker.signals.result.connect(self.openApplicationComplete)
        self.threadpool.start(worker)
        self.setPlainTextEdit("Đang mở ứng dụng. Vui lòng đợi...")

    def searchApp(self, fileName, fullName):
        path = findApp(fileName, drive)
        if path:
            os.startfile(path)
        else:
            fullName = "none"

        return fullName

    def openApplicationComplete(self, fullName):
        if "none" in fullName:
            self.response("Ứng dụng bạn yêu cầu chưa được cài đặt.")
        else:
            self.response("Đã mở ứng dụng {}.".format(fullName))

    # 9. Mở website
    def openWebsite(self, text):
        self.searchWebThread(text)

    def searchWebThread(self, text):
        worker = thread(self.searchWeb, text, 0)
        worker.signals.finished.connect(self.openWebsiteComplete)
        self.threadpool.start(worker)
        self.setPlainTextEdit("Đang mở Website. Vui lòng đợi...")

    def searchWeb(self, text):
        reg_ex = re.search("mở (.+)", text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)
            return True
        else:
            return False

    def openWebsiteComplete(self):
        self.response("Đã mở trang web bạn yêu cầu.")

    # 10. Tìm kiếm bằng google engine của trình duyệt mặc định
    def searchDefault(self, text):
        self.searchThread(text)

    def searchThread(self, text):
        worker = thread(self.search, text, 0)
        worker.signals.result.connect(self.searchDefaultComplete)
        self.threadpool.start(worker)
        self.setPlainTextEdit("Đang tìm kiếm. Vui lòng đợi...")

    def search(self, text):
        service = build("customsearch", "v1",
                        developerKey="AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw")
        response = service.cse().list(q=text, cx="efcdf7a6d77b621bc", num="3", fields="context/title, items/displayLink, \
            items/formattedUrl, items/link, items/snippet, items/title, searchInformation/formattedSearchTime, \
                searchInformation/formattedTotalResults").execute()
        content = "[{title}]\nKhoảng {totalResults} kết quả ({searchTime} giây)\n\n".format(
            title=response["context"]["title"], totalResults=response["searchInformation"]["formattedTotalResults"],
            searchTime=response["searchInformation"]["formattedSearchTime"])

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

    def searchDefaultComplete(self, result):
        self.setPlainTextEdit(result["content"])
        self.speak(result["string"])

    # 11. Dịch nghĩa sang tiếng Việt
    def translation(self):
        self.translateThread()

    def translateThread(self):
        worker = thread(self.translateGG, 0)
        worker.signals.result.connect(self.translationComplete)
        self.threadpool.start(worker)
        self.setPlainTextEdit("Chọn từ hoặc câu để dịch sang tiếng Việt.")

    def translateGG(self):
        keyboard = Controller()
        translator = Translator()

        # def clearClipboard():
        #     win32clipboard.OpenClipboard()
        #     win32clipboard.EmptyClipboard()
        #     win32clipboard.CloseClipboard()

        # def clearClb():
        #     if windll.user32.OpenClipboard(None):
        #         windll.user32.EmptyClipboard()
        #         windll.user32.CloseClipboard()

        def on_click(x, y, button, pressed):
            if not pressed:
                keyboard.press(Key.ctrl)
                keyboard.press("c")
                keyboard.release(Key.ctrl)
                keyboard.release("c")
                time.sleep(0.05)
                return False  # False to stop listener

        with mouse.Listener(on_click=on_click) as mouseListener:
            mouseListener.join()
        strFromClipBoard = pyperclip.paste()
        pyperclip.copy("")
        result = translator.translate(strFromClipBoard, dest="vi")

        content = "[src] {0}\n[origin] {1}\n\n[dest] {2}\n[translate] {3}".format(
            result.src, result.origin, result.dest, result.text)
        return content

    def translationComplete(self, text):
        self.setPlainTextEdit(text)
        self.speak("Đã dịch xong.")


# ================================ FUNCITON MAIN ==================================== #
if __name__ == "__main__":
    assistant()
