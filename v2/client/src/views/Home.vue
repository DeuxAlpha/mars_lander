<template>
  <div id="home">
    <CMarsLanderMap/>
  </div>
</template>

<script>
  import CMarsLanderMap from "@/components/content/mars-lander-map/CMarsLanderMap";

  export default {
    components: {CMarsLanderMap}
  }
</script>

<style lang="scss">
  #home {
    height: 100vh;
  }
</style>
