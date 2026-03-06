# utils/ocr.py

import pytesseract
import cv2

# Path Tesseract (sesuaikan kalau beda)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_text(image):
    """
    Terima gambar crop plat nomor (numpy array), langsung return teks
    Ini yang dipanggil dari app.py
    """
    if image is None or image.size == 0:
        return "(tidak terbaca)"

    # Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Konfigurasi OCR khusus plat nomor
    config = "--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    text = pytesseract.image_to_string(thresh, config=config)
    cleaned = text.strip().replace(" ", "").upper()

    # Filter hanya huruf & angka
    import re
    cleaned = re.sub(r'[^A-Z0-9]', '', cleaned)

    return cleaned if cleaned else "(tidak terbaca)"