import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

from Source.Views.CropFairy import CropFairy
from Source.Views.Font import Font

app = QApplication(sys.argv)

# 글꼴 설정
fontDB = QFontDatabase()
fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundR.ttf")
fontDB.addApplicationFont("../../FONT/ONE Mobile POP.ttf")
app.setFont(Font.text(4))

crop_fairy = CropFairy()
crop_fairy.show()
app.exec()
