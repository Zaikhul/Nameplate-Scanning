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

def convolve_image(image, kernel):
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]
    pad = (kW - 1) // 2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    output = np.zeros((iH, iW), dtype="float32")
    
    for y in range(pad, iH + pad):
        for x in range(pad, iW + pad):
            roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]
            k = (roi * kernel).sum()
            output[y - pad, x - pad] = k

    output = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)
    output = np.uint8(output)
    
    return output

# Function to preprocess the image
def preprocess_image(img):

    max_dimension = 1024
    height, width = img.shape[:2]
    if max(height, width) > max_dimension:
        scaling_factor = max_dimension / float(max(height, width))
        image = cv2.resize(img, (int(width * scaling_factor), int(height * scaling_factor)))
    
    rgb2gray_kernel = np.array([[0.2989, 0.5870, 0.1140]])
    gray_image = convolve_image(image, rgb2gray_kernel)

    gray = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    # Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    return blurred_image

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
