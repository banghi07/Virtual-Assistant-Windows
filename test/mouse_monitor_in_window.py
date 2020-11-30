import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


# class MouseTracker(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.setMouseTracking(True)

#     def initUI(self):
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle("Mouse Tracker")
#         self.label = QLabel(self)
#         self.label.resize(200, 40)
#         self.show()

#     def mouseMoveEvent(self, event):
#         self.label.setText("Mouse coords: ( %d : %d )" % (event.x(), event.y()))
#         if event.x() < 0:
#             self.close()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = MouseTracker()
#     sys.exit(app.exec_())


class mainwindow(QWidget):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)

    def enterEvent(self, event):
        print("Mouse Entered")
        # return super(mainwindow, self).enterEvent(event)

    def leaveEvent(self, event):
        print("Mouse Left")
        # return super(mainwindow, self).enterEvent(event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main = mainwindow()
    main.show()
    sys.exit(app.exec_())