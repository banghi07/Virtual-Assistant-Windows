import sys
from PyQt5 import QtWidgets
from trans_window import Ui_Form
from PyQt5.QtCore import QEvent, QPoint, Qt
from googletrans import Translator
from google_trans_new import google_translator
from assistant_threads import *


class Trans:
    def __init__(self, result, parent=None):
        # app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        self.result = result
        self.thread_pool = QThreadPool()
        self.set_form()
        self.parent = parent

        self.Form.show()
        # sys.exit(app.exec_())

    def set_form(self):
        # self.exit_flag = False
        window_pos = QPoint()
        window_pos.setX(self.result["cursor_pos"].x() + 10)
        window_pos.setY(self.result["cursor_pos"].y() + 25)
        self.Form.move(window_pos)

        self.trans_thread()

        self.ui.pushButton.pressed.connect(self.trans_again)
        self.ui.pushButton_3.pressed.connect(self.exit_dict)

    def trans_thread(self):
        worker = Thread(self.translate, "translate")
        worker.signals.result.connect(self.translate_complete)
        self.thread_pool.start(worker)
        self.ui.plainTextEdit.setPlainText("Đang dịch, vui lòng đợi...")

    # def translate(self):
    #     translator = Translator()
    #     try:
    #         content = translator.translate(self.result["text"], dest="vi")
    #     except:
    #         return "Lỗi! Hãy thử lại."
    #     else:
    #         return content.text

    def translate(self):
        translator = google_translator()
        try:
            content = translator.translate(self.result["text"], lang_tgt="vi")
        except:
            return "Lỗi! Hãy thử lại."
        else:
            return content

    def translate_complete(self, result):
        self.ui.plainTextEdit.setPlainText(result)

    def exit_dict(self):
        self.parent.exit_dict()
        self.Form.close()

    def trans_again(self):
        self.trans_thread()


if __name__ == "__main__":
    Trans()