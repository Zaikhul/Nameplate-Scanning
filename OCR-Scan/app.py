# app.py (backend)
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# Function to preprocess the image
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return adaptive_thresh

# Function to perform OCR on the image
def perform_ocr(image):
    preprocessed_img = preprocess_image(image)
    
    # Perform OCR using Tesseract
    ocr_result = pytesseract.image_to_string(preprocessed_img)
    
    return ocr_result

# Handling CORS manually for WebSocket
@socketio.on('ocr_request')
def handle_ocr_request(data):
    try:
        # Receiving image data from the client and decoding it
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform OCR on the image
        ocr_result = perform_ocr(image)

        # Sending the OCR result back to the client
        emit('ocr_result', {'result': ocr_result})
    except Exception as e:
        error_message = "Error during OCR: {}".format(e)
        print(error_message)
        emit('ocr_result', {'result': error_message})
        return

if __name__ == '__main__':
    socketio.run(app)
