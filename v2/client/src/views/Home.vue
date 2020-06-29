<template>
  <div id="home">
    <CMarsLander/>
  </div>
</template>

<script>
  import CMarsLander from "@/components/content/mars-lander/CMarsLander";

  export default {
    components: {CMarsLander}
  }
</script>

<style lang="scss">
  #home {
    height: 100vh;
  }
</style>
