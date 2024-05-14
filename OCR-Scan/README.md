# OCR Application

** Seamless Room Recognition: Leveraging Cloud OCR for Nameplate Scanning

# Guide Tesseract Installation on Linux
1. Update your system: Before installing any new packages, it’s a good practice to update your local package index. You can do this by running the following command

# sudo apt update

2. Add Tesseract OCR PPA to your system: Tesseract OCR provides a Personal Package Archive (PPA) that contains the latest packages. Depending on the version you want to install, you can add the PPA as follows

- For the latest release of Tesseract OCR 4 (v4.1.3 so far), you can add the PPA with this command:

# sudo add-apt-repository ppa:alex-p/tesseract-ocr
 
-For the new 5.x release series, you can add the PPA with this command:

# sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel


3. Install Tesseract OCR: After adding the PPA, you can install Tesseract OCR by running the following command:

# sudo apt install tesseract-ocr

# tesseract --version

# Path Tesseract installed
 
You can check the path of Tesseract OCR in Linux by using the which command. This command will show the full path of the shell executable. Here’s how you can do it:

# which tesseract

# Run OCR
 > Install packages # pip install -r requirements.txt 
 > python3 main.py

