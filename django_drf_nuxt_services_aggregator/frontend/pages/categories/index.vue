<template>
  <div class="container categories-content">
    <div class="row mb-4">
      <h1>Категории</h1>
    </div>
    <!--  список категорий  -->
    <div class="row row-cols-1 g-3">
      <!-- карточка категории components/cards/Service -->
      <CardsService
        v-for="category in categories"
        :key="category.id"
        :category="category"
      />
    </div>
  </div>
</template>

<script>
export default {
//   layout: "brands",
  head() {
    return {
      title: `Все виды ремонтируемой техники в ${this.$store.getters["cities/activeCity"].declension_p}`,
      meta: [
        {
          hid: `description`,
          name: "description",
          content: `Тут полный список видов техники, которую можно отремонтировать в сервисных центрах ${this.$store.getters["cities/activeCity"].declension_r}. Смотрите сейчас!`,
        },

        {
          hid: `og:title`,
          name: "og:title",
          content: `Все виды ремонтируемой техники в ${this.$store.getters["cities/activeCity"].declension_p}`,
        },
        {
          hid: `og:description`,
          name: "og:description",
          content: `Страница с полным списком видов техники, которую можно отремонтировать в сервисных центрах ${this.$store.getters["cities/activeCity"].declension_r}. Смотрите сейчас!`,
        },
        // TODO: og:url
        // {
        //   hid: `og:url`,
        //   name: "og:url",
        //   content: `https://sankt-peterburg.servis-centers.ru`,
        // },
      ],
    }
  },
  async fetch({ store }) {
    if (store.getters["categories/categories"].length === 0) {
      await store.dispatch("categories/fetch");
    }
  },
  data() {
    return {
      categories: this.$store.getters["categories/categories"],
    };
  },
};
</script>

<style lang="scss">
.categories-content{
  margin-top: 30px;
}
</style>
