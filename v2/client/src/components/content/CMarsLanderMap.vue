<template>
  <svg ref="map"/>
</template>

<script lang="ts">
  import {Vue, Component, Ref} from 'vue-property-decorator';
  import {MarsLanderMapController} from "@/components/content/MarsLanderMapController";

  @Component
  export default class CMarsLanderMap extends Vue {
    @Ref('map') readonly map!: SVGSVGElement;
    readonly controller = new MarsLanderMapController();

    mounted() {
      this.controller.Build(this.map);
    }
  }
</script>

<style scoped lang="scss">

</style>