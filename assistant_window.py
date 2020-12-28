import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser


class Window(QMainWindow):
    def __init__(self, option=0):
        super().__init__()
        self.setStyleSheet(open("./themes/light.css").read())
        self.widget_container = QWidget()
        self.widget_container.setObjectName("widget_container")
        self.layout_container = QVBoxLayout(self.widget_container)

        if option:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
            self.layout_container.setContentsMargins(0, 0, 0, 0)
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.layout_container.setContentsMargins(10, 10, 10, 10)

        self.setCentralWidget(self.widget_container)

    def set_shadow_window(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setObjectName("shadow_window")
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor("#666666"))
        self.shadow.setOffset(0.0, 0.0)

        for i in range(self.layout_container.count()):
            self.layout_container.itemAt(i).widget().setGraphicsEffect(self.shadow)

    def set_center_screen(self):
        desktop = QDesktopWidget()
        screen_width = desktop.width()
        screen_height = desktop.height()

        x = (screen_width - self.width()) / 2
        y = (screen_height - self.height()) / 2

        self.move(round(x), round(y))

    def set_location_window(self, result):
        desktop = QDesktopWidget()
        screen_width = desktop.width()
        screen_height = desktop.height()

        window_pos = QPoint()

        if result["cursor_pos"].x() + 10 + self.width() >= screen_width:
            window_pos.setX(result["cursor_pos"].x() - 10 - self.width())
        else:
            window_pos.setX(result["cursor_pos"].x() + 10)

        if result["cursor_pos"].y() + 20 + self.height() >= screen_height:
            window_pos.setY(result["cursor_pos"].y() - 15 - self.height())
        else:
            window_pos.setY(result["cursor_pos"].y() + 20)

        self.move(window_pos)


