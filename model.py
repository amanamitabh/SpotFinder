from roboflow import Roboflow
import supervision as sv
import cv2
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')

rf = Roboflow(api_key= API_KEY)
project = rf.workspace().project("parking-space-1srdb")
model = project.version(4).model


def predict():
    result = model.predict("image.jpg", confidence=60).json()
    labels = [item["class"] for item in result["predictions"]]

    detections = sv.Detections.from_inference(result)

    label_annotator = sv.LabelAnnotator()
    mask_annotator = sv.MaskAnnotator()

    image = cv2.imread("image.jpg")

    annotated_image = mask_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)

    cv2.imwrite("annotated_img.jpg", annotated_image)
    vacant_count = sum(1 for item in result["predictions"] if item.get("class") == "vacant")
    occ_count = sum(1 for item in result["predictions"] if item.get("class") == "occupied")
    return {"vacant" : vacant_count, "occupied": occ_count}
