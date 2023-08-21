<template>
  <div class="layout company">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
      <!-- <FormsSearchCompany /> -->
      <FormsAutocomplete />
    </div>
    <main class="mb-3">
      <Nuxt />
    </main>
    <ChunksFooter />

    <template v-if="current_company">
      <ModalsCompanyApplication :company="current_company" />
      <ModalsCompanyAbuse :company="current_company" />
    </template>
    <ModalsApplication />
  </div>
</template>

<script>
export default {
  middleware: "cities",
  async fetch() {
    if (this.$store.getters["cities/cities"].length === 0) {
      await this.$store.dispatch("cities/fetch");
    }
  },

  head() {
    return {
      meta: [
        {
          hid: 'og:site_name',
          property: "og:site_name",
          content: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_p}`,
        },
      ],
            link: [
        { rel: "canonical", href: `http://localhost:3000/${this.$route.path}` },
      ],
    };
  },

  data() {
    return {
      current_company: this.$store.getters["company/get_current_company"],
    }
  },
};
</script>
