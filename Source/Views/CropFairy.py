import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLayout, QComboBox, QCompleter, QPlainTextEdit, QListView, QCheckBox, QDateEdit
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5.Qt import QMainWindow

from Source.Views.UI_CropFairy import Ui_CropFairy


class CropFairy(QMainWindow, Ui_CropFairy):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 글꼴 설정
    fontDB = QFontDatabase()
    fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
    fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
    fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
    fontDB.addApplicationFont("../../FONT/NanumSquareRoundR.ttf")

    crop_fairy = CropFairy()
    crop_fairy.show()
    app.exec()