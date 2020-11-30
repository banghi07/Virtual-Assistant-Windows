import sys
from PyQt5 import QtWidgets
from trans_window import Ui_Form, TransForm
from PyQt5.QtCore import QEvent, QPoint, Qt


class Trans:
    def __init__(self, result):
        # app = QtWidgets.QApplication(sys.argv)
        self.Form = TransForm()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        self.set_form(result)

        self.Form.show()
        # sys.exit(app.exec_())

    def set_form(self, result):
        window_pos = QPoint()
        window_pos.setX(result["cursor_pos"].x() + 10)
        window_pos.setY(result["cursor_pos"].y() + 25)
        self.Form.move(window_pos)

        self.ui.plainTextEdit.setPlainText(result["text"])


if __name__ == "__main__":
    Trans()