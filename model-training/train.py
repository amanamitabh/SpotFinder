import ultralytics
from ultralytics import YOLO
import torch

def main():
    device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"Training on: {torch.cuda.get_device_name(0) if device == 0 else 'CPU'}")

    # Load YOLOv8 nano model with pretrained weights
    model = YOLO("yolov8n.pt")

    # Training the model
    results = model.train(
        data="dataset/data.yaml",   # Add the relative path to YAML file of dataset here
        epochs=30,
        imgsz=640,
        batch=16,
        name="yolov8n-parking-detect",
        optimizer="AdamW",
        mosaic=0.5,
        hsv_h=0.05,        
        hsv_s=0.7,         
        hsv_v=0.5,         
        device=device
    )

    # Display model metrics once training is completed
    metrics = model.val()
    print(metrics)


if __name__ == '__main__':
    main()