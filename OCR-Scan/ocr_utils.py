import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import logging
import os
from typing import Tuple, List, Dict

# Set Tesseract environment variables from configuration
TESSDATA_PREFIX = os.getenv('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/4.00/tessdata')
TESSERACT_CMD = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
os.environ['TESSDATA_PREFIX'] = TESSDATA_PREFIX

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_image(img: np.ndarray) -> np.ndarray:
    """Preprocess the image for better OCR accuracy."""
    logger.info("Preprocessing image")
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adjusted = cv2.convertScaleAbs(gray, alpha=1.5, beta=50)
        denoised = cv2.fastNlMeansDenoising(adjusted, None, 40, 7, 21)
        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return thresh
    except cv2.error as e:
        logger.error(f"OpenCV error in image preprocessing: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in image preprocessing: {e}")
        raise

def perform_ocr(image: np.ndarray) -> Tuple[str, Dict]:
    """Perform OCR on the preprocessed image."""
    logger.info("Performing OCR")
    try:
        preprocessed_img = preprocess_image(image)
        ocr_config = '--psm 7 --oem 3'
        ocr_result = pytesseract.image_to_string(preprocessed_img, config=ocr_config)
        data = pytesseract.image_to_data(preprocessed_img, config=ocr_config, output_type=pytesseract.Output.DICT)
        return ocr_result.strip(), data
    except pytesseract.TesseractError as e:
        logger.error(f"Tesseract error during OCR: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during OCR: {e}")
        raise

def is_valid_text(text: str) -> bool:
    """Check if the text is valid (contains alphanumeric characters)."""
    return any(char.isalnum() for char in text)

def async_ocr_task(image_bytes: bytes) -> Dict:
    """Asynchronous task for performing OCR."""
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
        logger.error(f"Error during OCR task: {e}")
        return {'result': 'Error processing image', 'boxes': []}



import unittest
from unittest.mock import MagicMock, patch, call
import base64
import io
import numpy as np
from PIL import Image
from app import handle_ocr_request, app, socketio
from ocr_utils import preprocess_image, perform_ocr, is_valid_text, async_ocr_task

"""unit testing."""
class OCRUtilsTests(unittest.TestCase):

    def setUp(self):
        # Sample image setup
        self.sample_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.sample_image_bytes = io.BytesIO()
        Image.fromarray(self.sample_image).save(self.sample_image_bytes, format='PNG')
        self.sample_image_bytes = self.sample_image_bytes.getvalue()

    @patch('cv2.cvtColor')
    @patch('cv2.convertScaleAbs')
    @patch('cv2.fastNlMeansDenoising')
    @patch('cv2.adaptiveThreshold')
    def test_preprocess_image(self, mock_threshold, mock_denoise, mock_scale, mock_cvtcolor):
        mock_cvtcolor.return_value = self.sample_image
        mock_scale.return_value = self.sample_image
        mock_denoise.return_value = self.sample_image
        mock_threshold.return_value = self.sample_image

        processed_img = preprocess_image(self.sample_image)

        mock_cvtcolor.assert_called_once()
        mock_scale.assert_called_once()
        mock_denoise.assert_called_once()
        mock_threshold.assert_called_once()
        self.assertIsInstance(processed_img, np.ndarray)

    @patch('pytesseract.image_to_string')
    @patch('pytesseract.image_to_data')
    def test_perform_ocr(self, mock_image_to_data, mock_image_to_string):
        mock_image_to_string.return_value = "Test OCR"
        mock_image_to_data.return_value = {'text': ["Test OCR"], 'left': [10], 'top': [20], 'width': [30], 'height': [40]}

        result, data = perform_ocr(self.sample_image)

        self.assertEqual(result, "Test OCR")
        self.assertIn('text', data)
        mock_image_to_string.assert_called_once()
        mock_image_to_data.assert_called_once()

    def test_is_valid_text(self):
        self.assertTrue(is_valid_text("Test123"))
        self.assertFalse(is_valid_text(" "))

    @patch('ocr_utils.perform_ocr')
    def test_async_ocr_task(self, mock_perform_ocr):
        mock_perform_ocr.return_value = ("Test OCR", {'text': ["Test OCR"], 'left': [10], 'top': [20], 'width': [30], 'height': [40]})

        result = async_ocr_task(self.sample_image_bytes)

        self.assertIn('result', result)
        self.assertIn('boxes', result)
        mock_perform_ocr.assert_called_once()


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.async_ocr_task')
    @patch('app.executor.submit')
    def test_handle_ocr_request_success(self, mock_submit, mock_async_ocr_task):
        mock_future = MagicMock()
        mock_submit.return_value = mock_future
        mock_future.result.return_value = {'result': 'Test OCR', 'boxes': []}

        image_data = base64.b64encode(self.sample_image_bytes).decode('utf-8')
        data = {'image': f'data:image/png;base64,{image_data}'}

        handle_ocr_request(data)

        mock_submit.assert_called_once_with(mock_async_ocr_task, self.sample_image_bytes)
        mock_future.result.assert_called_once()

    @patch('app.executor.submit')
    def test_handle_ocr_request_keyerror(self, mock_submit):
        data = {'wrong_key': 'data:image/png;base64,...'}

        with patch('flask_socketio.SocketIO.emit') as mock_emit:
            handle_ocr_request(data)
            mock_emit.assert_called_once_with('ocr_result', {'result': 'Invalid data format', 'boxes': []})
            mock_submit.assert_not_called()

    @patch('app.executor.submit')
    def test_handle_ocr_request_exception(self, mock_submit):
        mock_submit.side_effect = Exception("Test Exception")
        image_data = base64.b64encode(self.sample_image_bytes).decode('utf-8')
        data = {'image': f'data:image/png;base64,{image_data}'}

        with patch('flask_socketio.SocketIO.emit') as mock_emit:
            handle_ocr_request(data)
            mock_emit.assert_called_once_with('ocr_result', {'result': 'Test Exception', 'boxes': []})


if __name__ == '__main__':
    unittest.main()