import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from mainwindow import Ui_MainWindow
from PyQt5.Qt import QMainWindow


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)

        icon = QIcon(
            "./icon/fugue-icons-3.5.6/icons/application-plus-black.png")
        self.setIcon(icon)
        self.setVisible(True)

        menu = QMenu(parent)

        aboutaction = QAction("About", parent)
        # action1.triggered.connect()
        menu.addAction(aboutaction)

        settingsaction = QAction("Settings", parent)
        # action1.triggered.connect()
        menu.addAction(settingsaction)

        exitaction = QAction("Exit", parent)
        exitaction.triggered.connect(self.exit_app)
        menu.addAction(exitaction)

        testAction = menu.addAction("Test")
        testAction.triggered.connect(self.exit_app)

        self.setContextMenu(menu)
        self.setToolTip("Virtual Assistant\n\nVersion 1.0.0")
        # self.show()

    def exit_app(self):
        QCoreApplication.exit()


class test():
    def __init__(self):
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

        w = QWidget()
        tray_icon = SystemTrayIcon(w)
        tray_icon.show()

        # icon = QIcon(
        #     "./icon/fugue-icons-3.5.6/icons/application-plus-black.png")
        # tray = QSystemTrayIcon()
        # tray.setVisible(True)
        # tray.setIcon(icon)

        # menu = QMenu()
        # action1 = QAction("About")
        # # action1.triggered.connect()
        # menu.addAction(action1)

        # action2 = QAction("Settings")
        # # action2.triggered.connect()
        # menu.addAction(action2)

        # aquit = QAction("Exit")
        # aquit.triggered.connect(app.quit)
        # menu.addAction(aquit)

        # tray.setContextMenu(menu)
        # tray.activated.connect(self.activate)

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        sys.exit(app.exec_())

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.MainWindow.show()


if __name__ == "__main__":
    test()
