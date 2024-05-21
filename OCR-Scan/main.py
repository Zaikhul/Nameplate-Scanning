# # app.py
# from flask import Flask
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import cv2
# import pytesseract
# import numpy as np
# from PIL import Image
# import base64
# import io

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
# socketio = SocketIO(app, cors_allowed_origins="*")

# # Function to preprocess the image
# def preprocess_image(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5,5), 0)
#     adaptive_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
#     return adaptive_thresh

# # Function to perform OCR on the image
# def perform_ocr(image):
#     preprocessed_img = preprocess_image(image)
    
#     # Perform OCR using Tesseract
#     ocr_result = pytesseract.image_to_string(preprocessed_img)
    
#     return ocr_result

# # Handling CORS manually for WebSocket
# @socketio.on('ocr_request')
# def handle_ocr_request(data):
#     try:
#         # Receiving image data from the client and decoding it
#         image_data = data['image'].split(',')[1]
#         image_bytes = base64.b64decode(image_data)
#         image = Image.open(io.BytesIO(image_bytes))
#         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#         # Perform OCR on the image
#         ocr_result = perform_ocr(image)

#         # Sending the OCR result back to the client
#         emit('ocr_result', {'result': ocr_result})
#     except Exception as e:
#         error_message = "Error during OCR: {}".format(e)
#         print(error_message)
#         emit('ocr_result', {'result': error_message})

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000)


# ====================================================================
# from flask import Flask, Response
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
# import cv2
# import numpy as np
# from PIL import Image
# import base64
# import io
# from paddleocr import PaddleOCR

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# # Initialize PaddleOCR with adjusted parameters
# ocr = PaddleOCR(
#     use_angle_cls=False,  # Disable angle classification
#     lang='en',
#     det_db_thresh=0.5,  # Adjust threshold for detection
#     rec_batch_num=1,  # Adjust batch size for recognition
#     use_gpu=False,  # Ensure GPU is not used
#     det_algorithm='DB',  # Using DB algorithm for detection
#     rec_algorithm='CRNN'  # Using CRNN algorithm for recognition
# )

# # Function to preprocess the image
# def preprocess_image(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     alpha = 2.0  # Contrast control
#     beta = 50  # Brightness control
#     adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
#     denoised = cv2.fastNlMeansDenoising(adjusted, None, 30, 7, 21)
#     _, thresh = cv2.threshold(denoised, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return thresh

# # Function to perform OCR on the image
# def perform_ocr(image):
#     try:
#         preprocessed_img = preprocess_image(image)
#         pil_image = Image.fromarray(preprocessed_img)
#         result = ocr.ocr(np.array(pil_image), cls=False)  # Disable classification
#         text_result = ' '.join([line[1][0] for line in result[0]])
#         return text_result
#     except Exception as e:
#         print(f"Error during OCR: {e}")
#         return "OCR Error"

# # Handling CORS manually for WebSocket
# @socketio.on('ocr_request')
# def handle_ocr_request(data):
#     try:
#         image_data = data['image'].split(',')[1]
#         image_bytes = base64.b64decode(image_data)
#         image = Image.open(io.BytesIO(image_bytes))
#         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

#         ocr_result = perform_ocr(image)

#         emit('ocr_result', {'result': ocr_result})
#     except Exception as e:
#         error_message = f"Error during OCR: {e}"
#         print(error_message)
#         emit('ocr_result', {'result': error_message})

# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000)


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

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'

# Path to the Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function convolution matriks
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
        image = cv2.resize(image, (int(width * scaling_factor), int(height * scaling_factor)))
    
    rgb2gray_kernel = np.array([[0.2989, 0.5870, 0.1140]])
    gray_image = convolve_image(image, rgb2gray_kernel)
    gray = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)
    # Increase contrast and sharpness
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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
