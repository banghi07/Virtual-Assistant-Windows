from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from assistant_threads import *


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, assistant=None):
        super().__init__(parent)

        self.assistant = assistant

        icon = QIcon("./icon/tray_icon/application-plus-black.png")
        self.setIcon(icon)
        self.setVisible(True)

        self.menu = QMenu(parent)

        # about_action = menu.addAction("About")
        # settings_action = menu.addAction("Settings")

        self.translation_action = self.menu.addAction("Chức năng từ điển")
        self.update_translation_action()

        self.exit_action = self.menu.addAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)

        self.setContextMenu(self.menu)
        self.setToolTip("Virtual Assistant\n\nVersion 1.0.0")

    def update_translation_action(self, opt=0):
        if opt:
            self.translation_action.setEnabled(True)
            self.translation_action.setIcon(QIcon("./icon/tray_icon/confirm-16px.png"))
            self.translation_action.triggered.connect(self.exit_trans_thread)
        else:
            self.translation_action.setEnabled(False)
            self.translation_action.setIcon(QIcon())

    def exit_trans_thread(self):
        try:
            self.assistant.trans_thread.kill()
            self.update_translation_action()
        except:
            pass

    def exit_app(self):
        try:
            self.assistant.trans_thread.kill()
        except:
            pass
        QCoreApplication.exit()
