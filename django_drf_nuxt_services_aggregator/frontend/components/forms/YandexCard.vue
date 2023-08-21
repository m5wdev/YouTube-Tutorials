<template>
<div>


  <yandex-map
    :cluster-options="clusterOptions"
    :zoom="zoom"
    :coords="firstPoint"
    :scroll-zoom="false"
    :controls="['zoomControl',]"
  >
    <ymap-marker
      :balloon="{
        header: `[${company.name}]<br>${point.address_with_city}` ,
        body: `

              ${point.phone ? point.phone : ''}
              ${point.work_time ? point.work_time : ''}
              `
      }"
      cluster-name="1"
      marker-type="placemark"
      v-for="point in points"
      :key="point.id"
      :marker-id="point.id"
      :coords="[point.latitude, point.longitude]"
    />
  </yandex-map>
  </div>
</template>

<script>
export default {
  props: ["points", "company", "firstPoint", "zoom", "address"],

  data() {
    return {
      coords: [],
      clusterOptions: {
        // 1: {
        //   clusterDisableClickZoom: true,
        //   clusterOpenBalloonOnClick: true,
        //   clusterBalloonLayout: "<span>123</span>",
        // },
      },
    };
  },
};
</script>

<style >
.ymap-container {
  height: 400px;
  width: 100%;
}
.ymaps-2-1-79-controls__control_toolbar {
  display: none;
}
.ymaps-2-1-79-controls-pane *,
.ymaps-2-1-79-searchpanel-pane * {
  text-align: left;
  /* display: none; */
}
</style>
