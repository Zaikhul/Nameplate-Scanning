<template>
  <div class="d-flex h-100">
    <div class="justify-content-center align-self-center">
      <h2>
        <strong>Please Add <br />Nameplate Picture</strong>
      </h2>
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
            <p><strong>OCR Result:</strong> {{ ocrResult }}</p>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import VueSocketIO from 'vue-socket.io';

export default {
  name: "TakeCam",
  data() {
    return {
      ocrResult: null,
      socket: null,
      video: null,
      canvas: null,
      context: null,
      videoTrack: null,
      imageCapture: null,
      cameraStarted: false,
      processing: false
    };
  },
  mounted() {
    this.socket = new VueSocketIO({
      debug: true,
      connection: 'http://localhost:5000',
    });

    this.socket.io.on('ocr_result', (data) => {
      console.log('OCR result:', data.result);
      this.ocrResult = data.result;
      this.processing = false;
    });

    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext("2d");
  },
  methods: {
    startCamera() {
      this.cameraStarted = true;
      this.socket = new VueSocketIO({
        debug: true,
        connection: 'http://localhost:5000',
      });

      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          this.video.srcObject = stream;
          this.videoTrack = stream.getVideoTracks()[0];
          this.imageCapture = new ImageCapture(this.videoTrack);
          const canvas = this.canvas;
          const context = canvas.getContext('2d');

          const processFrame = () => {
            if (!this.videoTrack.readyState || this.videoTrack.readyState === 'ended') {
              console.log('Video track is not ready or has ended.');
              this.stopCamera();
              return;
            }

            this.imageCapture.grabFrame()
              .then((imageBitmap) => {
                canvas.width = imageBitmap.width;
                canvas.height = imageBitmap.height;
                context.drawImage(imageBitmap, 0, 0);
                const photo = canvas.toDataURL("image/png");
                this.processing = true;
                this.socket.io.emit('ocr_request', { image: photo });
                requestAnimationFrame(processFrame);
              })
              .catch((error) => {
                console.error('Error grabbing frame:', error);
                this.stopCamera();
              });
          };

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
  },
};
</script>

<style>
/* Style untuk container utama */
.nameplate-container {
  margin-top: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* Style untuk judul */
h2 {
  text-align: center;
  color: #343a40;
  font-size: 24px;
  margin-bottom: 20px;
}

/* Style untuk video dan canvas */
video, canvas {
  border: 2px solid #6c757d;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* Style untuk tombol */
b-button {
  margin-top: 10px;
}

/* Style untuk hasil OCR */
.ocr-result {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #495057;
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 5px;
}

/* Style untuk proses OCR */
.ocr-processing {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #007bff;
}
</style>