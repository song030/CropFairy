import random
import sys, os
import shutil
import numpy as np

target_path = "D:\CropFairy\AI\data\고추"
json_path = r"D:\CropFairy\AI\data"

label_folder = os.listdir(target_path+"\\labels")
for folders in label_folder:
    print(folders)
    file_list = os.listdir(target_path+"\\labels\\"+folders)
    random.shuffle(file_list)
    total_size = len(file_list)
    train_size = total_size//10*9
    test_size = total_size-train_size
    print(train_size, test_size)

    for idx in range(train_size):
        file = file_list[idx]
        shutil.move(target_path+"\\labels\\"+folders+"\\"+ file, json_path+r"\labels\train"+"\\"+file)
        img_name = file.split(".")[0]
        img_name += ".jpg"
        shutil.move(target_path+"\\images\\"+folders+"\\"+img_name, json_path+r"\images\train"+"\\"+img_name)

    for idx in range(train_size, total_size):
        file = file_list[idx]
        shutil.move(target_path+"\\labels\\"+folders+"\\" + file, json_path+r"\labels\test"+"\\"+file)
        img_name = file.split(".")[0]
        img_name += ".jpg"
        shutil.move(target_path+"\\images\\"+folders+"\\"+img_name, json_path+r"\images\test"+"\\"+img_name)



