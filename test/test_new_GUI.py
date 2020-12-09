import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sys_tray_icon import SystemTrayIcon


class TestGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        tray_icon = SystemTrayIcon(self.widget)
        tray_icon.activated.connect(self.activate)

        self.set_window()

        self.show()

    def set_window(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        widget = QWidget()
        self.setFixedSize(500, 400)
        self.setWindowTitle("Virtual Assistant - PyQt5")

        label = QLabel()
        loading_gif_url = "./icon/Spin-1s-200px.gif"
        loading_gif = QMovie(loading_gif_url)
        loading_gif.start()
        label.setMovie(loading_gif)
        label.setScaledContents(True)
        label.setFixedSize(200, 200)

        button = QPushButton("Next")
        button.pressed.connect(self.next_window)

        widget_layout = QGridLayout(widget)
        widget_layout.addWidget(label)
        widget_layout.addWidget(button)
        self.setCentralWidget(widget)

        self.set_center_screen()

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.set_window()
            self.show()

    def next_window(self):
        widget = QWidget()
        self.setFixedSize(500, 400)
        self.setWindowTitle("Virtual Assistant - PyQt5")

        button = QPushButton("OK")
        button.pressed.connect(self.set_window)

        widget_layout = QGridLayout(widget)
        widget_layout.addWidget(button)
        self.setCentralWidget(widget)

        self.set_center_screen()

    def set_center_screen(self):
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = TestGUI()
    sys.exit(app.exec_())