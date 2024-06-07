<template>
  <div class="upload">
    <Navbar />
    <div class="container">
      <uploadImage />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from "@/components/Navbar.vue";
import uploadImage from "@/components/uploadImage.vue";

export default {
  name: `upload`,
  components: {
    Navbar,
    uploadImage,
  },
};
</script>

<style></style>
