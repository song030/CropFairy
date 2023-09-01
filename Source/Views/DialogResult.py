from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Source.Views.UI_DialogResult import Ui_DlgResult

class DialogResult(QDialog, Ui_DlgResult):
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
    def accept(self):
        self.setResult(1)
        self.close()

    def set_dialog(self, crop, pad_name, pad_ctg, info1, info2, info3):
        self.lbl_spedies_txt.setText(crop)
        self.lbl_name_txt.setText(pad_name)

        if pad_name == "정상":
            self.lbl_ctg_txt.setText(pad_ctg)
            self.lbl_info_1_txt.setText(info1)
            self.lbl_info_2_txt.setText(info2)

    # 이벤트 연결
    def connect_event(self):
        # 예, 확인 : accept (1)
        # 아니오, 닫기 : reject (0)
        self.btn_analyze.clicked.connect(self.accept)
        self.btn_main.clicked.connect(self.reject)
