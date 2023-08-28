from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogJoin import Ui_DlgJoin

class DialogJoin(QDialog, Ui_DlgJoin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect_event()

    # 아니오, 닫기 눌렀을 때
    def reject(self) -> None:
        self.setResult(0)
        self.close()

    # 회원가입 눌렀을 때
    def join(self):
        # TODO 회원가입 예외처리 추가하기

        result = True
        if result:
            self.setResult(1)
            self.close()

    def closeEvent(self, a0):
        pass

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_join.clicked.connect(self.join)
        self.btn_close.clicked.connect(self.reject)

    # 이메일 중복확인 버튼
    def btn_check_click(self):
        # TODO 중복확인 내용 추가하기
        pass