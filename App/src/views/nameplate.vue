<template>
    <div class="nameplate">
      <Navbar />
      <div class="container">
        <TakeCam />
      </div>
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import Navbar from "@/components/Navbar.vue";
  import TakeCam from "@/components/TakeCam.vue";
  
  export default {
    name: `nameplate`,
    components: {
      Navbar,
      TakeCam
    },
  };
  </script>
  
  <style>
  </style>