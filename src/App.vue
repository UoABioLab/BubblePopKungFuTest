<template>
  <div id="app">
    <div class="background">
      <img src="/Assets/dojo.jpg" alt="dojo background" class="background-image" />
      <div class="ground"></div>
    </div>
    <Game />
  </div>
</template>
<script setup>
import Game from './components/Game.vue'
</script>
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
#app {
  width: 100vw;
  height: 100vh;
  position: relative;
}
.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 50px);
  object-fit: cover;
}
.ground {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50px;
  background-color: #ffffff;
}
</style> 
