<template>
  <div ref="map" id="map-wrapper" class="w-full h-full"/>
</template>

<script lang="ts">
  import {Vue, Component, Ref} from 'vue-property-decorator';
  import {MarsLanderMapController} from "@/components/content/MarsLanderMapController";

  @Component
  export default class CMarsLanderMap extends Vue {
    @Ref('map') readonly svgElement!: SVGSVGElement;
    controller!: MarsLanderMapController;

    mounted() {
      this.controller = new MarsLanderMapController(this.svgElement);
      this.controller.GenerateBoundaries(7000, 3000);
    }
  }
</script>

<style scoped lang="scss">
  #map-wrapper {
    background: red;
  }
</style>