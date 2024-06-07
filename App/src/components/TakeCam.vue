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
          <b-button @click="startCamera" variant="primary" class="mb-1 w-100" :disabled="cameraStarted">Start
            Camera</b-button>
          <b-button @click="stopCamera" variant="danger" class="mb-1 w-100" :disabled="!cameraStarted">Stop
            Camera</b-button>
          <b-button @click="captureImage" variant="success" class="mb-1 w-100" :disabled="!cameraStarted">Capture
            Image</b-button>
          <select v-model="selectedEngine" class="form-select mt-2">
            <option value="tesseract">Tesseract</option>
            <option value="paddle">PaddleOCR</option>
          </select>
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
      <div v-if="errorMessage" class="text-center mt-3">
        <p class="text-danger"><strong>{{ errorMessage }}</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
      errorMessage: '',
      selectedEngine: 'tesseract'
    };
  },
  methods: {
    startCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.video = this.$refs.video;
          this.video.srcObject = stream;
          this.videoTrack = stream.getVideoTracks()[0];
          this.canvas = this.$refs.canvas;
          this.context = this.canvas.getContext('2d');
          this.overlay = this.$refs.overlay;
          this.overlayContext = this.overlay.getContext('2d');
          this.cameraStarted = true;
          console.log("Camera started successfully.");
        })
        .catch(err => {
          console.error("Error starting camera: ", err);
        });
    },
    stopCamera() {
      this.videoTrack.stop();
      this.cameraStarted = false;
      console.log("Camera stopped.");
    },
    captureImage() {
      this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      this.canvas.toBlob(blob => {
        console.log("Image captured.");
        this.sendToServer(blob);
      }, 'image/png');
    },
    async sendToServer(imageBlob) {
      this.processing = true;
      this.progress = 0;
      this.noValidText = false;
      this.errorMessage = '';

      const formData = new FormData();
      formData.append('image', imageBlob, 'captured.png');
      formData.append('engine', this.selectedEngine);

      console.log("Sending image to server with selected engine:", this.selectedEngine);

      try {
        const response = await axios.post("http://localhost:5000/process-ocr", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        console.log("Response from server:", response.data);

        if (response.data && response.data.text) {
          this.ocrResult = response.data.text;
          if (!response.data.text.trim()) {
            this.noValidText = true;
          }
          this.drawBoundingBoxes(response.data.boxes || []);
        } else {
          this.noValidText = true;
        }
      } catch (error) {
        console.error("Error processing OCR request: ", error);
        this.errorMessage = 'Error processing OCR request. Please try again later.';
      } finally {
        this.processing = false;
        this.progress = 100;
      }
    },
    drawBoundingBoxes(boxes) {
      this.overlayContext.clearRect(0, 0, this.overlay.width, this.overlay.height);
      this.overlayContext.strokeStyle = 'red';
      this.overlayContext.lineWidth = 2;

      boxes.forEach(box => {
        this.overlayContext.beginPath();
        this.overlayContext.moveTo(box[0][0], box[0][1]);
        box.forEach(point => this.overlayContext.lineTo(point[0], point[1]));
        this.overlayContext.closePath();
        this.overlayContext.stroke();
      });

      console.log("Bounding boxes drawn on overlay.");
    }
  }
};
</script>


<!-- <template>
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
          <b-button @click="captureImage" variant="success" class="mb-1 w-100" :disabled="!cameraStarted">Capture Image</b-button>
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
      <div v-if="errorMessage" class="text-center mt-3">
        <p class="text-danger"><strong>{{ errorMessage }}</strong></p>
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
      errorMessage: '',
      socket: null
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000');
    this.socket.on('ocr_result', (data) => {
      this.processing = false;
      this.ocrResult = data.result;
      this.noValidText = data.result === 'No valid text detected';
      this.errorMessage = data.result !== 'No valid text detected' && !data.result ? 'Error processing image' : '';
    });
  },
  methods: {
    startCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.video = this.$refs.video;
          this.video.srcObject = stream;
          this.videoTrack = stream.getVideoTracks()[0];
          this.canvas = this.$refs.canvas;
          this.context = this.canvas.getContext('2d');
          this.overlay = this.$refs.overlay;
          this.overlayContext = this.overlay.getContext('2d');
          this.cameraStarted = true;
        })
        .catch(err => {
          console.error("Error starting camera: ", err);
        });
    },
    stopCamera() {
      this.videoTrack.stop();
      this.cameraStarted = false;
    },
    captureImage() {
      this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      const imageData = this.canvas.toDataURL('image/png');
      this.sendToServer(imageData);
    },
    sendToServer(imageData) {
      this.processing = true;
      this.socket.emit('ocr_request', { image: imageData });
    }
  }
};
</script> -->

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

canvas,
video {
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
