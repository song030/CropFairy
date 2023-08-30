from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import QByteArray, Qt

from Source.Views.UI_DialogLoading import Ui_DlgLoading
# from CLASS.Font import Font

class DialogLoading(QWidget, Ui_DlgLoading):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.center()

        self.movie = QMovie("../../Image/loading.gif", QByteArray(), self)
        self.lbl_loading.setMovie(self.movie)
        self.movie.start()

        # self.lbl_text.setFont(Font().button())

    def center(self):
        size = self.size()
        height = 900
        width = 600

        self.move(int(width/2-size.width()/2), int(height/2 - size.height()/2))
