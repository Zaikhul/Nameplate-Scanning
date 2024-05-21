<template>
  <div class="container-fluid vh-100 d-flex justify-content-center align-items-center">
    <div class="card p-4 shadow">
      <h2 class="text-center mb-4"><strong>OCR Scanner</strong></h2>
      <div class="d-flex justify-content-between mb-3">
        <div class="position-relative">
          <canvas ref="canvas" width="480" height="380" class="border border-primary rounded"></canvas>
          <canvas ref="overlay" width="480" height="380" class="position-absolute top-0 start-0"></canvas>
        </div>
        <div class="d-flex flex-column align-items-center">
          <video ref="video" width="440" height="280" autoplay class="border border-danger rounded mb-2"></video>
          <b-button @click="startCamera" variant="primary" class="mb-1 w-100" :disabled="cameraStarted">Start Camera</b-button>
          <b-button @click="stopCamera" variant="danger" class="mb-1 w-100" :disabled="!cameraStarted">Stop Camera</b-button>
        </div>
      </div>

      <div v-if="processing" class="text-center">
        <p><strong>Processing...</strong></p>
        <b-progress :value="progress" max="100"></b-progress>
      </div>

      <div v-if="ocrResult" class="text-center mt-3">
        <p><strong>Class Name Label:</strong> {{ ocrResult }}</p>
      </div>

      <div v-if="noValidText" class="text-center mt-3">
        <p class="text-danger"><strong>No valid text detected. Adjust the camera and try again.</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: "TakeCam",
  data() {
    return {
      ocrResult: null,
      video: null,
      canvas: null,
      context: null,
      overlay: null,
      overlayContext: null,
      videoTrack: null,
      imageCapture: null,
      cameraStarted: false,
      processing: false,
      progress: 0,
      noValidText: false,
      socket: null,
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000');
    this.socket.on('ocr_result', (data) => {
      this.ocrResultHandler(data);
    });

    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext("2d");
    this.overlay = this.$refs.overlay;
    this.overlayContext = this.overlay.getContext("2d");
  },
  beforeDestroy() {
    this.stopCamera();
    if (this.socket) {
      this.socket.disconnect();
    }
  },
  methods: {
    startCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          this.video.srcObject = stream;
          this.videoTrack = stream.getVideoTracks()[0];
          this.imageCapture = new ImageCapture(this.videoTrack);
          this.cameraStarted = true;
          this.processFrame();
        })
        .catch((error) => {
          console.error("Error starting video stream:", error);
          this.cameraStarted = false;
        });
    },
    stopCamera() {
      if (this.video.srcObject) {
        this.video.srcObject.getTracks().forEach(track => track.stop());
      }
      this.cameraStarted = false;
    },
    processFrame() {
      if (!this.videoTrack || this.videoTrack.readyState === 'ended') {
        this.stopCamera();
        return;
      }

      this.imageCapture.grabFrame()
        .then(imageBitmap => {
          this.context.drawImage(imageBitmap, 0, 0, this.canvas.width, this.canvas.height);
          const photo = this.canvas.toDataURL("image/png");
          this.socket.emit('ocr_request', { image: photo });
          this.processing = true;
          this.updateProgress();
          requestAnimationFrame(() => this.processFrame());
        })
        .catch(error => {
          console.error('Error grabbing frame:', error);
          this.stopCamera();
        });
    },
    updateProgress() {
      this.progress = (this.progress + 10) % 100; // Simulate progress update
    },
    ocrResultHandler(data) {
      console.log('OCR result:', data.result);
      this.processing = false;
      this.progress = 0;
      this.overlayContext.clearRect(0, 0, this.overlay.width, this.overlay.height);
      if (data.result === 'No valid text detected') {
        this.noValidText = true;
      } else {
        this.ocrResult = data.result;
        this.noValidText = false;
        this.drawTextOnCanvas(data.result);
        this.drawBoundingBoxes(data.boxes);
      }
    },
    drawTextOnCanvas(text) {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height); // Clear previous text
      this.context.font = "20px Arial";
      this.context.fillStyle = "red";
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        this.context.fillText(lines[i], 10, 30 + i * 25);
      }
    },
    drawBoundingBoxes(boxes) {
      this.overlayContext.strokeStyle = 'red';
      this.overlayContext.lineWidth = 2;
      boxes.forEach(box => {
        this.overlayContext.strokeRect(box[0], box[1], box[2], box[3]);
      });
    }
  },
};
</script>

<style>
body {
  background-color: #f8f9fa;
}

.container-fluid {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card {
  max-width: 800px;
  margin: auto;
}

h2 {
  color: #343a40;
}

canvas, video {
  display: block;
  margin: 0 auto;
}

.b-button {
  width: 100%;
  font-size: 16px;
  margin: 5px 0;
}

.ocr-processing {
  text-align: center;
  color: #ffc107;
}

.ocr-result {
  text-align: center;
  color: #28a745;
  font-size: 18px;
  font-weight: bold;
}

.ocr-no-text {
  text-align: center;
  color: #dc3545;
  font-size: 16px;
  font-weight: bold;
}

.position-absolute {
  position: absolute;
}

.top-0 {
  top: 0;
}

.start-0 {
  left: 0;
}
</style>