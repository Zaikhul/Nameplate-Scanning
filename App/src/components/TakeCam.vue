<template>
  <div class="d-flex h-100">
    <div class="justify-content-center align-self-center">
      <h2><strong>Please Add Nameplate Picture</strong></h2>
      <b-container fluid class="nameplate-container">
        <b-row>
          <b-col md="6" class="mb-3">
            <canvas ref="canvas" width="480" height="380"></canvas>
          </b-col>
          <b-col md="6" class="d-flex flex-column align-items-center justify-content-center">
            <video ref="video" width="440" height="280" autoplay class="mb-2"></video>
            <b-button @click="startCamera" variant="primary" class="mb-1" :disabled="cameraStarted">Start Camera</b-button>
            <b-button @click="stopCamera" variant="danger" class="mb-1" :disabled="!cameraStarted">Stop Camera</b-button>
          </b-col>
        </b-row>

        <b-row v-if="processing">
          <b-col cols="12" class="ocr-processing">
            <p><strong>Processing...</strong></p>
          </b-col>
        </b-row>

        <b-row v-if="ocrResult">
          <b-col cols="12" class="ocr-result">
            <p><strong>Class Name Label:</strong> {{ ocrResult }}</p>
          </b-col>
        </b-row>

        <b-row v-if="noValidText">
          <b-col cols="12" class="ocr-no-text">
            <p><strong>No valid text detected. Adjust the camera and try again.</strong></p>
          </b-col>
        </b-row>
      </b-container>
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
      videoTrack: null,
      imageCapture: null,
      cameraStarted: false,
      processing: false,
      noValidText: false,
      socket: null,
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000');

    this.socket.on('ocr_result', (data) => {
      console.log('OCR result:', data.result);
      this.processing = false;
      if (data.result === 'No valid text detected') {
        this.noValidText = true;
      } else {
        this.ocrResult = data.result;
        this.noValidText = false;
        this.drawTextOnCanvas(data.result);
      }
    });

    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext("2d");
  },
  beforeDestroy() {
    this.stopCamera();
    if (this.socket) {
      this.socket.disconnect();
    }
  },
  methods: {
    startCamera() {
      this.cameraStarted = true;
      this.noValidText = false;

      const processFrame = async () => {
        if (!this.videoTrack || this.videoTrack.readyState === 'ended') {
          this.stopCamera();
          return;
        }

        if (this.socket && this.socket.connected) {
          try {
            const imageBitmap = await this.imageCapture.grabFrame();
            this.canvas.width = imageBitmap.width;
            this.canvas.height = imageBitmap.height;
            this.context.drawImage(imageBitmap, 0, 0);
            const photo = this.canvas.toDataURL("image/png");

            this.processing = true;
            this.socket.emit('ocr_request', { image: photo });
          } catch (error) {
            console.error('Error grabbing frame:', error);
            this.stopCamera();
          }
        } else {
          console.warn('WebSocket is not connected.');
        }

        requestAnimationFrame(processFrame);
      };

      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          this.video.srcObject = stream;
          this.videoTrack = stream.getVideoTracks()[0];
          this.imageCapture = new ImageCapture(this.videoTrack);
          processFrame();
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
    drawTextOnCanvas(text) {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height); // Clear previous text
      this.context.font = "20px Arial";
      this.context.fillStyle = "red";
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        this.context.fillText(lines[i], 10, 30 + i * 25);
      }
    }
  },
};
</script>

<style>
.nameplate-container {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

h2 {
  color: #343a40;
  text-align: center;
  margin-bottom: 20px;
}

canvas {
  border: 2px solid #007bff;
  border-radius: 5px;
}

video {
  border: 2px solid #dc3545;
  border-radius: 5px;
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

.d-flex {
  display: flex;
}

.h-100 {
  height: 100vh;
}

.justify-content-center {
  justify-content: center;
}

.align-self-center {
  align-self: center;
}

.mb-1 {
  margin-bottom: 0.25rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
