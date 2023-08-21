<template>
  <div class="container">
    <!-- <div class="row">

      <h1>Бренды</h1>
    </div> -->

    <!-- карточка бренда(имя логотип) -->
    <div class="row">
      <div v-for="brand in brands" :key="brand.id" class="col-lg-2 col-12">
        <div
          @click="OnPage('/brands/' + brand.slug)"
          class="box-manufacturerss box-one-brand"
        >
          <img
            v-lazy-load
            height="36"
            :src="brand.logo"
            alt=""
            class="brand-logo-img"
          />
        </div>
        <h6 class="text-center mt-4">{{ brand.name }}</h6>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  //   layout: "brandsletters",
  head() {
    return {
      title: `Все сервисные центры ${this.$store.getters["cities/activeCity"].declension_r} по бренду. Реестр сервис-центров`,
      meta: [
        {
          hid: "description",
          property: "description",
          content: `Лучшие сервисные центры ${this.$store.getters["cities/activeCity"].declension_r} по бренду: отзывы, цены, услуги, время работы. Servis-Centers.ru — реестр сервисных центров: получи максимум информации перед визитом`,
        },
        {
          hid: "og:title",
          property: "og:title",
          content: `Все сервисные центры ${this.$store.getters["cities/activeCity"].declension_r} по бренду. Реестр сервис-центров — Servis-Centers.ru`,
        },
        {
          hid: "og:description",
          property: "og:description",
          content: `Лучшие сервисные центры ${this.$store.getters["cities/activeCity"].declension_r} по бренду: отзывы, цены, услуги, время работы. Servis-Centers.ru — реестр сервисных центров: получи максимум информации перед визитом`,
        },
        // TODO: og:url
        // {
        //   hid: `og:url`,
        //   name: "og:url",
        //   content: `https://sankt-peterburg.servis-centers.ru`,
        // },
      ],
    };
  },
  async fetch({ store }) {
    if (store.getters["brands/brands"].length === 0) {
      await store.dispatch("brands/fetch");
    }
  },
  data() {
    return {
      brands: this.$store.getters["brands/brands"],
      airports: [{ code: "LAX" }, { code: "NYC" }, { code: "PDX" }],
    };
  },
  methods: {
    OnPage(url) {
      this.$router.push(url);
    },
    onPageSlug(data_category, slug) {
      this.$store.commit("url_page/SetGroup_name_url", data_category);
      this.$store.commit("url_page/Setvalue_url", slug);
      this.$cookies.set("value_url", slug, {
        path: `/`,
        maxAge: 60 * 60 * 24 * 7,
      });
      this.$cookies.set("group_name_url", data_category, {
        path: `/`,
        maxAge: 60 * 60 * 24 * 7,
      });
      this.$router.push(`/${slug}`);
    },
  },
};
</script>

<style>
.box-one-brand img {
  width: auto !important;
  max-width: 100%;
}
</style>
