<template>
  <div>
    <yandex-map
      :zoom="18"
      :coords="[point.latitude, point.longitude]"
      :scroll-zoom="false"
      :controls="['zoomControl']"
    >
      <ymap-marker
        :balloon="{
          header: `[${company}]<br>${point.address_with_city}`,
          body: `

              ${point.phone ? point.phone : ''}
              ${point.work_time ? point.work_time : ''}
              `,
        }"
        marker-type="placemark"
        :marker-id="point.id"
        :coords="[point.latitude, point.longitude]"
      />
    </yandex-map>
  </div>
</template>

<script>
export default {
  props: ["point", "company"],

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

<style lang="scss" scoped>
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
}
</style>
