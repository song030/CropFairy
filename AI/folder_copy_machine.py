import shutil
import json
import os
import bbox_to_coco
# origin_path = r"C:\Users\kdt111\Downloads\166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터\01.데이터\2.Validation\라벨링데이터\경구약제조합 5000종"
# origin_path = r"C:\Users\kdt111\Downloads\166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터\01.데이터\2.Validation\K-000059_json"
# slash = "\\"
# path_to_copy = r"C:\Users\kdt111\Desktop\project_YOLOv8\data\orgin" + slash
# drug_name_list = list()
# folder_list = os.listdir(origin_path)
# for folder in folder_list:
    # if folder.endswith("json"):
    #     last_path = origin_path + slash + folder
    #     elements_folder = os.listdir(last_path)
    #     for fd in elements_folder:
    #         final_path = last_path + slash + fd
    #         json_list = os.listdir(final_path)
    #         for j in json_list:

                # print(final_path+j)
                # drug_num = bbox_to_coco.convert_to_coco(j, final_path+slash)
                # if str(drug_num) not in drug_name_list:
                #     drug_name_list.append(f"{drug_num}")
# for folder in folder_list:
#         bbox_to_coco.convert_to_coco(folder, origin_path+slash)
        # if str(drug_num) not in drug_name_list:
        #     drug_name_list.append(f"{drug_num}")
# with open(r"drug_num_list.txt", 'w', encoding='utf-8') as file:
#     file.write("\n".join(drug_name_list))
import json
import os
import bbox_to_coco
# origin_path = r"C:\Users\kdt111\Downloads\166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터\01.데이터\2.Validation\원천데이터\경구약제조합 5000종"
origin_path = r"C:\Users\kdt111\Downloads\166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터\01.데이터\2.Validation\K-000059"
slash = "\\"
path_to_copy = r"C:\Users\kdt111\Desktop\project_YOLOv8\data\images\train"
compare_file_list = os.listdir(r"C:\Users\kdt111\Desktop\project_YOLOv8\data\labels\train")
filtered_file_list = list()

for i in compare_file_list:
    filtered_file_list.append(i[:-4])


folder_list = os.listdir(origin_path)
for folder in folder_list:
        depth_1 = origin_path+slash
        shutil.copyfile(depth_1+folder, path_to_copy + slash + folder)
    # if not folder.endswith("zip"):
    #     depth_1 = origin_path+slash
    #     folder_2 = os.listdir(depth_1+folder)
    #     for fd in folder_2:
    #         if "index" not in fd:
    #             if fd[:-4] in filtered_file_list:
    #                 last_copy = depth_1+folder+slash+fd
    #                 # print(depth_1+folder+slash+fd)
    #                 shutil.copyfile(last_copy, path_to_copy+slash+fd)

