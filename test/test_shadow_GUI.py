import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Container(QWidget):
    def __init__(self, window):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet(open("./themes/dark.css").read())

        layout = QVBoxLayout(self)
        layout.addWidget(window)
        layout.setContentsMargins(10, 10, 10, 10)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(99, 255, 255))
        shadow.setOffset(0.0, 0.0)

        window.setGraphicsEffect(shadow)
        self.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        w = QWidget()
        w.setObjectName("mainwindow")
        w.setFixedSize(500, 400)

        layout = QVBoxLayout(w)
        # layout.addWidget()
        self.setCentralWidget(w)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    c = Container(w)
    sys.exit(app.exec_())
