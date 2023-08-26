import json
import sys, os
import cv2

from PIL import Image
import numpy as np
import pandas as pd

np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)

path = r"/data"
folder_path = path+r"\labels"
folders = os.listdir(folder_path) #os.listdir()
print(folders)

def json_to_yolo():
    for file in folders:
        try:
            with open(f"{folder_path}\\{file}", "r") as json_file:
                json_data = json.load(json_file)

                json.dumps(json_data, indent="/t")
                # print(json_data)

                img_width = json_data["description"]["width"]
                img_height = json_data["description"]["height"]

                # ---------------- 1
                # position = json_data["annotations"]["points"][0]
                # # print(position)
                #
                # target_width = position["xbr"]
                # target_height = position["ybr"]
                # x_center = position["xtl"]+(target_width/2)
                # y_center = position["ytl"]+(target_height/2)

                # ---------------- 2
                position = json_data["annotations"]["bbox"][0]
                # print(position)

                target_width = position["w"]
                target_height = position["h"]
                x_center = position["x"]+(target_width/2)
                y_center = position["y"]+(target_height/2)

                target_width_normalized = f"{(target_width/img_width):.6f}"
                target_height_normalized = f"{(target_height/img_height):.6f}"
                x_center_normalized = f"{(x_center/img_width):.6f}"
                y_center_normalized = f"{(y_center/img_height):.6f}"

                data = f"15 {x_center_normalized} {y_center_normalized} {target_width_normalized} {target_height_normalized}"
                file_path = file.split(".")[0]
                file_path += ".txt"

                f = open(folder_path+"\\"+file_path, "w")
                f.write(data)
                f.close()
        except:
            pass



json_to_yolo()

# image = cv2.imread("619627_20211026_1_1_a2_3_2_12_1_53.jpg")
# image_vector = image.reshape(json_data["description"]["height"], , 3)
#
# image_vector = image_vector[int(position["y"]):int(position["y"]+position["h"]), int(position["x"]):int(position["x"]+position["w"])]
# print(image_vector.shape)
# img = cv2.resize(image_vector, (512, 512))
# img = Image.fromarray(img)
# img.show()

# chr(1)