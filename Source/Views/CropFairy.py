import cv2
import numpy as np
import pickle

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor, QPixmap
from PyQt5.QtCore import QSize, Qt, QDate
from PyQt5.Qt import QMainWindow

from Source.Views.UI_CropFairy import Ui_CropFairy
from Source.Views.DialogJoin import DialogJoin
from Source.Views.DialogResult import DialogResult
from Source.Views.DialogWarning import DialogWarning
from Source.Views.DialogLoading import DialogLoading
from Source.Client.Client import Client


class CropFairy(QMainWindow, Ui_CropFairy):

    def __init__(self):
        super().__init__()

        # --- 변수 선언
        self.upload_text = "* 정확도 높이는 꿀팁 *\n\n1. 사진은 열매나 잎이 가운데, 정면으로 오도록 촬영해주세요.\n2. 열매나 잎 주위의 배경이 깨끗할수록 정확도가 올라갑니다."
        self.mode = ""
        # self.upload_image = False
        # --- 회원가입 변수
        self.use_email_check = False
        # --- 로그인 유저 변수
        self.login = False
        self.singin_email = False
        self.singin_user_id = False
        # --- ai 결과 변수
        self.ml_result = None
        self.dl_result = None
        # ---
        # --- 초기화
        self.set_Ui()

        # 검정 투명 배경
        self.back = QLabel(self)
        self.back.setGeometry(0, 0, 1024, 860)
        self.back.setStyleSheet("background-color: rgba(20, 20, 20, 50);")
        self.back.hide()

        self.dlg_warning = DialogWarning()

        self.dlg_loading = DialogLoading()
        self.dlg_loading.close()

        self.connect_Event()
        self.client = Client()
        self.connect_thread_signal()

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
        # 공통
        self.dlg_warning.showEvent = lambda e: self.back.show()
        self.dlg_warning.closeEvent = lambda e: self.back.hide()

        # 메인화면
        self.btn_login.clicked.connect(self.btn_login_click)
        self.btn_join.clicked.connect(self.btn_join_click)
        self.btn_bug.clicked.connect(self.btn_bug_click)
        self.btn_disease.clicked.connect(self.btn_disease_click)
        self.btn_exit.clicked.connect(self.btn_exit_click)
        self.btn_list.clicked.connect(self.btn_list_click)
        self.btn_back.clicked.connect(self.btn_back_click)

        # 진단하기
        self.btn_upload.clicked.connect(self.btn_upload_click)
        self.btn_start.clicked.connect(self.btn_start_click)

        # 내역조회

    # 메인으로 이동시 화면 설정
    def move_page_main(self):
        self.mode = ""
        self.stack_control.setVisible(False)
        self.btn_back.setVisible(False)
        self.btn_logout.setVisible(False)
        self.lbl_title.setText(" ")

        if self.login:
            self.widget_login.setVisible(False)
            self.widget_analyze.setVisible(True)
            self.btn_list.setVisible(True)
        else:
            self.widget_login.setVisible(True)
            self.widget_analyze.setVisible(False)
            self.btn_list.setVisible(False)

        self.stacke_main.setCurrentWidget(self.page_main)

    # 내역조회 화면으로 이동시 화면 설정
    def move_page_list(self):
        self.stack_control.setCurrentWidget(self.control_page)
        self.stack_control.setVisible(True)
        self.btn_back.setVisible(True)
        self.btn_logout.setVisible(True)
        self.btn_list.setEnabled(False)
        self.lbl_title.setText("진단 내역 조회")
        self.stacke_main.setCurrentWidget(self.page_list)

    # 진단 내역 버튼
    def btn_list_click(self):
        senddata = ["get_pad_result", self.singin_user_id]
        self.send_data(senddata)
        self.move_page_list()

    def btn_back_click(self):
        self.move_page_main()

    # -----------------------------------------------------signal-----------------------------------------------------
    def connect_thread_signal(self):
        # 메세지 발송
        self.client.idrd_check_result.connect(self.idrd_check_result)
        self.client.sing_up_result.connect(self.sing_up_result)
        self.client.sing_in_result.connect(self.sing_in_result)
        self.client.get_pad_result.connect(self.set_pad_result)
        self.client.ml_result.connect(self.get_ml_result)
        self.client.dl_result.connect(self.get_dl_result)

    # 딥러닝 품종 판별 결과 회신
    def get_dl_result(self, result):
        self.result_dlg(result)
        # self.send_data(send_data)
        pass

    # 도출된 결과들 다이얼로그에 띄우기
    def result_dlg(self, result):
        result1 = result[0]
        result2 = result[1]
        # todo 받은 결과들 다이얼로그에 띄우기 어떤식으로 받아오는지 아직 몰루
        crop, pad_name, pad_ctg, info1, info2, info3 = self.ml_result, result1[1], result1[2], result2[0], result2[1], result2[2]

        pass



    def get_ml_result(self, result):
        self.dlg_loading.hide()
        self.ml_result = result[0]
        self.dlg_warning.set_dialog_type("species_check", text=self.ml_result, bt_cnt=2)

        # 품종 맞을때
        if self.dlg_warning.exec():
            self.client.img_send(self.img_path)
            print(self.ml_result)
            send_data = ["dl_start", self.mode, self.ml_result, self.singin_user_id]

            self.send_data(send_data)
            # TODO 서버로 딥러닝 진행 시그널 보내기

        # 품종이 틀렸을 때
        else:
            self.dlg_warning.set_dialog_type("no_species", bt_cnt=1)
            self.dlg_warning.exec()
            self.lbl_upload_image.setText(self.upload_text)
            self.btn_start.setVisible(False)

    # 반환 받은 유저 진단 내역 테이블 위젯에 집어넣기
    def set_pad_result(self, result):
        result_list = result

        self.table_list.setColumnCount(4)  # 열의 수 설정
        self.table_list.setHorizontalHeaderLabels(["진단 일시", "품종", "구분", "내용"])
        self.table_list.verticalHeader().setVisible(False)
        self.table_list.setColumnWidth(0, 187)
        self.table_list.setColumnWidth(1, 80)
        self.table_list.setColumnWidth(2, 110)
        self.table_list.setColumnWidth(3, 185)

        # todo: 밑에 머신러닝과 딥러닝 결과로 품종 구분 내용 가져와서 집어넣는걸로 바꿔야함
        for result in result_list:  # 3은 열의 수
            current_row_count = self.table_list.rowCount()
            self.table_list.insertRow(current_row_count)
            print(result)
            for col, info in enumerate(result):
                item = QTableWidgetItem(f"{info}")
                self.table_list.setItem(current_row_count, col, item)

    # 로그인한 유저의 정보와 로그인 결과 반환받음
    def sing_in_result(self, result):
        if result[0] == False:
            self.dlg_warning.set_dialog_type("login_error")
            self.dlg_warning.exec()
        else:
            self.login = True
            self.singin_email = result[1]
            self.singin_user_id = result[0]

            self.move_page_main()
            self.dlg_warning.set_dialog_type("login_success", text=self.singin_email)
            self.dlg_warning.exec()

    # 회원가입 성공 다이얼로그 띄우기
    def sing_up_result(self, result):
        if result:
            self.dlg_warning.set_dialog_type("join_success")
            self.dlg_warning.exec()
        else:
            print("일정 횟수 틀리면 로봇입니까 띄워 보고싶다")

    # 아이디 중혹확인 결과 반환 시그널
    def idrd_check_result(self, result):
        self.use_email_check = result
        if result:
            self.dlg_warning.set_dialog_type("email_check_ok")
            self.dlg_warning.exec()
        else:
            self.dlg_warning.set_dialog_type("email_check_no")
            self.dlg_warning.exec()
        print(self.use_email_check, "main")

    # -----------------------------------------------------send-------------------------------------------------------
    # 클라이언트에서 서버에 보낼 데이터 피클로 변환해서 보내기
    def send_data(self, data_list):
        # a = ["get_pad_info", 102]
        data = data_list
        pickle_data = pickle.dumps(data)
        self.client.send(pickle_data)

    # ----------------------------------------------------- Main -----------------------------------------------------

    # 진단화면으로 이동시 화면 설정
    def move_page_analyze(self):
        self.stack_control.setCurrentWidget(self.control_analyze)
        self.stack_control.setVisible(True)
        self.btn_back.setVisible(True)
        self.btn_start.setVisible(False)
        self.btn_list.setEnabled(True)
        self.lbl_upload_image.setText(self.upload_text)
        self.lbl_title.setText("진단하기")
        self.stacke_main.setCurrentWidget(self.page_analyze)

    # 로그인
    def btn_login_click(self):
        self.sign_rqst()

    # 로그인 요청
    def sign_rqst(self):
        edt_email = self.edt_email.text()
        edt_pwd = self.edt_pwd.text()

        # 이메일 입력 확인
        if edt_email == "":
            self.dlg_warning.set_dialog_type("email_input")
            self.dlg_warning.exec()
        # 비밀번호 입력 확인
        elif edt_pwd == "":
            self.dlg_warning.set_dialog_type("pwd_input")
            self.dlg_warning.exec()
        else:
            data = ["sing_in", edt_email, edt_pwd]
            self.send_data(data)

    # 회원가입
    def btn_join_click(self):
        self.dlg_join = DialogJoin(self)
        self.dlg_join.showEvent = lambda e: self.back.show()
        self.dlg_join.closeEvent = lambda e: self.back.hide()
        self.dlg_join.exec()

    # 진단하기 페이지 이동 버튼
    def btn_disease_click(self):
        self.mode = "disease"
        self.move_page_analyze()

    def btn_bug_click(self):
        self.mode = "bug"
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
        self.dlg_loading.show()
        """
        원천 데이터 이미지 라벨링된 범위만큼 이미지 자르로 numpy로 변환후 저장
        """
        self.client.img_send(self.img_path)
        new_height = 640
        new_width = 640
        img_path = self.img_path

        # 이미지를 읽어 넘파이 배열로 변환
        image = cv2.imread(img_path)
        image_np = np.array(image)

        # 이미지.npy 리사이징
        resized_image = cv2.resize(image_np, (new_width, new_height))
        # image_bytes = pickle.dumps(resized_image)

        send_data = ["send_to_img_save", resized_image]
        # send_data = ["send_to_imginfo", image_np]
        print(send_data)
        self.send_data(send_data)

        # print(data_list)
        # print("==========================")
        # print(data_list[0])
        # # pass
    # def btn_start_click(self):
    # # TODO 진단 버튼 시작시 서버로 이미지 발송는 내용 추가하기
    # """
    # 원천 데이터 이미지 라벨링된 범위만큼 이미지 자르로 numpy로 변환후 저장
    # """
    # img_path = self.img_path
    #
    # # 이미지 파일 열기
    # print("img1")
    # with open(img_path, 'rb') as f:
    #     img_data = base64.b64encode(f.read()).decode('utf-8')
    #     # image_data = image_file.read(2048)
    # print("img2")
    #
    # # while image_data:
    # #     client.send(image_data)
    # #     image_data = file.read(2048)
    # send_data = ["send_to_imginfo", img_data]
    # # print(send_data)
    # # self.send_data(send_data)
    #
    # # user_info = json.dumps(send_data)
    # # message = f"{f'insertuser{header_split}{user_info}'}"
    #
    # print("img3")
    # self.send_data(send_data)
    # # print(data_list)
    # # print("==========================")
    # # print(data_list[0])
    # # pass

    # --------------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#             app = QApplication(sys.argv)
#
#             # 글꼴 설정
#             fontDB = QFontDatabase()
#             fontDB.addApplicationFont("../../FONT/NanumSquareRoundB.ttf")
#             fontDB.addApplicationFont("../../FONT/NanumSquareRoundEB.ttf")
#             fontDB.addApplicationFont("../../FONT/NanumSquareRoundL.ttf")
#             fontDB.addApplicationFont("../../FONT/ONE Mobile POP.ttf")
#
#             crop_fairy = CropFairy()
#             crop_fairy.show()
#             app.exec()
