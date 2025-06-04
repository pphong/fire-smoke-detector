from ultralytics import YOLO

model_folder = "models"
mymodel = f"../{model_folder}/best_model_v8/best_v8.pt"
model = YOLO(mymodel)

exported = model.export(format="ncnn")