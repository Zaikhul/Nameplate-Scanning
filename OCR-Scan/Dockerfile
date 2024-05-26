# Dockerfile for OCR-Scan
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python" ]

EXPOSE 5000

#CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "python", "app.py"]
CMD ["app.py" ]
