import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)

        icon = QIcon(
            "./icon/fugue-icons-3.5.6/icons/application-plus-black.png")
        self.setIcon(icon)
        self.setVisible(True)

        menu = QMenu(parent)

        about_action = menu.addAction("About")

        settings_action = menu.addAction("Settings")

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        self.setContextMenu(menu)
        self.setToolTip("Virtual Assistant\n\nVersion 1.0.0")

    def exit_app(self):
        QCoreApplication.exit()
