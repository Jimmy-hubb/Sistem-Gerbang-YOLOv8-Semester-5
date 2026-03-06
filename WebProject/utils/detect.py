# utils/detect.py
# VERSI FINAL — Super Akurat untuk Indonesia (Mobil + Motor + Truk + Bus)

from ultralytics import YOLO
import cv2

# Load model sekali saja (otomatis download kalau belum ada)
# yolov8s.pt = akurat + cepat (rekomendasi terbaik untuk ANPR)
model = YOLO("yolov8s.pt")

def detect_vehicle(img):
    """
    Deteksi SEMUA kendaraan bermotor:
    - Mobil (car)        → class 2
    - Motor (motorcycle) → class 3
    - Bus                → class 5
    - Truk               → class 7
    """
    if img is None or img.size == 0:
        print("[DETECT] Gambar kosong atau rusak!")
        return []

    # Resize gambar kalau terlalu besar (biar lebih cepat & akurat)
    height, width = img.shape[:2]
    if width > 1280:
        new_width = 1280
        new_height = int(height * (1280 / width))
        img = cv2.resize(img, (new_width, new_height))
        print(f"[DETECT] Gambar di-resize ke {new_width}x{new_height}")

    # Deteksi dengan setting terbaik untuk ANPR Indonesia
    results = model(
        img,
        conf=0.25,      # lebih sensitif (turunin dari 0.4)
        iou=0.45,       # hindari duplikat
        classes=[2, 3, 5, 7],  # HANYA kendaraan bermotor
        verbose=False
    )[0]

    boxes = []
    print(f"[DETECT] Total objek terdeteksi: {len(results.boxes) if results.boxes is not None else 0}")

    if results.boxes is not None:
        for i, box in enumerate(results.boxes):
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            class_name = {2: "Mobil", 3: "Motor", 5: "Bus", 7: "Truk"}.get(cls_id, "Lainnya")
            print(f"[DETECT] Kendaraan #{i+1} → {class_name} | Conf: {conf:.2f} | Box: ({x1},{y1},{x2},{y2})")

            # Filter hanya kendaraan yang cukup besar (hindari deteksi kecil2)
            area = (x2 - x1) * (y2 - y1)
            if area > 5000:  # minimal area kotak (bisa diatur)
                boxes.append((x1, y1, x2, y2))
            else:
                print(f"[DETECT] Skip: kendaraan terlalu kecil (area={area})")

    if len(boxes) == 0:
        print("[DETECT] TIDAK ADA KENDARAAN YANG LAYAK TERDETEKSI!")
        print("[DETECT] Tips: Gunakan foto dari depan/belakang, cahaya terang, plat terlihat jelas!")

    else:
        print(f"[DETECT] SUKSES! {len(boxes)} kendaraan siap dibaca platnya!")

    return boxes