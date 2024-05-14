from flask import Flask, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
from PIL import Image
import base64
import io
import os
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'

# Path to the Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Initialize ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=4)

# Function to preprocess the image
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    alpha = 2.0  # Contrast control
    beta = 50  # Brightness control
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Denoising
    denoised = cv2.fastNlMeansDenoising(adjusted, None, 30, 7, 21)

    # Thresholding
    _, thresh = cv2.threshold(denoised, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

# Function to perform OCR on the image
def perform_ocr(image):
    preprocessed_img = preprocess_image(image)
    ocr_config = '--psm 7 --oem 3'  # Configure Tesseract for better nameplate recognition
    ocr_result = pytesseract.image_to_string(preprocessed_img, config=ocr_config)
    return ocr_result

# Function to validate if the result contains text
def is_valid_text(text):
    # Check if text contains alphanumeric characters
    return any(char.isalnum() for char in text)

# Asynchronous OCR task
def async_ocr_task(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform OCR on the image
        ocr_result = perform_ocr(image)

        # Validate the OCR result
        if is_valid_text(ocr_result):
            return {'result': ocr_result}
        else:
            return {'result': 'No valid text detected'}
    except Exception as e:
        error_message = f"Error during OCR: {e}"
        print(error_message)
        return {'result': error_message}

# Handling CORS manually for WebSocket
@socketio.on('ocr_request')
def handle_ocr_request(data):
    try:
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # Run OCR in a separate thread
        future = executor.submit(async_ocr_task, image_bytes)
        result = future.result()

        emit('ocr_result', result)
    except Exception as e:
        error_message = f"Error during OCR: {e}"
        print(error_message)
        emit('ocr_result', {'result': error_message})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
