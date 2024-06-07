# utils/logger.py
import os
import logging

def setup_logger():
    log_file_path = os.path.join(os.getcwd(), 'ocr.log')
    logging.basicConfig(filename=log_file_path, level=logging.ERROR, 
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    return logging.getLogger()

logger = setup_logger()
