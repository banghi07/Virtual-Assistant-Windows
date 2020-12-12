import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet(open("./themes/light.css").read())

        self.widget_container = QWidget()
        self.widget_container.setObjectName("widget_container")

        self.layout_container = QVBoxLayout(self.widget_container)
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
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())


class UI_Windows(object):
    # * Init button, title & bottom bar
    def __init__(self):
        self.btn_close()
        self.btn_microphone()
        self.title_bar()
        self.bottom_bar()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def clear_UI(self, MainWindow):
        self.clear_layout(MainWindow.layout_container)

    def btn_close(self):
        self.button_close = QPushButton()
        self.button_close.setObjectName("button_close")
        self.button_close.setFixedSize(35, 35)
        self.button_close.setIcon(QIcon("./icon/close-32px.png"))

    def btn_microphone(self):
        self.button_microphone = QPushButton()
        self.button_microphone.setObjectName("button_microphone")
        self.button_microphone.setFixedSize(40, 40)
        # self.button_microphone.setIcon(QIcon("./icon/microphone-black-shape-32px.png"))
        self.button_microphone.setIcon(QIcon("./icon/microphone-32px.png"))

    def title_bar(self):
        self.widget_title_bar = QWidget()
        self.widget_title_bar.setObjectName("widget_title_bar")
        self.widget_title_bar.setFixedSize(500, 35)

        self.layout_title_bar = QHBoxLayout(self.widget_title_bar)
        self.layout_title_bar.setContentsMargins(0, 0, 0, 0)

        self.layout_title_bar.addStretch()
        self.layout_title_bar.addWidget(self.button_close)

    def bottom_bar(self):
        self.widget_bottom_bar = QWidget()
        self.widget_bottom_bar.setObjectName("widget_bottom_bar")
        self.widget_bottom_bar.setFixedSize(500, 40)

        self.layout_bottom_bar = QHBoxLayout(self.widget_bottom_bar)
        self.layout_bottom_bar.setContentsMargins(0, 0, 0, 0)

    def update_bottom_bar(self, *args):
        self.clear_layout(self.layout_bottom_bar)
        if len(args) > 0:
            if "0" in str(list(args)[0]):
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
                self.layout_bottom_bar.addStretch()
                self.layout_bottom_bar.addWidget(self.label_user_answer)

        else:
            self.label_assistant_listening = QLabel("Đang lắng nghe...")
            self.label_assistant_listening.setObjectName("label_assistant_listening")

            self.icon_sound_waves = QPushButton()
            self.icon_sound_waves.setObjectName("icon_sound_waves")
            self.icon_sound_waves.setFixedSize(40, 40)
            self.icon_sound_waves.setIcon(QIcon("./icon/audio-waves-32px.png"))

            self.layout_bottom_bar.addWidget(self.icon_sound_waves)
            self.layout_bottom_bar.addStretch()
            self.layout_bottom_bar.addWidget(self.label_assistant_listening)

    # * UI main window
    def setupUI_main_window(self, MainWindow):
        self.clear_UI(MainWindow)
        self.widget_main_window = QWidget()
        self.widget_main_window.setObjectName("widget_main_window")
        self.widget_main_window.setFixedSize(500, 450)

        self.layout_main_window = QVBoxLayout(self.widget_main_window)
        self.layout_main_window.setContentsMargins(0, 0, 0, 0)

        self.layout_main_window.addWidget(self.widget_title_bar)

        self.listen_animated()

        self.assistant_ask()

        self.assistant_hint()

        self.layout_main_window.addStretch()

        self.layout_main_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar()

        MainWindow.layout_container.addWidget(self.widget_main_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def listen_animated(self):
        self.widget_listen_animated = QWidget()
        self.widget_listen_animated.setObjectName("widget_listen_animated")

        self.layout_listen_animated = QHBoxLayout(self.widget_listen_animated)
        self.layout_listen_animated.setContentsMargins(0, 0, 0, 0)

        url_listen_gif = "./icon/Ripple-0.7s-170px.gif"
        listen_gif = QMovie(url_listen_gif)
        listen_gif.start()

        self.label_listen_animated = QLabel()
        self.label_listen_animated.setMovie(listen_gif)
        self.label_listen_animated.setScaledContents(True)
        self.label_listen_animated.setFixedSize(170, 170)

        self.layout_listen_animated.addWidget(self.label_listen_animated)

        self.layout_main_window.addWidget(self.widget_listen_animated)

    def assistant_ask(self):
        self.widget_assistant_ask = QWidget()
        self.widget_assistant_ask.setObjectName("widget_assistant_ask")

        self.layout_assistant_ask = QHBoxLayout(self.widget_assistant_ask)
        self.layout_assistant_ask.setContentsMargins(0, 0, 0, 0)

        self.label_assistant_ask = QLabel("Bạn có yêu cầu gì không?")
        self.label_assistant_ask.setObjectName("label_assistant_ask")

        self.layout_assistant_ask.addStretch()
        self.layout_assistant_ask.addWidget(self.label_assistant_ask)
        self.layout_assistant_ask.addStretch()

        self.layout_main_window.addWidget(self.widget_assistant_ask)

    def assistant_hint(self):
        self.widget_assistant_hint = QWidget()
        self.widget_assistant_hint.setObjectName("widget_assistant_hint")

        self.layout_assistant_hint = QHBoxLayout(self.widget_assistant_hint)
        self.layout_assistant_hint.setContentsMargins(0, 0, 0, 0)

        self.label_assistant_hint = QLabel('Thử gọi "Trợ giúp"')
        self.label_assistant_hint.setObjectName("label_assistant_hint")

        self.layout_assistant_hint.addStretch()
        self.layout_assistant_hint.addWidget(self.label_assistant_hint)
        self.layout_assistant_hint.addStretch()

        self.layout_main_window.addWidget(self.widget_assistant_hint)

    # * UI simple window
    def setupUI_simple_window(self, MainWindow, url, text):
        self.clear_UI(MainWindow)
        self.widget_simple_window = QWidget()
        self.widget_simple_window.setObjectName("widget_simple_window")
        self.widget_simple_window.setFixedSize(500, 450)

        self.layout_simple_window = QVBoxLayout(self.widget_simple_window)
        self.layout_simple_window.setContentsMargins(0, 0, 0, 0)

        self.layout_simple_window.addWidget(self.widget_title_bar)

        self.icon_assistant_answer(url)
        self.assistant_answer(text)
        self.layout_simple_window.addStretch()

        self.layout_simple_window.addWidget(self.widget_bottom_bar)
        self.update_bottom_bar(0)

        MainWindow.layout_container.addWidget(self.widget_simple_window)
        MainWindow.set_shadow_window()
        MainWindow.show()
        MainWindow.set_center_screen()

    def icon_assistant_answer(self, url):
        self.widget_icon_answer = QWidget()
        self.widget_icon_answer.setObjectName("widget_icon_assistant_answer")

        self.layout_icon_answer = QHBoxLayout(self.widget_icon_answer)
        self.layout_icon_answer.setContentsMargins(0, 0, 0, 0)

        self.label_icon_answer = QLabel()
        self.label_icon_answer.setObjectName("label_icon_assistant_answer")
        self.label_icon_answer.setPixmap(QPixmap(url))
        self.label_icon_answer.setScaledContents(True)
        self.label_icon_answer.setFixedSize(170, 170)

        self.layout_icon_answer.addWidget(self.label_icon_answer)

        self.layout_simple_window.addWidget(self.widget_icon_answer)

    def assistant_answer(self, text):
        self.widget_assistant_answer = QWidget()
        self.widget_assistant_answer.setObjectName("widget_assistant_answer")

        self.layout_assistant_answer = QHBoxLayout(self.widget_assistant_answer)
        self.layout_assistant_answer.setContentsMargins(0, 0, 0, 0)

        self.label_assistant_answer = QLabel(text)
        self.label_assistant_answer.setObjectName("label_assistant_answer")

        self.layout_assistant_answer.addStretch()
        self.layout_assistant_answer.addWidget(self.label_assistant_answer)
        self.layout_assistant_answer.addStretch()

        self.layout_simple_window.addWidget(self.widget_assistant_answer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Window()
    ui = UI_Windows()
    ui.title_bar()
    ui.bottom_bar()
    ui.setupUI_simple_window(MainWindow, "./icon/inability-to-speak.png", "hahahaaaaaa")
    sys.exit(app.exec_())