<!-- init -->
<template>
  <div class="row">
    <div class="col">
      <div class="d-flex h-100">
        <div class="justify-content-center align-self-center">
          <h2><strong>Please Add <br />Nameplate Picture</strong></h2>
          <form @submit.prevent="submitForm">
            <h4>Upload Here</h4>
            <input id="text" type="text" name="myText" />
            <input
              id="image"
              type="file"
              name="myImage"
              multiple
              accept="image/*"
              @change="previewImage"
            />
            <input id="submit" type="submit" value="Upload" />
            <hr />
            <h4>Preview</h4>
            <div id="preview">
              <img v-if="imageData" :src="imageData" alt="Image preview" />
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="col">
      <img src="../assets/page1.png" width="400" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: `page`,
  data() {
    return {
      imageData: null, // Ini akan menyimpan data gambar untuk preview
    };
  },
  methods: {
    previewImage(event) {
      const file = event.target.files[0];
      this.imageData = URL.createObjectURL(file);
    },
   submitForm() {
      const formData = new FormData();
      const imageInput = this.$refs.image;
      
      // Dapat menghandle multiple files dengan loop jika perlu
      Array.from(imageInput.files).forEach((file, index) => {
        formData.append('myImage' + index, file);
      });

      // Kirim form data ke server
      axios.post('http://localhost:5000/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
      })
      .then(response => {
        // upload berhasil
        console.log('Image uploaded successfully:', response);
      })
      .catch(error => {
        // jika upload gagal
        console.error('Error uploading image:', error);
      });
    },
  },
};
</script>

<style>
/* Anda dapat menambahkan style tambahan jika diperlukan */
</style>
