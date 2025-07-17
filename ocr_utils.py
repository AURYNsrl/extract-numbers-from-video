import pytesseract
import re
import cv2

def extract_numbers_from_roi(roi_image):
    """
    Applica thresholding e OCR per estrarre numeri da un'immagine (ROI).
    """
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=config)
    numbers = re.findall(r'\d+', text)
    return numbers
