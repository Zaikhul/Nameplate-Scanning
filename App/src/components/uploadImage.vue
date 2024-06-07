<template>
  <div class="container-fluid">
    <div class="card">
      <h2 class="text-center">Upload Image for OCR</h2>
      <div class="form-group">
        <input type="file" @change="onFileChange" class="form-control" />
      </div>
      <div class="form-group">
        <label for="ocrEngine">Select OCR Engine</label>
        <select v-model="selectedEngine" class="form-control">
          <option value="tesseract">Tesseract</option>
          <option value="paddle">PaddleOCR</option>
        </select>
      </div>
      <button @click="uploadImage" class="btn btn-primary b-button" :disabled="!selectedFile">
        Upload Image
      </button>
      <div v-if="ocrResult" class="ocr-result">
        <h3>OCR Result:</h3>
        <p>{{ ocrResult }}</p>
      </div>
      <div v-if="errorMessage" class="ocr-no-text">
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      selectedEngine: "tesseract",
      ocrResult: "",
      errorMessage: "",
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
      console.log("File selected:", this.selectedFile.name);
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("image", this.selectedFile);
      formData.append("engine", this.selectedEngine);

      console.log("Uploading image with selected engine:", this.selectedEngine);

      try {
        const response = await axios.post(
          "http://localhost:5000/process-ocr",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        console.log("Response from server:", response.data);
        this.ocrResult = response.data.text;
      } catch (error) {
        console.error("Error uploading image:", error);
        this.errorMessage = "Error uploading image. Please try again.";
      }
    },
  },
};
</script>



<!-- <template>
  <div class="container-fluid">
    <div class="card">
      <h2 class="text-center">Upload Image for OCR</h2>
      <div class="form-group">
        <input type="file" @change="onFileChange" class="form-control" />
      </div>
      <button
        @click="uploadImages"
        class="btn btn-primary b-button"
        :disabled="!selectedFile"
      >
        Upload Image
      </button>
      <div v-if="ocrResult" class="ocr-result">
        <h3>OCR Result:</h3>
        <p>{{ ocrResult }}</p>
      </div>
      <div v-if="errorMessage" class="ocr-no-text">
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";

export default {
  data() {
    return {
      selectedFile: null,
      ocrResult: "",
      errorMessage: "",
      socket: null,
    };
  },
  created() {
    this.socket = io("http://localhost:5000");
    this.socket.on("ocr_response", (data) => {
      this.ocrResult = data.result;
      this.errorMessage =
        data.result !== "No valid text detected" && !data.result
          ? "Error processing image"
          : "";
    });
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadimage() {
      if (!this.selectedFile) {
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        const base64Image = e.target.result.split(",")[1];
        this.socket.emit("ocr_request", { image: base64Image });
      };
      reader.readAsDataURL(this.selectedFile);
    },
  },
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

.b-button {
  width: 100%;
  font-size: 16px;
  margin: 5px 0;
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
</style>
