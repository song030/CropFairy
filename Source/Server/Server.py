import base64
import socket
import pickle
import sys
import cv2
import numpy as np

from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal

import json
import sqlite3
import select
from socket import *
from threading import *

from Source.Common.DBConnector import DataClass

# 사용할 구분자
header_split = chr(1)
list_split_1 = chr(2)
list_split_2 = chr(3)


class Server():
    '''
    실습실 종혁: 10.10.20.114
    기숙사 독서실 : 192.168.0.88
    '''
    # HOST = '10.10.20.114'
    # gethostbyname(gethostname())
    HOST = gethostbyname(gethostname())
    PORT = 5050
    BUFFER = 1500000
    FORMAT = 'utf-8'

    connected_member = list()

    def __init__(self, db_conn: DataClass):
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self.db_conn = db_conn
        self.server_socket = None
        self.config = None
        self.sockets_list = list()
        self.clients = dict()
        self.thread_for_run = None
        self.run_signal = True

    def start(self):
        if self.thread_for_run is not None:  # 실행중이면 종료 시키기
            return
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET(ipv4를 의미)
        self.server_socket.bind((self.HOST, self.PORT))  # 바인딩
        self.server_socket.listen()  # 리슨 시작
        self.sockets_list.clear()  # 소켓리스트 클리어
        self.sockets_list.append(self.server_socket)
        self.run_signal = True
        self.thread_for_run = Thread(target=self.run)
        self.thread_for_run.start()

    def stop(self):
        self.run_signal = False
        if self.thread_for_run is not None:
            self.thread_for_run.join()
        self.server_socket.close()
        self.thread_for_run = None

    def run(self):
        while True:
            if self.run_signal is False:
                break
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list, 0.1)
            except Exception:
                continue
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    user = self.receive_message(client_socket)
                    if user is False:
                        continue
                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user

                else:
                    message = self.receive_message(notified_socket)
                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    # client 한테 send 하는 함수
    def send_to_pickle(self, client_socket: socket, send_data: list):
        # # 서버에서 전송할 데이터 (파이썬 객체)
        # data_make_send = send_data

        # 데이터를 직렬화하여 이진 데이터로 변환
        pickle_data = pickle.dumps(send_data)
        client_socket.send(pickle_data)

    def receive_message(self, client_socket: socket):
        try:
            received_data = client_socket.recv(self.BUFFER)  # client recv data
            received_object = pickle.loads(received_data)  # 이진 데이터를 파이썬 객체로 역직렬화
            header = received_object[0]  # header = client recv data index[0]

            if header == 'idrd_check':  # email 중복 확인
                input_email = received_object[1]  # input data = client recv data index[1:]
                result = self.db_conn.idrd_check(input_email)  # 입력한 email 사용가능 여부 반환
                send_data = ["idrd_check_result", result]  # client send_dat(header, data)list

                print(f"idrd_check 결과: {send_data}")
                self.send_to_pickle(client_socket, send_data)

            elif header == 'sign_up':  # 회원가입
                # [헤더, 아이디, 비밀번호]

                input_data = received_object[1:]  # input data = client recv data index[1:]
                result = self.db_conn.insert_user(input_data)  # DB return 값 받아옴
                send_data = ["sing_up_result", result]  # client send_dat(header, data)list

                print(f"sign_up 결과: {send_data}")
                self.send_to_pickle(client_socket, send_data)

            elif header == 'sing_in':  # 로그인
                # [header, email, pw]
                input_data = received_object[1:]  # input data = client recv data index[1:]
                result = self.db_conn.sing_in(input_data)  # DB return 값 받아옴
                send_data = ["sing_in_result", result]  # client send_dat(header, data)list

                print(f"sing_in 결과: {send_data}")
                self.send_to_pickle(client_socket, send_data)

            elif header == 'insert_pad_result':  # 진단 내역 저장
                input_data = received_object[1:]  # input data = client recv data index[1:]
                self.db_conn.insert_pad_result(input_data)  # DB return 값 받아옴

            elif header == 'get_pad_result':  # 진단 내역 반환
                input_data = received_object[1:]  # input data = client recv data index[1:]
                result = self.db_conn.return_pad_result(input_data)  # DB return 값 받아옴
                send_data = ["get_pad_result", result]  # client send_dat(header, data)list
                print(f"get_pad_result 결과: {send_data}")
                self.send_to_pickle(client_socket, send_data)

            elif header == 'get_pad_info':  # 진단 병해충 정보 반환
                input_data = received_object[1:]  # input data = client recv data index[1:]
                result = self.db_conn.return_pad_info(input_data)  # DB return 값 받아옴
                result2 = self.db_conn.select_pad_info(result[1])  # DB return 값 받아옴

                send_data = ["get_pad_info", result + result2]  # client send_dat(header, data)list
                print(send_data)
                self.send_to_pickle(client_socket, send_data)

            elif header == 'send_to_imginfo':  # 이미지 정보 받아와서 모델 평가
                img_data = received_object[1]  # input data = client recv data index[1:]
                print(img_data)
                # 이미지 저장
                cv2.imwrite('server_test_save_img.jpg', img_data)
                print("이미지 저장안됨?")
                # print(f"이미지: {img_data}")
                # #
                # new_height = 150
                # new_width = 150
                # # # NumPy 파일을 저장할 리스트
                # data_list = []
                # np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)
                #
                # image = cv2.imread(img_path)
                # image_vector = image.flatten()
                #
                # image_rgb = cv2.cvtColor(image_vector, cv2.COLOR_BGR2RGB)
                # # 이미지를 NumPy 배열로 변환
                # image_np = np.array(image_rgb)
                # # 이미지.npy 리사이징
                # resized_image = cv2.resize(image_np, (new_width, new_height))
                #
                # # 리사이징한 이미지 넘파이 리스트에 넣기 -> 이미지를 여러장 넣었을때
                # data_list.append(resized_image)
                #
                # # result = self.db_conn.return_pad_info(input_data)  # DB return 값 받아옴
                # # result2 = self.db_conn.select_pad_info(result[1])  # DB return 값 받아옴
                #
                # # send_data = ["get_pad_info", result + result2] # client send_dat(header, data)list
                # # print(send_data)
                # # self.send_to_pickle(client_socket, send_data)


        except:
            pass


if __name__ == '__main__':
    Server(DataClass()).start()
