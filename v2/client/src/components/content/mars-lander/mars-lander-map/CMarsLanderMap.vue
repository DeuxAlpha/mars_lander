<template>
  <div ref="map" id="map-wrapper"/>
</template>

<script lang="ts">
  import {Vue, Component, Ref} from 'vue-property-decorator';
  import {MarsLanderMapController} from "@/components/content/mars-lander/mars-lander-map/MarsLanderMapController";

  @Component
  export default class CMarsLanderMap extends Vue {
    @Ref('map') readonly mapWrapper!: HTMLDivElement;
    controller: MarsLanderMapController = new MarsLanderMapController();

    mounted() {
      this.controller.InitializeChart(this.mapWrapper);
      this.controller.LoadData();
    }
  }
</script>

<style scoped lang="scss">
  #map-wrapper {
    height: 100%;
    width: 100%;
  }
</style>