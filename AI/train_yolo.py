from ultralytics import YOLO

# Load a model
# yolo V8 Nano : 가장 가벼운 버전
model = YOLO("yolov8n.yaml")  # build a new model from scratch
# yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
# Use the model
results = model.train(data="config.yaml", epochs=12, imgsz=416)  # train the model

# results = model.predict(source='data/', save=True)
