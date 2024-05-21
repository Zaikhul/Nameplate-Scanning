from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
from PIL import Image
import base64
import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
logging.basicConfig(level=logging.INFO)

# Set Tesseract environment variables
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
executor = ThreadPoolExecutor(max_workers=4)  # Limit to 4 workers for safety

def preprocess_image(img):
    logging.info("Preprocessing image")
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adjusted = cv2.convertScaleAbs(gray, alpha=1.5, beta=50)
        denoised = cv2.fastNlMeansDenoising(adjusted, None, 40, 7, 21)
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return thresh
    except Exception as e:
        logging.error(f"Error in image preprocessing: {e}")
        raise

def perform_ocr(image):
    logging.info("Performing OCR")
    try:
        preprocessed_img = preprocess_image(image)
        ocr_config = '--psm 7 --oem 3'
        ocr_result = pytesseract.image_to_string(preprocessed_img, config=ocr_config)
        data = pytesseract.image_to_data(preprocessed_img, config=ocr_config, output_type=pytesseract.Output.DICT)
        return ocr_result.strip(), data
    except Exception as e:
        logging.error(f"Error during OCR: {e}")
        raise

def is_valid_text(text):
    return any(char.isalnum() for char in text)

def async_ocr_task(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = np.array(image)
        if image.ndim == 2:  # grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        ocr_result, ocr_data = perform_ocr(image)
        boxes = []
        for i in range(len(ocr_data['text'])):
            if is_valid_text(ocr_data['text'][i]):
                (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                boxes.append((x, y, w, h))
        return {'result': ocr_result if is_valid_text(ocr_result) else 'No valid text detected', 'boxes': boxes}
    except Exception as e:
        logging.error(f"Error during OCR task: {e}")
        return {'result': 'Error processing image', 'boxes': []}

@socketio.on('ocr_request')
def handle_ocr_request(data):
    try:
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        future = executor.submit(async_ocr_task, image_bytes)
        result = future.result()
        emit('ocr_result', result)
    except Exception as e:
        logging.error(f"Error handling OCR request: {e}")
        emit('ocr_result', {'result': str(e), 'boxes': []})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
