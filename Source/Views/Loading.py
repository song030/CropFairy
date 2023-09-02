from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QByteArray, Qt

from Source.Views.UI_DialogLoading import Ui_DlgLoading

class Loading(QWidget, Ui_DlgLoading):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.movie = QMovie("../../Image/loading.gif", QByteArray(), self)
        self.lbl_loading.setMovie(self.movie)
        self.movie.start()