class UI_Windows(object):
    # * Init button, title & bottom bar
    def __init__(self):
        self.init_button_close()
        self.init_button_microphone()
        self.init_topic_button()
        self.init_title_bar()
        self.init_bottom_bar()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def clear_UI(self, MainWindow):
        self.clear_layout(MainWindow.layout_container)

    def init_button_close(self):
        self.button_close = QPushButton()
        self.button_close.setObjectName("button_close")
        self.button_close.setFixedSize(35, 35)
        self.button_close.setIcon(QIcon("./icon/close-32px.png"))

    def init_button_microphone(self):
        self.button_microphone = QPushButton()
        self.button_microphone.setObjectName("button_microphone")
        self.button_microphone.setFixedSize(40, 40)
        self.button_microphone.setIcon(QIcon("./icon/microphone-32px.png"))

    def init_topic_button(self):
        self.topic_button_1 = QPushButton("Mới Nhất")
        self.topic_button_1.setObjectName("topic_button_1")

        self.topic_button_2 = QPushButton("Nổi Bật")
        self.topic_button_2.setObjectName("topic_button_2")

        self.topic_button_3 = QPushButton("Giải trí")
        self.topic_button_3.setObjectName("topic_button_3")

        self.topic_button_4 = QPushButton("Thể Thao")
        self.topic_button_4.setObjectName("topic_button_4")

        self.topic_button_5 = QPushButton("Khoa Học")
        self.topic_button_5.setObjectName("topic_button_5")

    def init_title_bar(self):
        self.widget_title_bar = QWidget()
        self.widget_title_bar.setObjectName("widget_title_bar")

        self.layout_title_bar = QHBoxLayout(self.widget_title_bar)
        self.layout_title_bar.setContentsMargins(0, 0, 0, 0)

        self.layout_title_bar.addStretch()
        self.layout_title_bar.addWidget(self.button_close)

    def init_bottom_bar(self):
        self.widget_bottom_bar = QWidget()
        self.widget_bottom_bar.setObjectName("widget_bottom_bar")

        self.layout_bottom_bar = QHBoxLayout(self.widget_bottom_bar)
        self.layout_bottom_bar.setContentsMargins(0, 0, 0, 0)
        self.layout_bottom_bar.setSpacing(0)

    def update_bottom_bar(self, *args):
        self.clear_layout(self.layout_bottom_bar)
        if len(args) > 0:
            if "0" in str(list(args)[0]):
                self.label_assistant_listening = QLabel("Đang lắng nghe...")
                self.label_assistant_listening.setObjectName(
                    "label_assistant_listening"
                )

                self.icon_sound_waves = QPushButton()
                self.icon_sound_waves.setObjectName("icon_sound_waves")
                self.icon_sound_waves.setFixedSize(40, 40)
                self.icon_sound_waves.setIcon(QIcon("./icon/audio-waves-32px.png"))

                self.layout_bottom_bar.addWidget(self.icon_sound_waves)
                self.layout_bottom_bar.addWidget(self.label_assistant_listening)
                self.layout_bottom_bar.addStretch()

            elif "1" in str(list(args)[0]):
                self.layout_bottom_bar.addStretch()
                self.layout_bottom_bar.addWidget(self.button_microphone)

            else:
                text = str(list(args)[0])
                self.label_user_answer = QLabel(text)
                self.label_user_answer.setObjectName("label_user_answer")

                self.icon_user_message = QPushButton()
                self.icon_user_message.setObjectName("icon_user_message")
                self.icon_user_message.setFixedSize(40, 40)
                self.icon_user_message.setIcon(QIcon("./icon/message-32px.png"))

                self.layout_bottom_bar.addWidget(self.icon_user_message)
                self.layout_bottom_bar.addWidget(self.label_user_answer)
                self.layout_bottom_bar.addStretch()

        else:
            pass

    def init_button_close_2(self):
        self.button_close_2 = QPushButton()
        self.button_close_2.setObjectName("button_close_2")
        self.button_close_2.setFixedSize(10, 10)
        self.button_close_2.setIcon(QIcon("./icon/cancel-16px.png"))

    def init_button_speak_En(self):
        self.button_speak_En = QPushButton()
        self.button_speak_En.setObjectName("button_speak_En")
        self.button_speak_En.setFixedSize(24, 24)
        self.button_speak_En.setIcon(QIcon("./icon/speaker-32px.png"))

    def init_button_speak_Vi(self):
        self.button_speak_Vi = QPushButton()
        self.button_speak_Vi.setObjectName("button_speak_Vi")
        self.button_speak_Vi.setFixedSize(24, 24)
        self.button_speak_Vi.setIcon(QIcon("./icon/speaker-32px.png"))

    def add_widget_space_vertical(self, height, layout):
        widget_spaceV = QWidget()
        widget_spaceV.setFixedHeight(height)

        layout.addWidget(widget_spaceV)

    def add_widget_space_horizontal(self, width, layout):
        widget_spaceH = QWidget()
        widget_spaceH.setFixedWidth(width)

        layout.addWidget(widget_spaceH)

    # * UI main window
    def setupUI_main_window(self, MainWindow):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(520, 470)

        self.widget_main_window = QWidget()
        self.widget_main_window.setObjectName("widget_main_window")

        self.layout_main_window = QVBoxLayout(self.widget_main_window)
        self.layout_main_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(500, 35)
        self.layout_main_window.addWidget(self.widget_title_bar)

        self.display_listen_animated()

        self.display_assistant_ask()

        self.display_assistant_hint()

        self.layout_main_window.addStretch()

        self.widget_bottom_bar.setFixedSize(500, 40)
        self.layout_main_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(0)

        MainWindow.layout_container.addWidget(self.widget_main_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_listen_animated(self):
        self.widget_listen_animated = QWidget()
        self.widget_listen_animated.setObjectName("widget_listen_animated")

        self.layout_listen_animated = QHBoxLayout(self.widget_listen_animated)
        self.layout_listen_animated.setContentsMargins(0, 0, 0, 0)

        url_listen_gif = "./icon/Ripple-0.7s-170px.gif"
        listen_gif = QMovie(url_listen_gif)
        listen_gif.start()

        label_listen_animated = QLabel()
        label_listen_animated.setMovie(listen_gif)
        label_listen_animated.setScaledContents(True)
        label_listen_animated.setFixedSize(170, 170)

        self.layout_listen_animated.addWidget(label_listen_animated)

        self.layout_main_window.addWidget(self.widget_listen_animated)

    def display_assistant_ask(self):
        self.widget_assistant_ask = QWidget()
        self.widget_assistant_ask.setObjectName("widget_assistant_ask")

        self.layout_assistant_ask = QHBoxLayout(self.widget_assistant_ask)
        self.layout_assistant_ask.setContentsMargins(0, 0, 0, 0)

        label_assistant_ask = QLabel("Bạn có yêu cầu gì không?")
        label_assistant_ask.setObjectName("label_assistant_ask")

        self.layout_assistant_ask.addStretch()
        self.layout_assistant_ask.addWidget(label_assistant_ask)
        self.layout_assistant_ask.addStretch()

        self.layout_main_window.addWidget(self.widget_assistant_ask)

    def display_assistant_hint(self):
        self.widget_assistant_hint = QWidget()
        self.widget_assistant_hint.setObjectName("widget_assistant_hint")

        self.layout_assistant_hint = QHBoxLayout(self.widget_assistant_hint)
        self.layout_assistant_hint.setContentsMargins(0, 0, 0, 0)

        label_assistant_hint = QLabel('Thử gọi "Trợ giúp"')
        label_assistant_hint.setObjectName("label_assistant_hint")

        self.layout_assistant_hint.addStretch()
        self.layout_assistant_hint.addWidget(label_assistant_hint)
        self.layout_assistant_hint.addStretch()

        self.layout_main_window.addWidget(self.widget_assistant_hint)

    # * UI response window
    def setupUI_response_window(self, MainWindow, url, text, option=0):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(520, 470)

        self.widget_response_window = QWidget()
        self.widget_response_window.setObjectName("widget_response_window")

        self.layout_response_window = QVBoxLayout(self.widget_response_window)
        self.layout_response_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(500, 35)
        self.layout_response_window.addWidget(self.widget_title_bar)

        self.display_response_image(url)

        self.display_response_details(text)

        if option:
            widget_contain = QWidget()
            layout_contain = QHBoxLayout(widget_contain)

            button_ok = QPushButton("OK! Đã hiểu")
            button_ok.setObjectName("button_ok")
            button_ok.clicked.connect(lambda: MainWindow.close())

            layout_contain.addStretch()
            layout_contain.addWidget(button_ok)
            layout_contain.addStretch()

            self.add_widget_space_vertical(30, self.layout_response_window)
            self.layout_response_window.addWidget(widget_contain)

        self.layout_response_window.addStretch()

        self.widget_bottom_bar.setFixedSize(500, 40)
        self.layout_response_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_response_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_response_image(self, url):
        self.widget_response_image = QWidget()
        self.widget_response_image.setObjectName("widget_response_image")

        self.layout_response_image = QHBoxLayout(self.widget_response_image)
        self.layout_response_image.setContentsMargins(0, 0, 0, 0)

        label_response_image = QLabel()
        label_response_image.setObjectName("label_response_image")
        label_response_image.setPixmap(QPixmap(url))
        label_response_image.setScaledContents(True)
        label_response_image.setFixedSize(170, 170)

        self.layout_response_image.addWidget(label_response_image)

        self.layout_response_window.addWidget(self.widget_response_image)

    def display_response_details(self, text):
        self.widget_response_details = QWidget()
        self.widget_response_details.setObjectName("widget_response_details")

        self.layout_response_details = QHBoxLayout(self.widget_response_details)
        self.layout_response_details.setContentsMargins(0, 0, 0, 0)

        label_response_details = QLabel(text)
        label_response_details.setObjectName("label_response_details")

        self.layout_response_details.addStretch()
        self.layout_response_details.addWidget(label_response_details)
        self.layout_response_details.addStretch()

        self.layout_response_window.addWidget(self.widget_response_details)

    def setupUI_clock_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(520, 470)

        self.widget_clock_window = QWidget()
        self.widget_clock_window.setObjectName("widget_clock_window")

        self.layout_clock_window = QVBoxLayout(self.widget_clock_window)
        self.layout_clock_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(500, 35)
        self.layout_clock_window.addWidget(self.widget_title_bar)

        self.add_widget_space_vertical(50, self.layout_clock_window)

        s = result["zone_name"] + ", " + "UTC " + result["utc"]
        self.display_time_zone(s)
        self.layout_clock_window.addWidget(self.widget_time_zone)

        self.add_widget_space_vertical(30, self.layout_clock_window)

        self.display_clock(result["hour"], result["minute"], result["second"])

        self.add_widget_space_vertical(15, self.layout_clock_window)

        self.display_date_in_clock_window(
            result["day"], result["month"], result["year"]
        )

        self.layout_clock_window.addStretch()

        self.widget_bottom_bar.setFixedSize(500, 40)
        self.layout_clock_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_clock_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_time_zone(self, text):
        self.widget_time_zone = QWidget()
        self.widget_time_zone.setObjectName("widget_time_zone")

        self.layout_time_zone = QHBoxLayout(self.widget_time_zone)
        self.layout_time_zone.setContentsMargins(0, 0, 0, 0)

        icon_time_zone = QLabel()
        icon_time_zone.setObjectName("icon_time_zone")
        icon_time_zone.setPixmap(QPixmap("./icon/time-zone-32px.png"))
        icon_time_zone.setScaledContents(True)
        icon_time_zone.setFixedSize(32, 32)

        s = "<b>" + text + "</b>"
        label_time_zone = QLabel(s)
        label_time_zone.setObjectName("label_time_zone")

        self.layout_time_zone.addStretch()
        self.layout_time_zone.addWidget(icon_time_zone)
        self.layout_time_zone.addWidget(label_time_zone)
        self.layout_time_zone.addStretch()

    def display_clock(self, h, m, s):
        self.widget_clock = QWidget()
        self.widget_clock.setObjectName("widget_clock")

        self.layout_clock = QHBoxLayout(self.widget_clock)
        self.layout_clock.setContentsMargins(0, 0, 0, 0)

        label_hour = QLabel(h)
        label_hour.setObjectName("label_hour")

        label_colon = QLabel(":")
        label_colon.setObjectName("label_colon")

        label_minute = QLabel(m)
        label_minute.setObjectName("label_minute")

        label_colon2 = QLabel(":")
        label_colon2.setObjectName("label_colon2")

        label_second = QLabel(s)
        label_second.setObjectName("label_second")

        self.layout_clock.addStretch()
        self.layout_clock.addWidget(label_hour)
        self.layout_clock.addWidget(label_colon)
        self.layout_clock.addWidget(label_minute)
        self.layout_clock.addWidget(label_colon2)
        self.layout_clock.addWidget(label_second)
        self.layout_clock.addStretch()

        self.layout_clock_window.addWidget(self.widget_clock)

    def display_date_in_clock_window(self, d, m, y):
        self.widget_date_in_clock_window = QWidget()
        self.widget_date_in_clock_window.setObjectName("widget_date_in_clock_window")

        self.layout_date_in_clock_window = QHBoxLayout(self.widget_date_in_clock_window)
        self.layout_date_in_clock_window.setContentsMargins(0, 0, 0, 0)

        icon_date = QLabel()
        icon_date.setObjectName("icon_date")
        icon_date.setPixmap(QPixmap("./icon/calendar-32px.png"))
        icon_date.setScaledContents(True)
        icon_date.setFixedSize(25, 25)

        date = d + "/" + m + "/" + y

        label_date_in_clock_window = QLabel(date)
        label_date_in_clock_window.setObjectName("label_date_in_clock_window")

        self.layout_date_in_clock_window.addStretch()
        self.layout_date_in_clock_window.addWidget(icon_date)
        self.layout_date_in_clock_window.addWidget(label_date_in_clock_window)
        self.layout_date_in_clock_window.addStretch()

        self.layout_clock_window.addWidget(self.widget_date_in_clock_window)

    def setupUI_date_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(520, 470)

        self.widget_date_window = QWidget()
        self.widget_date_window.setObjectName("widget_date_window")

        self.layout_date_window = QVBoxLayout(self.widget_date_window)
        self.layout_date_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(500, 35)
        self.layout_date_window.addWidget(self.widget_title_bar)

        self.add_widget_space_vertical(50, self.layout_date_window)

        s = result["zone_name"] + ", " + "UTC " + result["utc"]
        self.display_time_zone(s)
        self.layout_date_window.addWidget(self.widget_time_zone)

        self.add_widget_space_vertical(30, self.layout_date_window)

        self.display_date(result["day"], result["month"], result["year"])

        self.add_widget_space_vertical(15, self.layout_date_window)

        self.display_clock_in_date_window(
            result["hour"], result["minute"], result["second"]
        )

        self.layout_date_window.addStretch()

        self.widget_bottom_bar.setFixedSize(500, 40)
        self.layout_date_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_date_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_date(self, d, m, y):
        self.widget_date = QWidget()
        self.widget_date.setObjectName("widget_date")

        self.layout_date = QHBoxLayout(self.widget_date)
        self.layout_date.setContentsMargins(0, 0, 0, 0)

        label_day = QLabel(d)
        label_day.setObjectName("label_day")

        label_slash = QLabel("/")
        label_slash.setObjectName("label_slash")

        label_month = QLabel(m)
        label_month.setObjectName("label_month")

        label_slash2 = QLabel("/")
        label_slash2.setObjectName("label_slash2")

        label_year = QLabel(y)
        label_year.setObjectName("label_year")

        self.layout_date.addStretch()
        self.layout_date.addWidget(label_day)
        self.layout_date.addWidget(label_slash)
        self.layout_date.addWidget(label_month)
        self.layout_date.addWidget(label_slash2)
        self.layout_date.addWidget(label_year)
        self.layout_date.addStretch()

        self.layout_date_window.addWidget(self.widget_date)

    def display_clock_in_date_window(self, h, m, s):
        self.widget_clock_in_date_window = QWidget()
        self.widget_clock_in_date_window.setObjectName("widget_clock_in_date_window")

        self.layout_clock_in_date_window = QHBoxLayout(self.widget_clock_in_date_window)
        self.layout_clock_in_date_window.setContentsMargins(0, 0, 0, 0)

        icon_clock = QLabel()
        icon_clock.setObjectName("icon_clock")
        icon_clock.setPixmap(QPixmap("./icon/clock-32px.png"))
        icon_clock.setScaledContents(True)
        icon_clock.setFixedSize(25, 25)

        clock = h + ":" + m + ":" + s

        label_clock_in_date_window = QLabel(clock)
        label_clock_in_date_window.setObjectName("label_clock_in_date_window")

        self.layout_clock_in_date_window.addStretch()
        self.layout_clock_in_date_window.addWidget(icon_clock)
        self.layout_clock_in_date_window.addWidget(label_clock_in_date_window)
        self.layout_clock_in_date_window.addStretch()

        self.layout_date_window.addWidget(self.widget_clock_in_date_window)

    def setupUI_loading_window(self, MainWindow, text):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(520, 470)

        self.widget_loading_window = QWidget()
        self.widget_loading_window.setObjectName("widget_loading_window")

        self.layout_loading_window = QVBoxLayout(self.widget_loading_window)
        self.layout_loading_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(500, 35)
        self.layout_loading_window.addWidget(self.widget_title_bar)

        self.display_loading_animated()

        self.display_assistant_loading(text)

        self.layout_loading_window.addStretch()

        self.widget_bottom_bar.setFixedSize(500, 40)
        self.layout_loading_window.addWidget(self.widget_bottom_bar)

        MainWindow.layout_container.addWidget(self.widget_loading_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_loading_animated(self):
        self.widget_loading_animated = QWidget()
        self.widget_loading_animated.setObjectName("widget_loading_animated")

        self.layout_loading_animated = QHBoxLayout(self.widget_loading_animated)
        self.layout_loading_animated.setContentsMargins(0, 0, 0, 0)

        url_loading_gif = "./icon/Spin-1s-170px.gif"
        loading_gif = QMovie(url_loading_gif)
        loading_gif.start()

        label_loading_animated = QLabel()
        label_loading_animated.setMovie(loading_gif)
        label_loading_animated.setScaledContents(True)
        label_loading_animated.setFixedSize(170, 170)

        self.layout_loading_animated.addWidget(label_loading_animated)

        self.layout_loading_window.addWidget(self.widget_loading_animated)

    def display_assistant_loading(self, text):
        self.widget_assistant_loading = QWidget()
        self.widget_assistant_loading.setObjectName("widget_assistant_loading")

        self.layout_assistant_loading = QHBoxLayout(self.widget_assistant_loading)
        self.layout_assistant_loading.setContentsMargins(0, 0, 0, 0)

        label_assistant_loading = QLabel(text)
        label_assistant_loading.setObjectName("label_assistant_loading")

        self.layout_assistant_loading.addStretch()
        self.layout_assistant_loading.addWidget(label_assistant_loading)
        self.layout_assistant_loading.addStretch()

        self.layout_loading_window.addWidget(self.widget_assistant_loading)

    def setupUI_weather_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(570, 470)

        self.widget_weather_window = QWidget()
        self.widget_weather_window.setObjectName("widget_weather_window")

        self.layout_weather_window = QVBoxLayout(self.widget_weather_window)
        self.layout_weather_window.setContentsMargins(0, 0, 0, 0)

        self.widget_title_bar.setFixedSize(550, 35)
        self.layout_weather_window.addWidget(self.widget_title_bar)

        self.display_city_name(result["city"])

        self.add_widget_space_vertical(15, self.layout_weather_window)

        self.display_icon_weather_and_temp(result["icon"], result["temp"])

        self.add_widget_space_vertical(15, self.layout_weather_window)

        self.display_weather_description(result["feel_like"], result["desc"])

        self.add_widget_space_vertical(10, self.layout_weather_window)

        self.display_weather_details(result)

        self.layout_weather_window.addStretch()

        self.widget_bottom_bar.setFixedSize(550, 40)
        self.layout_weather_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_weather_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_city_name(self, text):
        self.widget_city_name = QWidget()
        self.widget_city_name.setObjectName("widget_city_name")

        self.layout_city_name = QHBoxLayout(self.widget_city_name)
        self.layout_city_name.setContentsMargins(0, 0, 0, 0)

        icon_location_city_name = QLabel()
        icon_location_city_name.setObjectName("icon_location_city_name")
        icon_location_city_name.setFixedSize(23, 23)
        icon_location_city_name.setScaledContents(True)
        icon_location_city_name.setPixmap(QPixmap("./icon/placeholder-32px.png"))

        s = "<b>" + text + "</b>"
        label_city_name = QLabel(s)
        label_city_name.setObjectName("label_city_name")

        self.add_widget_space_horizontal(30, self.layout_city_name)
        self.layout_city_name.addWidget(icon_location_city_name)
        self.layout_city_name.addWidget(label_city_name)
        self.layout_city_name.addStretch()

        self.layout_weather_window.addWidget(self.widget_city_name)

    def display_icon_weather_and_temp(self, icon, temp):
        self.widget_weather_and_temp = QWidget()
        self.widget_weather_and_temp.setObjectName("widget_weather_and_temp")

        self.layout_weather_and_temp = QHBoxLayout(self.widget_weather_and_temp)
        self.layout_weather_and_temp.setContentsMargins(0, 0, 0, 0)

        self.layout_weather_and_temp.addStretch()

        no_icon_weather = icon
        label_icon_weather = QLabel()
        s = "./icon/weather/{}.png".format(no_icon_weather)
        label_icon_weather.setPixmap(QPixmap(s))
        label_icon_weather.setScaledContents(True)
        label_icon_weather.setFixedSize(130, 130)
        self.layout_weather_and_temp.addWidget(label_icon_weather)

        self.add_widget_space_horizontal(70, self.layout_weather_and_temp)

        s = "{}<sup>o</sup>C".format(temp)
        label_temp = QLabel()
        label_temp.setObjectName("label_temp")
        label_temp.setTextFormat(Qt.RichText)
        label_temp.setText(s)
        # label_temp.setAlignment(Qt.AlignCenter)
        self.layout_weather_and_temp.addWidget(label_temp)

        self.layout_weather_and_temp.addStretch()
        self.layout_weather_window.addWidget(self.widget_weather_and_temp)

    def display_weather_description(self, temp, desc):
        self.widget_weather_description = QWidget()

        self.layout_weather_description = QHBoxLayout(self.widget_weather_description)
        self.layout_weather_description.setContentsMargins(0, 0, 0, 0)

        s = "<b>Cảm giác như {}<sup>o</sup>C. {}.</b>".format(
            round(temp), desc.capitalize()
        )

        label_desc = QLabel()
        label_desc.setObjectName("label_desc")
        label_desc.setTextFormat(Qt.RichText)
        label_desc.setText(s)

        self.layout_weather_description.addStretch()
        self.layout_weather_description.addWidget(label_desc)
        self.layout_weather_description.addStretch()

        self.layout_weather_window.addWidget(self.widget_weather_description)

    def display_weather_details(self, result):
        self.widget_weather_details = QWidget()
        self.layout_weather_details = QHBoxLayout(self.widget_weather_details)
        self.layout_weather_details.setContentsMargins(0, 0, 0, 0)

        self.widget_weather_details_child = QWidget()
        self.layout_weather_details_child = QGridLayout(
            self.widget_weather_details_child
        )
        self.layout_weather_details_child.setContentsMargins(0, 0, 0, 0)

        s = "Áp suất: {}hPa".format(result["pressure"])
        label_pressure = QLabel()
        label_pressure.setObjectName("label_pressure")
        label_pressure.setText(s)
        self.layout_weather_details_child.addWidget(label_pressure, 0, 0)

        s = "Độ ẩm: {}%".format(result["humidity"])
        label_humidity = QLabel()
        label_humidity.setObjectName("label_humidity")
        label_humidity.setText(s)
        self.layout_weather_details_child.addWidget(label_humidity, 0, 2)

        s = "Có mây: {}%".format(result["cloud"])
        label_cloud = QLabel()
        label_cloud.setObjectName("label_cloud")
        label_cloud.setText(s)
        self.layout_weather_details_child.addWidget(label_cloud, 1, 0)

        s = "Tốc độ gió: {}m/s".format(result["wind_speed"])
        label_wind = QLabel()
        label_wind.setObjectName("label_wind")
        label_wind.setText(s)
        self.layout_weather_details_child.addWidget(label_wind, 1, 2)

        s = "Chỉ số UV: {}".format(result["uvi"])
        label_uvi = QLabel()
        label_uvi.setObjectName("label_uvi")
        label_uvi.setText(s)
        self.layout_weather_details_child.addWidget(label_uvi, 2, 0)

        v = int(result["visibility"]) / 1000
        s = "Tầm nhìn xa: {}km".format(v)
        label_visible = QLabel()
        label_visible.setObjectName("label_visible")
        label_visible.setText(s)
        self.layout_weather_details_child.addWidget(label_visible, 2, 2)

        for i in range(3):
            widget_middle = QWidget()
            widget_middle.setFixedWidth(50)
            self.layout_weather_details_child.addWidget(widget_middle, i, 1)

        self.layout_weather_details.addStretch()
        self.layout_weather_details.addWidget(self.widget_weather_details_child)
        self.layout_weather_details.addStretch()

        self.layout_weather_window.addWidget(self.widget_weather_details)

    def setupUI_news_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(720, 820)

        self.widget_news_window = QWidget()
        self.widget_news_window.setObjectName("widget_news_window")

        self.layout_news_window = QVBoxLayout(self.widget_news_window)
        self.layout_news_window.setContentsMargins(0, 0, 0, 0)
        self.layout_news_window.setSpacing(0)

        self.widget_title_bar.setFixedSize(700, 35)
        self.layout_news_window.addWidget(self.widget_title_bar)

        # title_news = QLabel("<b>Tin Tức VNExpress</b>")
        # title_news.setObjectName("title_news")
        # title_news.setTextFormat(Qt.RichText)
        # self.layout_news_window.addWidget(title_news)

        self.display_topic_buttons()

        self.display_topic_content()
        self.update_topic_content(MainWindow, result)

        self.widget_bottom_bar.setFixedSize(700, 40)
        self.layout_news_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_news_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_topic_buttons(self):
        self.widget_topic_buttons = QWidget()
        self.widget_topic_buttons.setObjectName("widget_topic_buttons")

        self.layout_topic_buttons = QHBoxLayout(self.widget_topic_buttons)
        self.layout_topic_buttons.setContentsMargins(10, 0, 10, 10)

        self.layout_topic_buttons.addWidget(self.topic_button_1)
        self.layout_topic_buttons.addWidget(self.topic_button_2)
        self.layout_topic_buttons.addWidget(self.topic_button_3)
        self.layout_topic_buttons.addWidget(self.topic_button_4)
        self.layout_topic_buttons.addWidget(self.topic_button_5)
        self.layout_topic_buttons.addStretch()

        self.layout_news_window.addWidget(self.widget_topic_buttons)

    def update_topic_buttons(self, opt):
        if opt == 1:
            self.topic_button_1.setDisabled(True)
            self.topic_button_2.setEnabled(True)
            self.topic_button_3.setEnabled(True)
            self.topic_button_4.setEnabled(True)
            self.topic_button_5.setEnabled(True)
        elif opt == 2:
            self.topic_button_2.setDisabled(True)
            self.topic_button_1.setEnabled(True)
            self.topic_button_3.setEnabled(True)
            self.topic_button_4.setEnabled(True)
            self.topic_button_5.setEnabled(True)
        elif opt == 3:
            self.topic_button_3.setDisabled(True)
            self.topic_button_1.setEnabled(True)
            self.topic_button_2.setEnabled(True)
            self.topic_button_4.setEnabled(True)
            self.topic_button_5.setEnabled(True)
        elif opt == 4:
            self.topic_button_4.setDisabled(True)
            self.topic_button_1.setEnabled(True)
            self.topic_button_2.setEnabled(True)
            self.topic_button_3.setEnabled(True)
            self.topic_button_5.setEnabled(True)
        elif opt == 5:
            self.topic_button_5.setDisabled(True)
            self.topic_button_1.setEnabled(True)
            self.topic_button_2.setEnabled(True)
            self.topic_button_3.setEnabled(True)
            self.topic_button_4.setEnabled(True)

    def display_topic_content(self):
        self.widget_topic_content = QWidget()
        self.widget_topic_content.setObjectName("widget_topic_content")

        self.layout_topic_content = QVBoxLayout(self.widget_topic_content)
        self.layout_topic_content.setContentsMargins(0, 0, 0, 0)

        self.layout_news_window.addWidget(self.widget_topic_content)

    def update_topic_content(self, MainWindow, result):
        self.clear_layout(self.layout_topic_content)

        self.scroll_area_news = QScrollArea(self.widget_topic_content)
        self.scroll_area_news.setObjectName("scroll_area_news")

        self.scroll_area_news_content = QWidget()
        self.scroll_area_news_content.setObjectName("scroll_area_news_content")

        self.layout_scroll_area_news_content = QVBoxLayout(
            self.scroll_area_news_content
        )
        self.layout_scroll_area_news_content.setContentsMargins(10, 10, 10, 10)
        self.layout_scroll_area_news_content.setSpacing(10)

        for i in range(10):
            self.display_news_widget(MainWindow, result[str(i)])

        button_see_more_news = QPushButton("Xem thêm nhiều tin tức khác cùng chủ đề...")
        button_see_more_news.setObjectName("button_see_more_news")
        button_see_more_news.clicked.connect(
            lambda: self.open_url_from_button(MainWindow, result["see_more"])
        )
        self.layout_scroll_area_news_content.addWidget(button_see_more_news)

        self.scroll_area_news.setWidget(self.scroll_area_news_content)
        self.layout_topic_content.addWidget(self.scroll_area_news)

    def display_news_widget(self, MainWindow, article):
        widget_news = QWidget()
        widget_news.setObjectName("widget_news")
        widget_news.setFixedSize(661, 150)

        layout_news = QHBoxLayout(widget_news)
        layout_news.setContentsMargins(0, 0, 0, 0)

        cover_image = QLabel()
        cover_image.setObjectName("cover_image")
        cover_image.setPixmap(QPixmap(article["cover_img"]))
        cover_image.setScaledContents(True)
        cover_image.setFixedSize(210, 150)

        widget_details = QWidget()
        layout_details = QVBoxLayout(widget_details)
        layout_details.setContentsMargins(5, 5, 5, 5)

        s = "<b>" + article["title"] + "</b>"
        label_title_news = QLabel(s)
        label_title_news.setObjectName("label_title_news")
        label_title_news.setTextFormat(Qt.RichText)
        label_title_news.setWordWrap(True)

        label_desc_news = QLabel(article["desc"])
        label_desc_news.setObjectName("label_desc_news")
        label_desc_news.setWordWrap(True)

        widget_contain_button = QWidget()
        layout_widget_contain_button = QHBoxLayout(widget_contain_button)
        layout_widget_contain_button.setContentsMargins(0, 0, 0, 0)

        button_read_more = QPushButton("Đọc tiếp...")
        button_read_more.setObjectName("button_read_more")
        button_read_more.setFixedSize(85, 27)
        button_read_more.clicked.connect(
            lambda: self.open_url_from_button(MainWindow, article["link"])
        )

        layout_widget_contain_button.addStretch()
        layout_widget_contain_button.addWidget(button_read_more)

        layout_details.addWidget(label_title_news)
        layout_details.addWidget(label_desc_news)
        layout_details.addStretch()
        layout_details.addWidget(widget_contain_button)

        layout_news.addWidget(cover_image)
        layout_news.addWidget(widget_details)

        self.layout_scroll_area_news_content.addWidget(widget_news)

    def open_url_from_button(self, MainWindow, url):
        MainWindow.close()
        webbrowser.open(url)

    def setupUI_wikipedia_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(620, 520)

        self.widget_wiki_window = QWidget()
        self.widget_wiki_window.setObjectName("widget_wiki_window")

        self.layout_wiki_window = QVBoxLayout(self.widget_wiki_window)
        self.layout_wiki_window.setContentsMargins(0, 0, 0, 0)
        self.layout_wiki_window.setSpacing(0)

        self.widget_title_bar.setFixedSize(600, 35)
        self.layout_wiki_window.addWidget(self.widget_title_bar)

        self.display_logo_wiki_and_title(result["keyword"])

        self.display_meaning_of_keyword(result["meaning"])

        self.widget_bottom_bar.setFixedSize(600, 40)
        self.layout_wiki_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_wiki_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_logo_wiki_and_title(self, keyword):
        self.widget_logo_wiki_and_title = QWidget()
        self.widget_logo_wiki_and_title.setObjectName("widget_logo_wiki_and_title")

        self.layout_logo_wiki_and_title = QHBoxLayout(self.widget_logo_wiki_and_title)
        self.layout_logo_wiki_and_title.setContentsMargins(0, 10, 0, 0)

        logo_wiki = QLabel()
        logo_wiki.setPixmap(QPixmap("./icon/wikipedia-logo-128px.png"))
        logo_wiki.setScaledContents(True)
        logo_wiki.setFixedSize(100, 100)

        widgget_title_and_keyword = QWidget()
        layout_title_and_keyword = QVBoxLayout(widgget_title_and_keyword)
        layout_title_and_keyword.setContentsMargins(0, 0, 0, 0)

        title_wiki = QLabel("<b>Wikipedia</b>")
        title_wiki.setObjectName("title_wiki")
        title_wiki.setTextFormat(Qt.RichText)

        s = "<b>" + keyword + "</b>"
        label_keyword = QLabel(s)
        label_keyword.setObjectName("label_keyword")
        label_keyword.setTextFormat(Qt.RichText)

        layout_title_and_keyword.addWidget(title_wiki)
        layout_title_and_keyword.addWidget(label_keyword)

        self.add_widget_space_horizontal(35, self.layout_logo_wiki_and_title)
        self.layout_logo_wiki_and_title.addWidget(logo_wiki)
        self.add_widget_space_horizontal(15, self.layout_logo_wiki_and_title)
        self.layout_logo_wiki_and_title.addWidget(widgget_title_and_keyword)
        self.layout_logo_wiki_and_title.addStretch()

        self.layout_wiki_window.addWidget(self.widget_logo_wiki_and_title)

    def display_meaning_of_keyword(self, meaning):
        self.widget_meaning_of_keyword = QWidget()
        self.widget_meaning_of_keyword.setObjectName("widget_meaning_of_keyword")

        self.layout_meaning_of_keyword = QVBoxLayout(self.widget_meaning_of_keyword)
        self.layout_meaning_of_keyword.setContentsMargins(10, 15, 0, 0)

        meaning_of_keyword = QPlainTextEdit(meaning)
        meaning_of_keyword.setObjectName("meaning_of_keyword")
        meaning_of_keyword.setReadOnly(True)

        self.layout_meaning_of_keyword.addWidget(meaning_of_keyword)
        self.layout_wiki_window.addWidget(self.widget_meaning_of_keyword)

    def setupUI_search_default_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.setFixedSize(670, 620)

        self.widget_search_default_window = QWidget()
        self.widget_search_default_window.setObjectName("widget_search_default_window")

        self.layout_search_default_window = QVBoxLayout(
            self.widget_search_default_window
        )
        self.layout_search_default_window.setContentsMargins(0, 0, 0, 0)
        self.layout_search_default_window.setSpacing(0)

        self.widget_title_bar.setFixedSize(650, 35)
        self.layout_search_default_window.addWidget(self.widget_title_bar)

        self.display_title_search_default(result)

        self.display_result_content(MainWindow, result)

        self.widget_bottom_bar.setFixedSize(650, 40)
        self.layout_search_default_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(1)

        MainWindow.layout_container.addWidget(self.widget_search_default_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def display_title_search_default(self, result):
        self.widget_title_search_default = QWidget()
        self.widget_title_search_default.setObjectName("widget_title_search_default")
        self.widget_title_search_default.setFixedHeight(110)

        self.layout_title_search_default = QHBoxLayout(self.widget_title_search_default)
        self.layout_title_search_default.setContentsMargins(0, 0, 0, 10)
        self.layout_title_search_default.setSpacing(0)

        logo_google = QLabel()
        logo_google.setPixmap(QPixmap("./icon/search-gg-128px.png"))
        logo_google.setScaledContents(True)
        logo_google.setFixedSize(90, 90)

        widget_search_box_and_about = QWidget()
        layout_search_box_and_about = QVBoxLayout(widget_search_box_and_about)
        layout_search_box_and_about.setContentsMargins(0, 0, 0, 0)
        layout_search_box_and_about.setSpacing(0)

        widget_search_box = QWidget()
        layout_search_box = QHBoxLayout(widget_search_box)
        layout_search_box.setContentsMargins(0, 0, 0, 0)
        layout_search_box.setSpacing(0)

        search_box = QLineEdit(result["text"])
        search_box.setObjectName("search_box")
        search_box.setReadOnly(True)
        search_box.setFixedWidth(350)
        search_box.setFixedHeight(35)

        icon_search_magnifying = QPushButton()
        icon_search_magnifying.setObjectName("icon_search_magnifying")
        icon_search_magnifying.setIcon(
            QIcon("./icon/searching-magnifying-glass-32px.png")
        )
        icon_search_magnifying.setFixedSize(35, 35)

        layout_search_box.addWidget(search_box)
        layout_search_box.addWidget(icon_search_magnifying)
        layout_search_box.addStretch()

        label_about_of_result = QLabel(result["about"])
        label_about_of_result.setObjectName("label_about_of_result")

        self.add_widget_space_vertical(13, layout_search_box_and_about)
        layout_search_box_and_about.addWidget(widget_search_box)
        self.add_widget_space_vertical(2, layout_search_box_and_about)
        layout_search_box_and_about.addWidget(label_about_of_result)

        self.add_widget_space_horizontal(40, self.layout_title_search_default)
        self.layout_title_search_default.addWidget(logo_google)
        self.add_widget_space_horizontal(20, self.layout_title_search_default)
        self.layout_title_search_default.addWidget(widget_search_box_and_about)

        self.layout_search_default_window.addWidget(self.widget_title_search_default)

    def display_result_content(self, MainWindow, result):
        self.scroll_area_result = QScrollArea()
        self.scroll_area_result.setObjectName("scroll_area_result")

        self.scroll_area_result_content = QWidget()
        self.scroll_area_result_content.setObjectName("scroll_area_result_content")

        self.layout_scroll_area_result_content = QVBoxLayout(
            self.scroll_area_result_content
        )
        self.layout_scroll_area_result_content.setContentsMargins(10, 10, 10, 10)
        self.layout_scroll_area_result_content.setSpacing(10)

        self.widget_result_container = QWidget()
        self.widget_result_container.setObjectName("widget_result_container")
        self.widget_result_container.setFixedWidth(611)

        self.layout_result_container = QVBoxLayout(self.widget_result_container)
        self.layout_result_container.setContentsMargins(10, 10, 10, 10)
        self.layout_result_container.setSpacing(25)

        for i in range(10):
            self.display_result_widget(MainWindow, result[str(i)])

        button_see_more_result = QPushButton("Xem thêm các kết quả khác...")
        button_see_more_result.setObjectName("button_see_more_result")
        button_see_more_result.clicked.connect(
            lambda: self.open_url_from_button(MainWindow, result["see_more"])
        )

        self.layout_result_container.addWidget(button_see_more_result)

        self.layout_scroll_area_result_content.addWidget(self.widget_result_container)

        self.scroll_area_result.setWidget(self.scroll_area_result_content)

        self.layout_search_default_window.addWidget(self.scroll_area_result)

    def display_result_widget(self, MainWindow, result):
        widget_result = QWidget()
        layout_result = QVBoxLayout(widget_result)
        layout_result.setContentsMargins(0, 0, 0, 0)
        layout_result.setSpacing(5)

        label_link_result = QLabel(result["formatted_url"])
        label_link_result.setObjectName("label_link_result")

        button_title_result = QPushButton(result["title"])
        button_title_result.setObjectName("button_title_result")
        button_title_result.clicked.connect(
            lambda: self.open_url_from_button(MainWindow, result["link"])
        )

        widget_snippet = QWidget()
        layout_snippet = QVBoxLayout(widget_snippet)
        layout_snippet.setContentsMargins(0, 0, 0, 0)

        label_snippet_result = QLabel(result["snippet"])
        label_snippet_result.setObjectName("label_snippet_result")
        label_snippet_result.setWordWrap(True)
        label_snippet_result.adjustSize()

        widget_snippet.setFixedHeight(label_snippet_result.height())
        layout_snippet.addWidget(label_snippet_result)
        layout_snippet.addStretch()

        layout_result.addWidget(label_link_result)
        layout_result.addWidget(button_title_result)
        layout_result.addWidget(widget_snippet)
        layout_result.addStretch()

        self.layout_result_container.addWidget(widget_result)

    def setupUI_trans_window(self, MainWindow, result):
        self.clear_UI(MainWindow)
        MainWindow.widget_container.adjustSize()

        self.widget_trans_window = QWidget()
        self.widget_trans_window.setObjectName("widget_trans_window")

        self.layout_trans_window = QHBoxLayout(self.widget_trans_window)
        self.layout_trans_window.setContentsMargins(10, 10, 10, 10)

        if result["error"]:
            self.label_text_dest = QLabel(result["text"])
            self.label_text_dest.setObjectName("label_text_dest")
            self.label_text_dest.setWordWrap(True)
            self.label_text_dest.adjustSize()

            self.layout_trans_window.addStretch()
            self.layout_trans_window.addWidget(self.label_text_dest)
            self.layout_trans_window.addStretch()
        else:
            if len(result["src"]) < 15:
                self.widget_contain_0 = QWidget()
                self.layout_contain_0 = QVBoxLayout(self.widget_contain_0)
                self.layout_contain_0.setContentsMargins(0, 0, 0, 0)

                self.label_detect_lang = QLabel(result["detect"])
                self.label_detect_lang.setObjectName("label_detect_lang")

                self.widget_contain_1 = QWidget()
                self.layout_contain_1 = QVBoxLayout(self.widget_contain_1)
                self.layout_contain_1.setContentsMargins(0, 0, 0, 0)

                self.label_text_src = QLabel(result["src"])
                self.label_text_src.setObjectName("label_text_src")

                self.layout_contain_1.addWidget(self.label_text_src)
                self.widget_contain_1.adjustSize()

                self.label_trans_to_vi = QLabel("Vietnamese")
                self.label_trans_to_vi.setObjectName("label_trans_to_vi")

                self.widget_contain_2 = QWidget()
                self.layout_contain_2 = QVBoxLayout(self.widget_contain_2)
                self.layout_contain_2.setContentsMargins(0, 0, 0, 0)

                self.label_text_dest = QLabel(result["dest"])
                self.label_text_dest.setObjectName("label_text_dest")

                self.layout_contain_2.addWidget(self.label_text_dest)
                self.widget_contain_1.adjustSize()

                self.layout_contain_0.addWidget(self.label_detect_lang)
                self.layout_contain_0.addWidget(self.widget_contain_1)
                self.layout_contain_0.addWidget(self.label_trans_to_vi)
                self.layout_contain_0.addWidget(self.widget_contain_2)

                self.layout_trans_window.addWidget(self.widget_contain_0)

            else:
                self.label_text_dest = QLabel(result["dest"])
                self.label_text_dest.setObjectName("label_text_dest")
                self.label_text_dest.setWordWrap(True)

                self.layout_trans_window.addStretch()
                self.layout_trans_window.addWidget(self.label_text_dest)
                self.layout_trans_window.addStretch()

        MainWindow.layout_container.addWidget(self.widget_trans_window)
        MainWindow.show()
        MainWindow.set_location_window(result)


# if __name__ == "__main__":
# app = QApplication(sys.argv)
# MainWindow = TransForm()
# ui = UI_TransForm()
# ui.setupUI_trans_window(MainWindow)
# sys.exit(app.exec_())
