import json
import sys, os

import numpy as np
import pandas as pd

np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)

path = r"D:\104.식물 병 유발 통합 데이터\1.Training\라벨링데이터"
kind = "TL5_토마토"
folder_path = f"{path}\\{kind}"
targets = os.listdir(folder_path)

for target in targets:
    print("------------------ "+target)
    folder_path = f"{path}\\{kind}\\{target}"
    files = os.listdir(folder_path)


    # 고추
    image_data = pd.DataFrame(columns = ["image", "width", "height", "crop", "area", "grow", "disease", "risk", "bbox", "part"])

    row = 0
    for file in files:
        with open(f"{folder_path}\\{file}", "r") as json_file:
            try:
                json_data = json.load(json_file)

                json.dumps(json_data, indent="/t")
                print(json_data)
                description = json_data['description']
                annotations = json_data['annotations']
                annotations: dict
                if "part" in annotations.keys():
                    image_data.loc[row] = [description["image"], description["width"], description["height"],
                                           annotations["crop"], annotations["area"], annotations["grow"],
                                           annotations["disease"], annotations["risk"],
                                           annotations["bbox"], annotations["part"]]
                else:
                    image_data.loc[row] = [description["image"], description["width"], description["height"],
                                           annotations["crop"], annotations["area"], annotations["grow"],
                                           annotations["disease"], annotations["risk"],
                                           annotations["bbox"], annotations["points"]]
            except:
                print(file)
                image_data.loc[row] = [file, "file_error", "", "", "", "", "", "", "", ""]

            print(row)
            row += 1

    print(image_data)
    with pd.ExcelWriter('토마토.xlsx', mode='a', engine='openpyxl') as writer:
        image_data.to_excel(excel_writer=writer, sheet_name=target)
