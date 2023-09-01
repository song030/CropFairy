import json
import os

import pandas as pd

pd.set_option('display.max_columns', None) # 전체 열 보기
pd.set_option('display.max_rows', None) # 전체 행 보기
pd.set_option('display.width', None) # 모든 value 잘리지 않고 출력하는 방법

target_path = r"D:\CropFairy\AI\cucumber" # ㅣlee 폴더

image_path = target_path+"\\images\\train2"
label_path = target_path+"\\labels\\train2"

json_path = r"D:\104.식물 병 유발 통합 데이터\1.Training\라벨링데이터\TL4_오이"  #json파일 폴더 경로

image_list = os.listdir(image_path)
for image in image_list:
    print(image)
    file_name = image.split(".")[0]
    file_name += ".json"
    with open(f"{json_path}\\{file_name}", "r") as json_file:
        json_data = json.load(json_file)
        json.dumps(json_data, indent="/t")
        # print(json_data)

        code = json_data["annotations"]["disease"]
        # '00', '01', 'A5', 'A6', 'B2', 'B3', 'B6', 'B7', 'B8'
        if code == "a3":
            code = 1
        elif code == "a4":
            code = 2

        # 질병 코드 변환 넣기
        img_width = json_data["description"]["width"]
        img_height = json_data["description"]["height"]

        # print(position)
        positions = json_data["annotations"]["part"]
        text = ""
        if len(positions) == 0:
            positions = json_data["annotations"]["bbox"]

        # print(positions)
        for pos in positions:
            target_width = pos["w"]
            target_height = pos["h"]
            x_center = pos["x"] + (target_width / 2)
            y_center = pos["y"] + (target_height / 2)

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