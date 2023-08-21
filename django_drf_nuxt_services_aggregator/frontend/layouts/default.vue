<template>
  <div class="layout default">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
    </div>
    <main>
      <!-- <FormsSearchCompany /> -->
      <FormsAutocomplete v-if="!$route.path.includes('/registration') || !$route.path.includes('/login')" />
      <div class="my-3">
        <section v-if="RoutePath" id="header_index" class="mb-4">
          <div
            id="header_page"
            lazy-background="~/assets/images/bg-service.jpg"
            data-not-lazy
          >
            <div id="header_page__inner">
              <h1 class="text-center">
                Услуги сервисных центров
                {{ $store.getters["cities/activeCity"].declension_r }}
              </h1>
            </div>
          </div>
        </section>
        <Nuxt />
      </div>
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
          hid: "og:site_name",
          property: "og:site_name",
          content: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_p}`,
        },
      ],
      link: [
        // { rel: "canonical", href: `http://localhost:3000/${this.$route.path}` },
      ],
    };
  },

  data() {
    return {
      current_company: this.$store.getters["company/get_current_company"],
    }
  },

  computed: {
    RoutePath() {
      // console.log(222,this.$route.params);
      if (
        this.$route.path.includes("/categories") ||
        this.$route.path.includes("/brands") ||
        this.$route.path.includes("/companies") ||
        this.$route.path.includes("/registration") ||
        this.$route.path.includes("/login") ||
        this.$route.params.category
      ) {
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>

<style lang="scss">
#header_index{
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}
#header_page {
  // background-size: auto 40%;
  // background-position: 50% -20%;
  background-position: 50% 0;
  background-repeat: no-repeat;
  background-attachment: fixed;
  box-shadow: 0 1px 5px hsl(0deg 0% 86% / 50%);
  color: white;
  width: 100%;
  height: 100%;
  background-size: 110% !important;

  @media (min-width: 1080.99px) {
    background-size: 100%;
    // background-position: 50% -10%;
  }
  @media (max-width: 1080px) {
    background-size: auto 50%;
    // background-position: 50% 0;
  }

  &__inner {
    background-image: linear-gradient(rgba(0, 0, 0, 0.29), rgba(0, 0, 0, 0.66));
    // padding: 100px 25px;
    height: 25vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
