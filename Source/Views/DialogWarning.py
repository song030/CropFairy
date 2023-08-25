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

    def closeEvent(self, a0):
        pass

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
    def set_dialog_type(self, bt_cnt=1, t_type="", text=""):
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
        elif t_type == "login_approve":
            self.lbl_text.setText("회원 승인 대기중입니다.")
        elif t_type == "login_success":
            self.lbl_text.setText(f"'{text}'님 안녕하세요.")
        elif t_type == "id_check_ok":
            self.lbl_text.setText("사용가능한 아이디입니다.")
        elif t_type == "id_check_no":
            self.lbl_text.setText("이미 존재하는 아이디입니다.")
        elif t_type == "join_id_input":
            self.lbl_text.setText("아이디를 입력해주세요")
        elif t_type == "join_id_check":
            self.lbl_text.setText("아이디 중복확인을 진행해주세요.")
        elif t_type == "join_pwd_input":
            self.lbl_text.setText("비밀번호를 입력해주세요")
        elif t_type == "join_pwd_same":
            self.lbl_text.setText("비밀번호와 비밀번호 확인이 다릅니다.")
        elif t_type == "join_name_input":
            self.lbl_text.setText("이름을 입력해주세요")
        elif t_type == "join_success":
            self.lbl_text.setText("회원가입이 완료 되었습니다.\n관리자 승인 후 로그인 가능합니다.")
        elif t_type == "save_fail":
            self.lbl_text.setText("저장 실패 했습니다.")
        elif t_type == "save_success":
            self.lbl_text.setText("저장 완료 되었습니다.")
        elif t_type == "no_select_row":
            self.lbl_text.setText("선택된 행이 없습니다.")
        elif t_type == "input_sch_name":
            self.lbl_text.setText("학교이름을 입력해주세요.")
        elif t_type == "input_sch_addr":
            self.lbl_text.setText("주소를 입력해주세요.")
        elif t_type == "brc_ctg":
            self.lbl_text.setText("분기 카테고리를 입력해주세요.")
        elif t_type == "brc_ctg_digit":
            self.lbl_text.setText("분기 카테고리를 숫자만 입력해주세요.")
        elif t_type == "talk_cnt":
            self.lbl_text.setText("회차 카테고리를 입력해주세요.")
        elif t_type == "talk_cnt_digit":
            self.lbl_text.setText("회차 카테고리를 숫자만 입력해주세요.")
        elif t_type == "talk_save_check":
            self.lbl_text.setText("저장을 진행하는 \n경우 학교정보는 수정할수 없습니다.\n진행하시겠습니까?")
        elif t_type == "find_before":
            self.lbl_text.setText("엑셀파일을 열어 \n변환을 진행할 연락처 정보를 입력해주세요.")
        elif t_type == "find_search":
            self.lbl_text.setText("엑셀파일을 열어 \n검증을 진행할 연락처 정보를 입력해주세요.")
        elif t_type == "find_result":
            self.lbl_text.setText("이미 결과가 나왔습니다.\n다른 정보를 입력해주세요.")

        elif text:
            self.lbl_text.setText(text)