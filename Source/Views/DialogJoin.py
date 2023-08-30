from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogJoin import Ui_DlgJoin
from Source.Views.DialogWarning import DialogWarning

class DialogJoin(QDialog, Ui_DlgJoin):
    def __init__(self, cropfairy):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect_event()
        self.dialog = DialogWarning()
        self.cropfairy = cropfairy

    # 아니오, 닫기 눌렀을 때
    def reject(self) -> None:
        self.setResult(0)
        self.close()

    # 회원가입 눌렀을 때
    def join(self):
        # TODO 회원가입 예외처리 추가하기
        check = self.cropfairy.use_email_check
        pw_check = self.check_pw()

        # 아이디 패스워드 사용가능
        if check and pw_check:
            edt_email = self.edt_email.text()
            edt_pw = self.edt_pwd_1.text()

            send_data = ["sign_up", edt_email, edt_pw]
            self.cropfairy.send_data(send_data)
            self.dialog.set_dialog_type("join_success")
            self.dialog.exec()
            self.setResult(1)
            self.close()
        else:
            if not check:
                self.dialog.set_dialog_type("id_check_not")
                self.dialog.exec()


        # result = False
        # if result:
        #     self.setResult(1)
        #     self.close()

    # 패스워드 확인 함수
    def check_pw(self):
        edt_pw = self.edt_pwd_1.text()
        edt_pw2 = self.edt_pwd_2.text()

        if edt_pw == edt_pw2 and len(edt_pw) > 8:
            return True
        elif edt_pw != edt_pw2:
            self.dialog.set_dialog_type("join_pwd_same")
            self.dialog.exec()
            return False
        elif len(edt_pw) <= 0:
            self.dialog.set_dialog_type("join_pwd_input")
            self.dialog.exec()
            return False
        elif len(edt_pw) < 8:
            self.dialog.set_dialog_type("join_pwd_input_len")
            self.dialog.exec()
            return False

    def closeEvent(self, a0):
        pass

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_join.clicked.connect(self.join)
        self.btn_close.clicked.connect(self.reject)
        self.btn_check.clicked.connect(self.btn_check_click)

    # 이메일 중복확인 버튼
    def btn_check_click(self):
        # TODO 중복확인 내용 추가하기
        edt_email = self.edt_email.text()
        senddata = ["idrd_check", edt_email]
        print(senddata)

        self.cropfairy.send_data(senddata)
