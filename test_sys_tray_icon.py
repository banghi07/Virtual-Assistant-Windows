import sys
from PyQt5 import QtWidgets
from PyQt5.Qt import QAction, QIcon, QMenu, QSystemTrayIcon
from mainwindow import Ui_MainWindow


class test():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        icon = QIcon(
            "./icon/fugue-icons-3.5.6/icons/application-plus-black.png")
        tray = QSystemTrayIcon()
        tray.setVisible(True)
        tray.setIcon(icon)

        menu = QMenu()
        action1 = QAction("About")
        # action1.triggered.connect()
        menu.addAction(action1)

        action2 = QAction("Settings")
        # action2.triggered.connect()
        menu.addAction(action2)

        aquit = QAction("Exit")
        aquit.triggered.connect(app.quit)
        menu.addAction(aquit)

        tray.setContextMenu(menu)
        tray.activated.connect(self.activate)

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        sys.exit(app.exec_())

    def activate(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.MainWindow.show()


if __name__ == "__main__":
    test()
