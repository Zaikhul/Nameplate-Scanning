<!-- init -->

<template>
  <nav class="navbar navbar-expand-lg navbar-light ">
    <div class="container"><a class="navbar-brand" href="#">Nameplate Scanning</a>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
    
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>

        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/nameplate">Nameplate</router-link>
        </li>
        
        <li class="nav-item">
          <router-link class="nav-link" to="/upload">Upload</router-link>
        </li>
      </ul>
    </div></div>
  </nav>
</template>

<script>
export default {
  name: `Navbar`,
};
</script>

<style>
</style>