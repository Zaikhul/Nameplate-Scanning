<template>
  <div class="d-flex h-100">
    <div class="justify-content-center align-self-center">
      <h2>
        <strong>
          Please Add <br />
          Nameplate Picture</strong>
      </h2>
      <b-container fluid class="nameplate-container">
        <!--  capture dan preview kamera -->
        <b-row>
          <!--  menampilkan hasil capture -->
          <b-col md="6" class="mb-3">
            <canvas ref="canvas" width="480" height="380"></canvas>
          </b-col>
          <!--  preview kamera dan tombol -->
          <b-col md="6" class="d-flex flex-column align-items-center justify-content-center">
            <video ref="video" width="440" height="280" autoplay class="mb-2"></video>
            <b-button @click="startCamera" variant="primary" class="mb-1">Start Camera</b-button>
            <b-button @click="takePhoto" variant="success">Take Photo</b-button>
          </b-col>
        </b-row>

        <!--  hasil foto yang berhasil disimpan -->
        <b-row v-if="photo">
          <b-col cols="12" class="mt-3">
            <b-image :src="photo" fluid alt="Captured Photo"></b-image>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
//import axios from 'axios';
export default {
  name: "TakeCam",
  data() {
    return {
      photo: null,
    };
  },
  methods: {
    startCamera() {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          this.$refs.video.srcObject = stream;
        })
        .catch((error) => {
          console.error("Error starting video stream:", error);
        });
    },
    takePhoto() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext("2d");
      const video = this.$refs.video;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.photo = canvas.toDataURL("image/png");

      // Mematikan kamera
      const stream = video.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach((track) => track.stop());

      // video tidak menampilkan apa-apa
      video.srcObject = null;

      // simpan photo
      this.savePhoto();
    },
    /*
    savePhoto() {
      const formData = new FormData();
      const canvas = this.$refs.canvas;

      // canvas image ke Blob --> tambahkan ke form data
      canvas.toBlob(blob => {
        formData.append('photo', blob, 'photo.png');

        // axios untuk POST request ke server
        axios.post('http://your-backend-url/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
          .then(response => {
            // Lakukan sesuatu jika upload berhasil
            console.log('Image uploaded successfully:', response);
          })
          .catch(error => {
            // jika upload gagal
            console.error('Error uploading image:', error);
          });
      }, 'image/png');
    }, */
  },
};
</script>

<style>
/* Tambahkan style yang Anda perlukan di sini */
</style>