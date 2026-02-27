from ultralytics import YOLO
import supervision as sv
import cv2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEBUG = os.getenv("DEBUG")

# Get the absolute path of weights and image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(BASE_DIR, "model.pt")
IMAGE_PATH = os.path.join(BASE_DIR, "image.jpg")

# Load the model weights
model = YOLO(WEIGHTS_PATH)

def annotate_result(result):
    if int(DEBUG) == 1:
        # Convert YOLO result to supervision detections
        detections = sv.Detections.from_ultralytics(result)

        # Create labels
        labels = [
            f"{result.names[int(cls)]} {conf:.2f}"
            for cls, conf in zip(detections.class_id, detections.confidence)
        ]

        image = cv2.imread(IMAGE_PATH)

        # Create Annotator objects
        label_annotator = sv.LabelAnnotator()
        box_annotator = sv.BoxAnnotator()

        annotated_image = box_annotator.annotate(
            scene=image,
            detections=detections
        )

        annotated_image = label_annotator.annotate(
            scene=annotated_image,
            detections=detections,
            labels=labels
        )

        # Save annotated image
        output_path = os.path.join(BASE_DIR, "annotated_img.jpg")
        cv2.imwrite(output_path, annotated_image)


def predict():
    vac_count = 0
    occ_count = 0

    result = model.predict(source=IMAGE_PATH, conf=0.5)

    # Find counts of each class
    for box in result[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name == "vacant":
            vac_count += 1
        
        elif class_name == "occupied":
            occ_count += 1

    # Extract inference time
    inf_time = result[0].speed["inference"]

    # Performs annotation only in debug mode
    annotate_result(result[0])    

    # Return detection result as a dictionary
    return {"vacant" : vac_count, "occupied": occ_count, "inference_time_ms": round(inf_time, 2)}