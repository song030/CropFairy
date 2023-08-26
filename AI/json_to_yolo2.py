import random
import sys, os
import shutil
import numpy as np

np.set_printoptions(linewidth=np.inf, threshold=sys.maxsize)

search_path = r"D:\104.식물 병 유발 통합 데이터\1.Training\원천데이터\고추"
kind = "생리장해"
move_path = r"D:\CropFairy\AI\data\고추\images"+"\\"+kind
folder_path = f"{search_path}\\{kind}"
targets = os.listdir(folder_path)

# move_image = {12: {3:[1]}, 13:{3:[1]}}
move_image = {"b6":{13:{3:[3]}}, "b7":{11:{3:[1]}, 12:{3:[1]}}}
move_count = [401, 500, 500]
move_num = 0

for disease in move_image.keys():
    for grow in move_image[disease].keys():
        for area in move_image[disease][grow].keys():
            for risk in move_image[disease][grow][area]:
                print(f"------------------ 5_2_{disease}_{area}_2_{grow}_{risk}")
                image_list = list()
                for target in targets:
                    if f"5_2_{disease}_{area}_2_{grow}_{risk}" in target:
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



