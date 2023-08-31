from ultralytics import YOLO
import time

start = time.time()
model = YOLO(r"D:\CropFairy\model\tomato_best.pt")  # build a new model from scratch
print("model load :", time.time()-start)
start = time.time()

results = model.predict(source=r'D:\CropFairy\AI\tomato\images\test\638394_20211024_2_1_a5_3_2_12_2_181.jpg', save=True)
print("predict :", time.time()-start)
start = time.time()

for result in results:
    if result.boxes:
        box = result.boxes[0]
        class_id = int(box.cls)
        object_name = model.names[class_id]
        confidence = float(box.conf)
        print(object_name, confidence)

print("complete : ", time.time()-start)
