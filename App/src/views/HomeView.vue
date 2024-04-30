<template>
  <div class="home">
    <Navbar />
    <div class="container">
      <Page />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from "@/components/Navbar.vue";
import Page from "@/components/Page.vue";

export default {
  name: "HomeView",
  components: {
    Navbar,
    Page,
  },
};
</script>
