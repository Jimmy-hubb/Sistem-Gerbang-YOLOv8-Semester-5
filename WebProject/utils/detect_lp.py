from ultralytics import YOLO
import cv2

model = YOLO("models/best.pt")
print("MODEL NAMES:", model.names)

def detect_license_plate(img):
    # PREPROCESS: perbesar agar plat kecil terlihat
    enhanced = cv2.resize(img, (0,0), fx=2.0, fy=2.0)
    enhanced = cv2.GaussianBlur(enhanced, (3,3), 0)
    enhanced = cv2.convertScaleAbs(enhanced, alpha=1.3, beta=15)

    # YOLO inference
    results = model.predict(
        source=enhanced,
        conf=0.05,
        imgsz=1280,
        verbose=True
    )[0]

    crops = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = enhanced[y1:y2, x1:x2]
        if crop.size > 0:
            crops.append(crop)

    return crops
