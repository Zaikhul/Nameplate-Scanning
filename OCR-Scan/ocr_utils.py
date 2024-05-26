import pytesseract
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def is_valid_text(text):
    return text.strip() != ''

def perform_ocr(image):
    try:
        img_np = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        ocr_result = pytesseract.image_to_string(img)
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        return ocr_result, ocr_data
    except Exception as e:
        logger.error(f"Error during OCR: {e}")
        raise

def async_ocr_task(image):
    try:
        ocr_result, ocr_data = perform_ocr(image)
        boxes = []
        for i in range(len(ocr_data['text'])):
            if is_valid_text(ocr_data['text'][i]):
                (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                boxes.append((x, y, w, h))
        return {'result': ocr_result if is_valid_text(ocr_result) else 'No valid text detected', 'boxes': boxes}
    except Exception as e:
        logger.error(f"Error during OCR task: {e}")
        raise
