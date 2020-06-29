<template>
  <div id="mars-lander">
    <CMarsLanderMap/>
  </div>
</template>

<script lang="ts">
  import {Vue, Component} from 'vue-property-decorator';
  import CMarsLanderMap from "@/components/content/mars-lander/mars-lander-map/CMarsLanderMap.vue";
  @Component({
    components: {CMarsLanderMap}
  })
  export default class CMarsLander extends Vue {
  }
</script>

<style scoped lang="scss">
  #mars-lander {
    height: 100%;
    width: 100%;
  }
</style>