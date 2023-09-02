from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogWarning import Ui_DlgWarning

class DialogWarning(QDialog, Ui_DlgWarning):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect_event()

    # 아니오, 닫기 눌렀을 때
    def reject(self) -> None:
        self.setResult(0)
        self.close()

    # 예, 확인 눌렀을 때
    def accept(self) -> None:
        self.setResult(1)
        self.close()

    # def closeEvent(self, a0):
    #     pass

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        print("in!!")
        self.btn_single.clicked.connect(self.accept)
        self.btn_yes.clicked.connect(self.accept)
        self.btn_close.clicked.connect(self.reject)
        self.btn_no.clicked.connect(self.reject)

    # 다이얼로그 타입 설정
    # bt_cnt : 버튼 수량
    # t_type : 다이얼로그 타입
    def set_dialog_type(self, t_type="", text="", bt_cnt=1):

        # 버튼 설정
        if bt_cnt == 1:
            self.layout_double.setVisible(False)
            self.btn_single.setVisible(True)
        elif bt_cnt == 2:
            self.layout_double.setVisible(True)
            self.btn_single.setVisible(False)

        # 텍스트 설정
        if t_type == "server_error":
            self.lbl_text.setText("서버에 접속 할 수 없습니다..")
        elif t_type == "login_error":
            self.lbl_text.setText("유효하지않은 아이디/비밀번호 입니다.")
        elif t_type == "login_success":
            self.lbl_text.setText(f"'{text}'님 안녕하세요.")
        elif t_type == "email_check_ok":
            self.lbl_text.setText("사용가능한 이메일 주소입니다.")
        elif t_type == "email_check_no":
            self.lbl_text.setText("이미 존재하는 이메일 주소입니다.")
        elif t_type == "email_check_not":
            self.lbl_text.setText("이메일 중복확인을 진행 해주세요")
        elif t_type == "email_wrong":
            self.lbl_text.setText("이메일 주소를 올바르게 입력해주세요")
        elif t_type == "email_input":
            self.lbl_text.setText("이메일 주소를 입력해주세요")
        elif t_type == "pwd_input":
            self.lbl_text.setText("비밀번호를 입력해주세요")
        elif t_type == "join_pwd_input_len":
            self.lbl_text.setText("비밀번호를 8 자리이상 입력해주세요")
        elif t_type == "join_pwd_same":
            self.lbl_text.setText("비밀번호와 비밀번호 확인이 다릅니다.")
        elif t_type == "join_name_input":
            self.lbl_text.setText("이름을 입력해주세요")
        elif t_type == "join_success":
            self.lbl_text.setText("회원가입이 완료 되었습니다.")

        elif t_type == "fail_analyze":
            self.lbl_text.setText("사진 분석에 실패했습니다.")

        elif t_type == "species_check":
            self.lbl_text.setText(f"촬영한 작품의 품종이\n'{text}'가 맞나요?")
        elif t_type == "no_species":
            self.lbl_text.setText("사진을 다시 촬영해주세요.")
        elif text:
            self.lbl_text.setText(text)