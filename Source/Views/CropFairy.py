from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLayout, QComboBox, QCompleter, QPlainTextEdit, QListView, QCheckBox, QDateEdit
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QSize, Qt, QDate

# from Source.Views.UI_TeacherManage import Ui_TeacherManage


class TeacherManage(QDialog, Ui_TeacherManage):

    def __init__(self):
        super().__init__()
        self.setupUi(self)