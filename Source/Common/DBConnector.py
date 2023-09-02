import sys
import geopy.distance
import psycopg2 as pg
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import os


class DataClass:
    def __init__(self):
        # print(sys.path)
        self.pgdb = pg.connect(
            host='10.10.20.114',
            # host='localhost',
            dbname='CropFairy',
            user='postgres',
            password='ilsan1236526',
            port=5432
        )
        self.engine = create_engine(f'postgresql://postgres:ilsan1236526@10.10.20.114:5432/CropFairy')

    def end_conn(self):
        self.pgdb.close()

    def idrd_check(self, input_email):
        """
        :아이디 중복확인
        """
        cur = self.pgdb.cursor()
        # 쿼리문 및 중복 확인
        query = f"SELECT * FROM public.\"TB_USER\" WHERE \"USER_EMAIL\" = '{input_email}';"
        cur.execute(query)
        username_id = cur.fetchone()
        # self.end_conn()  # 커서 닫기

        # 결과값 리턴
        if username_id is None:
            return True  # 사용 가능한 아이디일때
        return False  # 사용 불가능한 아이디일때

    def insert_user(self, sign_up_data):
        """
        회원가입
        :return:
        """
        try:
            user_email, user_pw = sign_up_data
            cur = self.pgdb.cursor()
            # 쿼리문 및 중복 확인
            query = f"INSERT INTO public.\"TB_USER\" (\"USER_EMAIL\", \"USER_PW\") " \
                    f"VALUES ('{user_email}', '{user_pw}')"
            cur.execute(query)
            self.pgdb.commit()
            return True
        except:
            return False

    def sing_in(self, sing_in_data):
        """
        로그인
        :return:
        """
        input_email, input_pw = sing_in_data
        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT * FROM public.\"TB_USER\" WHERE \"USER_EMAIL\" = '{input_email}' AND \"USER_PW\" = '{input_pw}';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        results = [(list(record)) for record in results]
        # 연결 종료
        # self.end_conn()
        # 결과값 리턴
        if len(results) > 0:
            return results[0]
        return [False]

    def return_pad_info(self, pad_code):
        """
        병충해 코드가 들어오면 정보들 반환
        :return:
        """
        # pad_code = pad_code[0]
        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT * FROM public.\"TB_PAD\" WHERE \"PAD_ID\" = '{pad_code}';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        results = [(list(record)) for record in results]
        # 결과값 리턴
        if len(results) > 0:
            return results[0]
        return [False]

    def return_pad_info2(self, pad_name):
        """
        병충해 이름이 들어오면 정보들 반환
        :return:
        """
        # pad_code = pad_code[0]
        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT \"PAD_CTG\" FROM public.\"TB_PAD\" WHERE \"PAD_NAME\" = '{pad_name}';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        results = [(list(record)) for record in results]
        # 결과값 리턴
        if len(results) > 0:
            return results[0]
        return [False]

    def return_bug_info(self):
        """
        병충해 코드가 들어오면 정보들 반환
        :return:
        """
        pad_ctg = "해충"
        print("db")
        # pad_code = pad_code[0]
        # 커서 생성
        cur = self.pgdb.cursor()
        # sql_query = """
        # SELECT table1.name, table1.info, table2.category
        # FROM table1
        # INNER JOIN table2
        # ON table1.name = table2.name
        # WHERE table1.name = '특정이름';
        # """
        # sql_query = f"SELECT * FROM public.\"TB_PAD\" WHERE \"PAD_CTG\" = '{pad_ctg}';"
        sql_query = f"SELECT \"TB_PAD\".\"PAD_NAME\", \"TB_PAD\".\"PAD_CTG\", \"TB_PAD_INFO\".\"PAD_INFO3\"FROM public." \
                    f"\"TB_PAD\"INNER JOIN \"TB_PAD_INFO\" ON \"TB_PAD\".\"PAD_NAME\" = \"TB_PAD_INFO\".\"PAD_NAME\"" \
                    f"WHERE \"TB_PAD\".\"PAD_CTG\" = '해충';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        print(results)
        results = [(list(record)) for record in results]
        # 결과값 리턴
        if len(results) > 0:
            return results
        return [False]

    def return_disease_info(self):
        """
        병충해 코드가 들어오면 정보들 반환
        :return:
        """
        data = "해충"
        # pad_code = pad_code[0]
        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT \"TB_PAD\".\"PAD_NAME\", \"TB_PAD\".\"PAD_CTG\", \"TB_PAD_INFO\".\"PAD_INFO3\"FROM public." \
                    f"\"TB_PAD\"INNER JOIN \"TB_PAD_INFO\" ON \"TB_PAD\".\"PAD_NAME\" = \"TB_PAD_INFO\".\"PAD_NAME\"" \
                    f"WHERE \"TB_PAD\".\"PAD_CTG\" != '해충' AND \"TB_PAD\".\"PAD_CTG\" != '문제없음';"
        # sql_query = f"SELECT * FROM public.\"TB_PAD\" WHERE \"PAD_CTG\" != '{data}' AND \"PAD_CTG\" != '문제없음';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        results = [(list(record)) for record in results]
        # 결과값 리턴
        if len(results) > 0:
            return results
        return [False]

    def select_pad_info(self, pad_name):
        """
        병충해 이름을 받아 info 반환
        """
        if "탄저병" in pad_name:
            pad_name = "탄저병"
        elif "노균병" in pad_name:
            pad_name = "노균병"
        elif "흰가루병" in pad_name:
            pad_name = "흰가루병"
        # print("정보 반환 db", pad_code)

        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT * FROM public.\"TB_PAD_INFO\" WHERE \"PAD_NAME\" = '{pad_name}';"
        cur.execute(sql_query)
        # 결과 가져오기
        results = list(cur.fetchall())  # 리스트로 변환
        print(results)
        results = [(list(record)) for record in results]
        print(results)
        # 연결 종료
        # self.end_conn()

        print(results)
        # 결과값 리턴
        if len(results) > 0:
            return results[0]
        return [False]

    def insert_pad_result(self, pad_result_data):
        """
        진단 내역 저장
        result_species : 딥러닝 결과
        result_stat : 머신러닝 결과
        :return:
        """

        user_id, result_species, result_stat = pad_result_data
        print(pad_result_data)
        save_time = self.return_datetime('time')
        print(save_time)
        try:
            cur = self.pgdb.cursor()
            # 쿼리문 및 중복 확인
            query = f"INSERT INTO public.\"TB_RESULT\" (\"USER_ID\", \"RESULT_SPECIES\", \"RESULT_STAT\", \"SAVE_TIME\") VALUES ('{user_id}', '{result_species}', '{result_stat}', '{save_time}')"
            print(query)
            cur.execute(query)
            self.pgdb.commit()
            print("내역 저장 성공")

        except Exception as ex:
            print(ex)

    def return_pad_result(self, user_id):
        """
        로그인한 유저의 진단 내역 반환
        :return:
        """
        user_id = user_id[0]
        # 커서 생성
        cur = self.pgdb.cursor()
        sql_query = f"SELECT \"RESULT_SPECIES\", \"RESULT_STAT\", \"SAVE_TIME\" FROM public.\"TB_RESULT\" WHERE \"USER_ID\" = '{user_id}';"
        # sql_query = f"SELECT \"RESULT_SPECIES\" \"RESULT_STAT\" \"SAVE_TIME FROM\" public.\"TB_RESULT\" WHERE \"USER_ID\" = '{user_id}';"
        cur.execute(sql_query)
        # 결과 가져오기
        # results = list(cur.fetchall())  # 리스트로 변환
        results = list(cur)  # 리스트로 변환
        results = [(list(record)) for record in results]
        # 연결 종료
        # self.end_conn()
        # 결과값 리턴
        if len(results) > 0:
            return results
        return []

    def return_datetime(self, type):
        """원하는 날짜/시간 포멧을 반환"""
        now = datetime.now()  # 시간
        if type == 'date':
            now_format = now.strftime("%Y-%m-%d")  # 년 월 일
        elif type == 'time':
            now_format = now.strftime("%Y-%m-%d %H:%M:%S")  # 년 월 일 시 분 초
        elif type == 'time_only':
            now_format = now.strftime("%H:%M:%S")  # 시 분 초

        # print('[dateimte.py]시간 포멧팅: ', now_format)
        return now_format

    def update_user_pw(self, pw, email):
        """
        :param pw:
        :param email:
        :사용자가 비밀번호 변경 시 DB 해당 내용을 DB에 업데이트
        """
        cursor = self.pgdb.cursor()
        cursor.execute(f"update USERS set user_pw='{pw} where user_email='{email}")
        self.pgdb.commit()

# if __name__ == '__main__':
#     db = DataClass()
#     a = db.select_dong_population()
#     print(a)

# list_1 = []
# dict_1 = {}
# for i in a:
#     dong_code = i[0]
#     population = i[1]
#     # print(dong_code)
#     population_data = db.select_dong(dong_code)
#     list_1.append(population_data[0][0])
#     dict_1[population_data[0][0]] = population
# print(dict_1)

# print(a)
