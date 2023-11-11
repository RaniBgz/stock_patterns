from ultralytics import YOLO

yaml_path = "/datasets/3p_1k5_custom/data_config.yaml"

# Load a model
model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data=yaml_path, epochs=90, imgsz=1280, batch=-1, patience=15)  # train the model
metrics = model.val()  # evaluate model performance on the validation set
# path = model.export(format="onnx")  # export the model to ONNX format