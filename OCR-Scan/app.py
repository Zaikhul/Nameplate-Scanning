import logging
import os
import base64
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import traceback
from ocr_utils import async_ocr_task
from logger_config import logger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

executor = ThreadPoolExecutor(max_workers=4)

@socketio.on('ocr_request')
def handle_ocr_request(data: dict) -> None:
    """Handles OCR request received from client."""
    try:
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        future = executor.submit(async_ocr_task, image_bytes)
        result = future.result()
        emit('ocr_result', result)
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        emit('ocr_result', {'result': 'Invalid data format', 'boxes': []})
    except (KeyError, ValueError) as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        emit('ocr_result', {'result': str(e), 'boxes': []})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
