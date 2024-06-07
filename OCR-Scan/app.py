# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
from utils.logger import logger
from utils.ocr_engine import OCREngine
from utils.data_fetcher import fetch_data, post_record
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ocr_engine = OCREngine()

class APIException(Exception):
    def __init__(self, message, status_code, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/ocr_request', methods=['POST'])
def handle_ocr_request():
    """Handles OCR request received from client."""
    try:
        if 'image' not in request.files:
            raise APIException("Missing 'image' file in request", 400)
        
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        
        image_bytes = image_file.read()
        image = Image.open(BytesIO(image_bytes))

        result = ocr_engine.perform_ocr(image_bytes)

        room_url = os.getenv('ROOM_URL')
        if not room_url:
            raise APIException("ROOM_URL environment variable not set", 500)

        field = str(result.get('text', ''))
        post_record(room_url, field, image_bytes)

        return jsonify(result)
    except APIException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise APIException("Internal server error", 500)

@app.route('/process-ocr', methods=['POST'])
def process_ocr():
    try:
        if 'image' not in request.files:
            logger.error("No image provided in request")
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        engine = request.form.get('engine', 'tesseract')
        
        logger.info(f"Processing image with engine: {engine}")

        result = ocr_engine.perform_ocr(image.read())
        
        logger.info(f"OCR result: {result}")

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing OCR request: {e}", exc_info=True)
        return jsonify({'error': f"Error processing OCR request: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
