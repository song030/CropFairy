import random
import sys, os
import shutil
import numpy as np

np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)

search_path = r"D:\104.식물 병 유발 통합 데이터\1.Training\원천데이터\오이"
kind = "병해"
move_path = r"D:\CropFairy\AI\cucumber\images\train2"
folder_path = f"{search_path}\\{kind}"
targets = os.listdir(folder_path)

# move_image = {"b1": {11: {3: [1, 2, 3]}}
move_image = {"a4":{11:{3:[1,2,3]}}}

move_count = [120, 300, 400]
move_num = 0

for disease in move_image.keys():
    for grow in move_image[disease].keys():
        for area in move_image[disease][grow].keys():
            for risk in move_image[disease][grow][area]:
                print(f"------------------4_1_{disease}_{area}_2_{grow}_{risk}")
                image_list = list()
                for target in targets:
                    if f"4_1_{disease}_{area}_2_{grow}_{risk}" in target:
                        image_list.append(target)

                print(f"image count : {len(image_list)}")
                goal_count = move_count[move_num]
                gap = goal_count // len(image_list)
                if gap == 0:
                    gap = 1

                random.shuffle(image_list)
                idx = 0
                mv_cnt = 0
                temp_list = image_list.copy()
                while goal_count != mv_cnt:
                    # print(idx, len(temp_list[idx]))
                    image = temp_list[idx]
                    print(image)
                    shutil.move(folder_path + "\\" + image, move_path + "\\" + image)
                    idx += gap
                    mv_cnt += 1

                move_num += 1
