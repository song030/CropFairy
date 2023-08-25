import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

# from Source.Client.ClientLogin import ClientLogin

app = QApplication(sys.argv)

# 글꼴 설정
fontDB = QFontDatabase()
fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
fontDB.addApplicationFont("../../FONT/NanumSquareRoundR.ttf")

# login = ClientLogin()
# login.show()
# app.exec()
