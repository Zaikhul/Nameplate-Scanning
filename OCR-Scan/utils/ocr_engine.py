import cv2
import pytesseract
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
from io import BytesIO
from utils.logger import logger
import os

class OCREngine:
    def __init__(self, engine_type='tesseract', use_gpu=False):
        self.engine_type = engine_type
        if engine_type == 'paddle':
            self.engine = PaddleOCR(lang="en", ocr_version="PP-OCRv4", show_log=False, use_gpu=use_gpu)
        elif engine_type == 'tesseract':
            self.engine = pytesseract
        else:
            raise ValueError("Unsupported OCR engine type")

    def perform_ocr(self, image: bytes) -> dict:
        if self.engine_type == 'paddle':
            return self._perform_ocr_paddle(image)
        elif self.engine_type == 'tesseract':
            return self._perform_ocr_tesseract(image)
        else:
            raise ValueError("Unsupported OCR engine type")

    def _perform_ocr_paddle(self, image: bytes) -> dict:
        try:
            preprocessed_image = preprocess_image(image)
            result = self.engine.ocr(preprocessed_image)
            text = '\n'.join([','.join([word[1][0] for word in line]) for line in result])
            return {'text': text}
        except Exception as e:
            logger.error(f"Error performing OCR with PaddleOCR: {e}")
            return {'error': f"Error performing OCR with PaddleOCR: {e}"}

    def _perform_ocr_tesseract(self, image: bytes) -> dict:
        try:
            preprocessed_image = preprocess_image(image)
            text = self.engine.image_to_string(preprocessed_image)
            return {'text': text}
        except Exception as e:
            logger.error(f"Error performing OCR with Tesseract: {e}")
            return {'error': f"Error performing OCR with Tesseract: {e}"}

def preprocess_image(image_bytes):
    # Baca gambar dari bytes
    image = np.array(Image.open(BytesIO(image_bytes)))

    # Buat folder untuk menyimpan hasil pemrosesan gambar
    output_folder = 'processed_images'
    os.makedirs(output_folder, exist_ok=True)
    
    # Simpan gambar asli
    cv2.imwrite(os.path.join(output_folder, 'original_image.png'), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    # Konversi ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(output_folder, 'grayscale_image.png'), gray)
    
    # Equalisasi histogram adaptif
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    cv2.imwrite(os.path.join(output_folder, 'equalized_image.png'), equalized)
    # Terapkan Gaussian blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
    cv2.imwrite(os.path.join(output_folder, 'blurred_image.png'), blurred)
    # Terapkan thresholding adaptif
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite(os.path.join(output_folder, 'adaptive_threshold_image.png'), adaptive_thresh)
    # Penerapan morfologi untuk membersihkan noise
    kernel = np.ones((3, 3), np.uint8)
    morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(os.path.join(output_folder, 'morphed_image.png'), morphed)
    return morphed