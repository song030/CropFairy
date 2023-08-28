import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from Source.Views.CropFairy import CropFairy

app = QApplication(sys.argv)

# 글꼴 설정
fontDB = QFontDatabase()
fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundR.ttf")
fontDB.addApplicationFont("../../FONT/ONE Mobile POP.ttf")

crop_fairy = CropFairy()
crop_fairy.show()
app.exec()
