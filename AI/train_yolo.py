from ultralytics import YOLO

# Load a model
# yolo V8 Nano : 가장 가벼운 버전
model = YOLO(r"D:\CropFairy\AI\runs\detect\train\weights\last.pt")  # build a new model from scratch
# yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
# Use the model
results = model.train(data="config.yaml", epochs=20)  # train the model
# results = model.val()


# model = YOLO('yolov8x.yaml').load('yolov8x.pt') # build from YAML and transfer weights
# model.train(data="/image_datasets/Website_Screenshots.v1-raw.yolov8/data.yaml", epochs=1)

# model = YOLO('yolov8x.yaml').load('yolov8x.pt')
# results = model.predict(source='data/', save=True)
# model.val()
# print(results)