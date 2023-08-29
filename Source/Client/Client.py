import socket
import pickle

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from threading import *
from socket import *

# import socket
# _SERVER_IP = '10.10.20.114'
_SERVER_IP = gethostbyname(gethostname())
_SERVER_PORT = 5050
BUFFER = 1500000
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

    def __init__(self, client_controller=None):
        super().__init__()
        self.client_controller = client_controller
        self.client_socket = None
        self._connected = None

        self.connect_server()

        # self.listeningThread = Thread(target=self.check_server_response)
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
        self.client_socket.send(pickle_data)

    # pickle 관련 함수
    def get_all_data(self):
        try:
            with open("data.p", 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def add_data(self, no, subject, content):
        data = self.get_all_data()
        data[no] = {'no': no, 'subject': subject, 'content': content}
        with open('data.p', 'wb') as f:
            pickle.dump(data, f)

    def get_data(self, no):
        data = self.get_all_data()
        return data[no]

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
            # todo: emit
            result = received_object[1]
            print(result)
            self.idrd_check_result.emit(result)


        elif header == 'sing_up_result':  # 회원가입 요청 결과
            # todo: emit
            result = received_object[1]
            self.idrd_check_result.emit(result)


        elif header == 'sing_in_result':  # 로그인 요청 결과
            # todo: emit -> 회원 정보 보내서 저장 -> 저장된 유저 식별 코드로 사용내역 저장
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
                #todo: 진단 내역이 없습니다 진단하러 가시겠습니까? 기능 할까?
                # self.get_pad_result.emit(result)
                pass
            else:
                self.get_pad_result.emit(result)

        elif header == 'get_pad_info':  # 병충해 정보 반환
            # todo: emit -> 회원 정보 보내서 저장 -> 저장된 유저 식별 코드로 사용내역 저장
            result = received_object[1]
            if not result:
                print(f"내역 없음:{result}")
            else:
                print(f"결과 불러오기 성공:{result}")

# if __name__ == '__main__':
#     ClientApp()
#     # a = ["idrd_check", '1231231']
#     # a = ["sign_up", '이종혁1', '1234']
#     # a = ["sing_in", '이종1', '1234']
#     # a = ["get_pad_result", 8]
#     a = ["insert_pad_result", 8, '딥러닝 결과2', '머신러닝 결과2']
#     # a = ["get_pad_info", 102]
#     pickle_data = pickle.dumps(a)
#     Client().send(pickle_data)
