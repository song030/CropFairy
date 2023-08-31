import json
import os

import pandas as pd

pd.set_option('display.max_columns', None) # 전체 열 보기
pd.set_option('display.max_rows', None) # 전체 행 보기
pd.set_option('display.width', None) # 모든 value 잘리지 않고 출력하는 방법

target_path = r"D:\CropFairy\AI\tomato" # ㅣlee 폴더

image_path = target_path+"\\images\\train"
label_path = target_path+"\\labels\\train"

json_path = r"D:\104.식물 병 유발 통합 데이터\1.Training\라벨링데이터\TL5_토마토"  #json파일 폴더 경로

image_list = os.listdir(image_path)
for image in image_list:
    print(image)
    file_name = image.split(".")[0]
    file_name += "jpg.json"
    with open(f"{json_path}\\{file_name}", "r") as json_file:
        json_data = json.load(json_file)
        json.dumps(json_data, indent="/t")
        # print(json_data)

        code = json_data["annotations"]["disease"]
        # '00', '01', 'A5', 'A6', 'B2', 'B3', 'B6', 'B7', 'B8'
        if code == "00":
            code = 0
        elif code == "01":
            code = 1
        elif code == "02":
            code = 2
        elif code == "03":
            code = 3
        elif code == "04":
            code = 4
        elif code == "05":
            code = 5
        elif code == "06":
            code = 6
        elif code == "07":
            code = 7
        elif code == "08":
            code = 8
        elif code == "09":
            code = 9
        elif code == "10":
            code = 10
        elif code == "11":
            code = 11
        elif code == "12":
            code = 12
        elif code == "13":
            code = 13
        elif code == "14":
            code = 14
        elif code == "15":
            code = 15
        elif code == "16":
            code = 16
        elif code == "17":
            code = 17
        elif code == "18":
            code = 18
        elif code == "19":
            code = 19
        elif code == "20":
            code = 20


        # 질병 코드 변환 넣기
        img_width = json_data["description"]["width"]
        img_height = json_data["description"]["height"]

        # print(position)
        # positions = json_data["annotations"]["object"] ["points"][0]   # 해충좌표로 바꾸기

        position = json_data["annotations"]["points"]

        # 주어진 좌표
        xtl, ytl = position[0]["xtl"], position[0]["ytl"]
        xbr, ybr = position[0]["xbr"], position[0]["ybr"]

        # 이미지의 위치 (X, Y) 계산
        X, Y = xtl, ytl
        # 이미지의 너비 (W)와 높이 (H) 계산
        W = xbr - xtl
        H = ybr - ytl

        text = ""
        # if len(positions) == 0:
        #     positions = json_data["annotations"]["bbox"] # 작물 좌표로 바꾸기

        # print(positions)
        for pos in positions:
            target_width = W
            target_height = H
            x_center = X + (target_width / 2)
            y_center = Y + (target_height / 2)
            # target_width = pos["w"]
            # target_height = pos["h"]
            # x_center = pos["x"] + (target_width / 2)
            # y_center = pos["y"] + (target_height / 2)

            target_width_normalized = f"{(target_width / img_width):.6f}"
            target_height_normalized = f"{(target_height / img_height):.6f}"
            x_center_normalized = f"{(x_center / img_width):.6f}"
            y_center_normalized = f"{(y_center / img_height):.6f}"

            text += f"{code} {x_center_normalized} {y_center_normalized} {target_width_normalized} {target_height_normalized}\n"
            file_path = image.split(".")[0]
            file_path += ".txt"

            f = open(label_path+"\\" + file_path, "w")
            f.write(text)
            f.close()
