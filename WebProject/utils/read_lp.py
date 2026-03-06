import easyocr
import cv2

reader = easyocr.Reader(['en'], download_enabled=True)

def read_plate(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = reader.readtext(img_gray, detail=0)
    return result[0] if result else "(Tidak Terbaca)"
