import cv2
import pytesseract
import numpy as np
from PIL import Image
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

def captureScreen(bbox=(300, 300, 1500, 1000)):
    capScr = np.array(Image.open(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    return adaptive_thresh

def check_accuracy(word, x, y, w, h, original_img):
    roi = original_img[y:h, x:w]
    if roi.size == 0:
        return False
    preprocessed_roi = preprocess_image(roi)
    pred = pytesseract.image_to_string(preprocessed_roi, config='--psm 10 --oem 3')
 
    if pred.strip() == word:
        return True
    else:
        return False

while True:
    timer = cv2.getTickCount()
    ret, img = cap.read()
    if not ret:
        print("Unable to capture video")
        break
    try:
        hImg, wImg, _ = img.shape
    except AttributeError:
        print("shape not found")
        continue
    
    original_img = img.copy()
    
    # Preprocessing gambar
    preprocessed_img = preprocess_image(img)
    
    boxes = pytesseract.image_to_boxes(preprocessed_img)
    scanned_words = []  
    current_word = ''  
    current_word_correct_count = 0
    current_word_total_count = 0
    for b in boxes.splitlines():
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        word = b[0]  
        scanned_words.append(word) 
        # Deteksi tiap huruf
        is_correct = check_accuracy(word, x, y, w, h, original_img)
        if is_correct:
            current_word += word
            current_word_correct_count += 1
        else:
            if current_word:
                current_word += ' '
            current_word = word
        current_word_total_count += 1
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 2)
        cv2.putText(img, word, (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    if current_word:
        scanned_words.append(current_word)
        word_accuracy = (current_word_correct_count / current_word_total_count) * 100
        print(f"Akurasi kata '{current_word}': {word_accuracy:.2f}%")
        
        with open("scanned_text.txt", "w") as file:
            file.write(" ".join(scanned_words))  
        with open("scanned_text.txt", "r") as file:
            content = file.read()
            print("Kata-kata dan angka yang terdeteksi:", content)
    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.imshow("Result", img)
    cv2.waitKey(1)
