<template>
  <div ref="map" id="map-wrapper"/>
</template>

<script lang="ts">
  import {Vue, Component, Ref} from 'vue-property-decorator';
  import {MarsLanderMapController} from "@/components/content/MarsLanderMapController";

  @Component
  export default class CMarsLanderMap extends Vue {
    @Ref('map') readonly mapWrapper!: HTMLElement;
    controller: MarsLanderMapController = new MarsLanderMapController();

    mounted() {
      this.controller.Init(this.mapWrapper);
      this.controller.GenerateBoundaries(7000, 3000);
    }
  }
</script>

<style scoped lang="scss">
</style>