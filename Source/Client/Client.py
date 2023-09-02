import base64
import socket
import pickle

from PyQt5.QtCore import pyqtSignal, QObject
from threading import *
from socket import *

_SERVER_IP = gethostbyname(gethostname())
_SERVER_PORT = 5050
BUFFER = 1000000
FORMAT = "utf-8"
_CONNECT = (_SERVER_IP, _SERVER_PORT)

# 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class Client(QObject):
    # --- 시그널
    idrd_check_result = pyqtSignal(bool)
    sing_up_result = pyqtSignal(bool)
    sing_in_result = pyqtSignal(list)
    get_pad_result = pyqtSignal(list)
    ml_result = pyqtSignal(list)
    dl_result = pyqtSignal(list)
    return_bug_info = pyqtSignal(list)
    return_disease_info = pyqtSignal(list)
    re_clicked_pad_info = pyqtSignal(list)

    def __init__(self, client_controller=None):
        super().__init__()
        self.client_controller = client_controller
        self.client_socket = None
        self._connected = None

        self.connect_server()

        self.listeningThread = Thread(target=self.check_server_response, daemon=True)
        self.listeningThread.start()

    # 서버 접속
    def connect_server(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(_CONNECT)
        message = f"{f'enter{header_split}접속한다':{BUFFER}}".encode(FORMAT)
        self.send(message)
        self._connected = True

    # 서버 send 함수
    def send(self, pickle_data):
        print(f"보내는 데이터{pickle_data}")
        self.client_socket.send(pickle_data)
        print("보냈음")

    # recv 관련 함수들
    def check_server_response(self):
        while self._connected:
            try:
                received_data = self.client_socket.recv(BUFFER)
                # 이진 데이터를 파이썬 객체로 역직렬화
                received_object = pickle.loads(received_data)
                self._parse_packet(received_object)

            except Exception as e:
                pass

    # recv 받은 데이터로 이벤트 발생
    def _parse_packet(self, p: str):
        received_object = p
        header = received_object[0]

        if header == 'idrd_check_result':  # 아이디 중복체크
            result = received_object[1]
            print(result)
            self.idrd_check_result.emit(result)


        elif header == 'sing_up_result':  # 회원가입 요청 결과
            result = received_object[1]
            self.idrd_check_result.emit(result)


        elif header == 'sing_in_result':  # 로그인 요청 결과
            result = received_object[1]
            if not result:
                self.sing_in_result.emit(result)
                print(f"로그인 실패:{result}")
            else:
                self.sing_in_result.emit(result)
                print(f"로그인 성공:{result}")

        elif header == 'get_pad_result':  # 진단 내역 반환받음
            result = received_object[1]
            if not result:
                pass
            else:
                self.get_pad_result.emit(result)

        elif header == 'ml_result':  # 품종 판별 결과
            print("client 드옴?")
            result = [received_object[1]]
            print(result)
            self.ml_result.emit(result)

        elif header == 'dl_result':  # 품종 판별 결과
            result = received_object[1:]
            result = [result]
            print("딥러닝 결과")
            self.dl_result.emit(result)

        elif header == 'get_pad_info':  # 병충해 정보 반환
            result = received_object[1]
            if not result:
                print(f"내역 없음:{result}")
            else:
                print(f"결과 불러오기 성공:{result}")

        elif header == 'return_bug_info':  # 해충 정보 반환
            result = received_object[1]
            self.return_bug_info.emit(result)

        elif header == 'return_disease_info':  # 질병 정보 반환
            result = received_object[1]
            self.return_disease_info.emit(result)

        elif header == 're_clicked_pad_info':  # 클릭한 셀의 질병 정보 반환
            result = received_object[1]
            self.re_clicked_pad_info.emit(result)
