import base64
import os
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
        print(f"보내는 데이터{pickle_data}")
        self.client_socket.send(pickle_data)
        print("보냈음")
    def img_send(self, img_path):
        with open(img_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        send_data = f"dl_start{header_split}{img_data}"
        # print("피클로 잘 만들어?")
        # print(send_data)
        pickle_data = pickle.dumps(send_data)
        # self.send('size' + self.header_split + file_size)
        message = send_data.encode()
        message_length = len(message).to_bytes(4, byteorder='big')  # 메시지 길이를 바이트로 변환
        self.client_socket.send(message_length + message)
        # self.send(pickle_data)
    #     path = img_path # 여기에 파일 주소가 들어가야 함
    #     file_size = self.get_file_size(path) # 파일 사이즈를 밑에 함수로 받아오는거
    #
    #     send_data = ['size', file_size]
    #     print("피클로 잘 만들어?")
    #     pickle_data = pickle.dumps(send_data)
    #
    #     self.send(pickle_data) # 받는 쪽으로 파일 사이즈를 미리 보내주는거
    #     with open(path, 'rb') as file: # 파일 읽는거인데 'rb'가 비트 단위로 읽는다는 표시임
    #         try:
    #             data = file.read()
    #             self.client_socket.sendall(data) # 읽은 파일 내용 전체를 다 보내는거
    #             file.close() # 파일은 꼭닫아줍시다
    #             print('file sent')
    #
    #         except Exception as ex:
    #             print(ex)
    #
    # # 파일 크기를 측정해서 돌려주는 함수. 이게 제일 중요한 과정 중 하나임
    # def get_file_size(self, path):
    #     file_size = os.path.getsize(path)
    #     return str(file_size)



        # try:
        #     # 이미지를 읽고 이진 형식으로 직렬화
        #     with open(img_path, "rb") as image_file:
        #         while True:
        #             chunk = image_file.read(BUFFER)  # 작은 청크 읽기
        #             if not chunk:
        #                 break
        #             # 헤더와 이미지 데이터를 포함하는 리스트 생성
        #             send_data = ["image_data", chunk]
        #             # 서버에 데이터 전송
        #             self.client_socket.send(send_data)
        #             # self.send_data(client_socket, send_data)

        # except Exception as e:
        #     print(f"Error sending image: {str(e)}")
        # #=================================
        # # 이미지를 읽고 이진 형식으로 직렬화
        # with open(img_path, "rb") as image_file:
        #     image_data = image_file.read()
        # image_data_binary = pickle.dumps(image_data)
        #
        # # 헤더와 이미지 데이터를 포함하는 리스트 생성
        # send_data = ["dl_start", image_data_binary]
        # print("피클로 잘 만들어?")
        # pickle_data = pickle.dumps(send_data)
        # self.client_socket.send(pickle_data)
        # #============================
        # self.send(send_data)
        # # 서버에 데이터 전송
        # self.send_data(client_socket, send_data)
        #


        # print("이미지 서버에 보내기")
        # file = open(img_path, 'rb')
        # image_data = file.read(BUFFER - 20)
        # while image_data:
        #     print(image_data)
        #     self.send_img_pickle(image_data)
        #     # self.client_socket.send(image_data)
        #     image_data = file.read(BUFFER - 20)
        #
        # file.close()
    #
    # def send_img_pickle(self, img_data):
    #     print("피클로 잘 만들어?")
    #     data_list = ["dl_start", img_data]
    #     data = data_list
    #     pickle_data = pickle.dumps(data)
    #     print("피클로 잘 만들어?")
    #     self.send(pickle_data)

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
                # todo: 진단 내역이 없습니다 진단하러 가시겠습니까? 기능 할까?
                # self.get_pad_result.emit(result)
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
