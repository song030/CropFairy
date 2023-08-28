import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from PyQt5.QtWidgets import QLayout, QComboBox, QCompleter, QPlainTextEdit, QListView, QCheckBox, QDateEdit
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor, QPixmap
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5.Qt import QMainWindow

from Source.Views.UI_CropFairy import Ui_CropFairy

from Source.Views.DialogJoin import DialogJoin
from Source.Views.DialogResult import DialogResult
from Source.Views.DialogWarning import DialogWarning


class CropFairy(QMainWindow, Ui_CropFairy):

    def __init__(self):
        super().__init__()

        # --- 변수 선언
        self.login = False
        self.upload_image = False

        # --- 초기화
        self.set_Ui()
        self.connect_Event()

    # 화면 초기화
    def set_Ui(self):
        self.setupUi(self)
        self.set_Font()

        self.move_page_main()


    # 글꼴 설정
    def set_Font(self):
        pass

    # 이벤트 연결
    def connect_Event(self):
        # 메인화면
        self.btn_login.clicked.connect(self.btn_login_click)
        self.btn_join.clicked.connect(self.btn_join_click)
        self.btn_analyze.clicked.connect(self.btn_analyze_click)
        self.btn_exit.clicked.connect(self.btn_exit_click)
        self.btn_list.clicked.connect(self.btn_list_click)
        self.btn_back.clicked.connect(self.btn_back_click)

        # 진단하기
        self.btn_upload.clicked.connect(self.btn_upload_click)
        self.btn_start.clicked.connect(self.btn_start_click)

        # 내역조회

    # 메인으로 이동시 화면 설정
    def move_page_main(self):
        self.stack_control.setVisible(False)
        self.btn_back.setVisible(False)
        self.btn_list.setEnabled(True)

        if self.login:
            self.widget_login.setVisible(False)
            self.btn_analyze.setVisible(True)
        else:
            self.widget_login.setVisible(True)
            self.btn_analyze.setVisible(False)

        self.stacke_main.setCurrentWidget(self.page_main)

    # 내역조회 화면으로 이동시 화면 설정
    def move_page_list(self):
        self.stack_control.setCurrentWidget(self.control_page)
        self.stack_control.setVisible(True)
        self.btn_back.setVisible(True)
        self.btn_list.setEnabled(False)
        self.stacke_main.setCurrentWidget(self.page_list)

    def btn_list_click(self):
        self.move_page_list()

    def btn_back_click(self):
        self.move_page_main()

    # ----------------------------------------------------- Main -----------------------------------------------------

    # 진단화면으로 이동시 화면 설정
    def move_page_analyze(self):
        self.stack_control.setCurrentWidget(self.control_analyze)
        self.stack_control.setVisible(True)
        self.btn_back.setVisible(True)
        self.btn_start.setVisible(False)
        self.btn_list.setEnabled(True)
        self.lbl_upload_image.setText(" ")
        self.stacke_main.setCurrentWidget(self.page_analyze)

    # 로그인
    def btn_login_click(self):
        # TODO 로그인 예외처리 추가하기!

        self.login = True
        self.move_page_main()

    # 회원가입
    def btn_join_click(self):
        self.dlg_join = DialogJoin()
        self.dlg_join.exec()

    # 진단하기 페이지 이동 버튼
    def btn_analyze_click(self):
        self.move_page_analyze()

    # 종료
    def btn_exit_click(self):
        self.close()

    # --------------------------------------------------------------------------------------------------------------

    # -------------------------------------------------- Analyze --------------------------------------------------

    # 이미지 업로드 버튼
    def btn_upload_click(self):
        fname = QFileDialog.getOpenFileName(self, '', '', '모든 파일(*.*);;사용자 지정 파일(*.jpg *.jpeg *.png *.gif)')
        if fname[0]:
            self.img_path = fname[0]
            self.lbl_upload_image.setPixmap(QPixmap(self.img_path).scaled(QSize(552, 628), Qt.KeepAspectRatio))
            self.btn_start.setVisible(True)

    # 진단 시작 버튼
    def btn_start_click(self):
        # TODO 진단 버튼 시작시 서버로 이미지 발송는 내용 추가하기
        pass

    # --------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
            app = QApplication(sys.argv)

            # 글꼴 설정
            fontDB = QFontDatabase()
            fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
            fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
            fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
            fontDB.addApplicationFont("../../FONT/ONE Mobile POP.ttf")

            crop_fairy = CropFairy()
            crop_fairy.show()
            app.exec()



