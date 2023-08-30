from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogJoin import Ui_DlgJoin
from Source.Views.DialogWarning import DialogWarning

class DialogJoin(QDialog, Ui_DlgJoin):
    def __init__(self, cropfairy):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 1024, 860)
        self.back.setStyleSheet("background-color: rgba(20, 20, 20, 50);")
        self.back.hide()

        self.dialog = DialogWarning()

        self.connect_event()
        self.cropfairy = cropfairy

    # 아니오, 닫기 눌렀을 때
    def reject(self) -> None:
        self.setResult(0)
        self.close()

    def closeEvent(self, a0):
        pass

    # 이벤트 연결
    def connect_event(self):
        self.dialog.showEvent = lambda e: self.back.show()
        self.dialog.closeEvent = lambda e: self.back.hide()

        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_join.clicked.connect(self.join)
        self.btn_close.clicked.connect(self.reject)
        self.btn_check.clicked.connect(self.btn_check_click)

    # 회원가입 눌렀을 때
    def join(self):
        check = self.cropfairy.use_email_check

        # 비밀번호 입력 확인
        pw_check = self.check_pw()

        edt_email = self.edt_email.text()
        # 아이디 패스워드 사용가능
        if check and pw_check:
            edt_pw = self.edt_pwd_1.text()

            send_data = ["sign_up", edt_email, edt_pw]
            self.cropfairy.send_data(send_data)
            self.dialog.set_dialog_type("join_success")
            self.dialog.exec()
            self.setResult(1)
            self.close()
        else:
            if not check:
                if edt_email == "":
                    self.dialog.set_dialog_type("email_input")
                else:
                    self.dialog.set_dialog_type("email_check_not")
                self.dialog.exec()

        # result = False
        # if result:
        #     self.setResult(1)
        #     self.close()

    # 패스워드 확인 함수
    def check_pw(self):
        edt_pw = self.edt_pwd_1.text()
        edt_pw2 = self.edt_pwd_2.text()

        if edt_pw == edt_pw2 and len(edt_pw) >= 8:
            return True
        elif edt_pw != edt_pw2:
            self.dialog.set_dialog_type("join_pwd_same")
            self.dialog.exec()
            return False
        elif len(edt_pw) <= 0:
            self.dialog.set_dialog_type("pwd_input")
            self.dialog.exec()
            return False
        elif len(edt_pw) < 8:
            self.dialog.set_dialog_type("join_pwd_input_len")
            self.dialog.exec()
            return False

    # 이메일 중복확인 버튼
    def btn_check_click(self):
        edt_email = self.edt_email.text()
        if edt_email == "":
            self.dialog.set_dialog_type("email_input")
            self.dialog.exec()
        elif "@" not in edt_email or "." not in edt_email:
            self.dialog.set_dialog_type("email_wrong")
            self.dialog.exec()
        else:
            senddata = ["idrd_check", edt_email]
            print(senddata)

            self.cropfairy.send_data(senddata)
