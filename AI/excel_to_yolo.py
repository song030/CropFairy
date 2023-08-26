import json
import sys, os

import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None) # 전체 열 보기
pd.set_option('display.max_rows', None) # 전체 행 보기
pd.set_option('display.width', None) # 모든 value 잘리지 않고 출력하는 방법

target_path = "D:\CropFairy\AI\data\고추"
image_path = target_path+"\\images"
label_path = target_path+"\\labels"
json_path = r"D:\104.식물 병 유발 통합 데이터\1.Training\라벨링데이터\TL1_고추"

sheet_name = os.listdir(image_path)

for folder in sheet_name:
    image_list = os.listdir(image_path+"\\"+folder)
    for image in image_list:
        print(image)
        file_name = image.split(".")[0]
        file_name += ".json"
        with open(f"{json_path}\\{folder}\\{file_name}", "r") as json_file:
            json_data = json.load(json_file)
            json.dumps(json_data, indent="/t")
            # print(json_data)

            code = json_data["annotations"]["disease"]

            if code == "a7":
                code = 0
            elif code == "a8":
                code = 1
            elif code == "b3":
                code = 2
            elif code == "b6":
                code = 3
            elif code == "b7":
                code = 4
            elif code == "b8":
                code = 5
            elif code == "c7":
                code = 6

            # 질병 코드 변환 넣기
            img_width = json_data["description"]["width"]
            img_height = json_data["description"]["height"]

            # print(position)
            positions = json_data["annotations"]["part"]
            text = ""
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

                f = open(label_path+"\\"+folder+"\\" + file_path, "w")
                f.write(text)
                f.close()



