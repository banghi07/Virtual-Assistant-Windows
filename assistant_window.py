import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from assistant_sys_tray_icon import *


class UI_Window(QMainWindow):
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

        self.widget_main = QWidget()
        self.widget_main.setObjectName("widget_main")

        self.layout_main = QVBoxLayout(self.widget_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        self.shadow_window()
        self.main_window()

        self.widget_main.setGraphicsEffect(self.shadow)

        self.layout_container.addWidget(self.widget_main)
        self.setCentralWidget(self.widget_container)
        self.show()
        self.center_screen()

    def center_screen(self):
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())

    def shadow_window(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setObjectName("shadow_window")
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor("#666666"))
        self.shadow.setOffset(0.0, 0.0)

    def main_window(self):
        self.widget_main.setFixedSize(500, 450)
        self.title_bar()
        self.listen_animated()
        self.assistant_ask()
        self.assistant_hint()
        self.layout_main.addStretch()
        self.user_answer()

    def title_bar(self):
        self.widget_title_bar = QWidget()
        self.widget_title_bar.setObjectName("widget_title_bar")
        self.widget_title_bar.setFixedSize(500, 35)

        self.layout_title_bar = QHBoxLayout(self.widget_title_bar)
        self.layout_title_bar.setContentsMargins(0, 0, 0, 0)

        self.button_close = QPushButton()
        self.button_close.setObjectName("button_close")
        self.button_close.setFixedSize(32, 32)
        self.button_close.setIcon(QIcon("./icon/close.png"))
        self.button_close.clicked.connect(self.close_window)

        self.layout_title_bar.addStretch()
        self.layout_title_bar.addWidget(self.button_close)

        self.layout_main.addWidget(self.widget_title_bar)

    def listen_animated(self):
        self.widget_listen_animated = QWidget()
        self.widget_listen_animated.setObjectName("widget_listen_animated")

        self.layout_listen_animated = QHBoxLayout(self.widget_listen_animated)
        self.layout_listen_animated.setContentsMargins(0, 0, 0, 0)

        url_listen_gif = "./icon/Ripple-1.4s-200px.gif"
        listen_gif = QMovie(url_listen_gif)
        listen_gif.start()

        self.label_listen_animated = QLabel()
        self.label_listen_animated.setMovie(listen_gif)
        self.label_listen_animated.setScaledContents(True)
        self.label_listen_animated.setFixedSize(200, 200)

        self.layout_listen_animated.addWidget(self.label_listen_animated)

        self.layout_main.addWidget(self.widget_listen_animated)

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

        self.layout_main.addWidget(self.widget_assistant_ask)

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

        self.layout_main.addWidget(self.widget_assistant_hint)

    def user_answer(self, *agrs):
        self.widget_user_answer = QWidget()
        self.widget_user_answer.setObjectName("widget_user_answer")

        self.layout_user_answer = QHBoxLayout(self.widget_user_answer)
        self.layout_user_answer.setContentsMargins(0, 0, 0, 0)

        if len(agrs) > 0:
            pass
        else:
            self.label_user_listening = QLabel("Đang lắng nghe...")
            self.label_user_listening.setObjectName("label_user_listening")

            self.layout_user_answer.addWidget(self.label_user_listening)
            self.layout_user_answer.addStretch()

        self.layout_main.addWidget(self.widget_user_answer)

    def close_window(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = UI_Window()
    sys.exit(app.exec_())