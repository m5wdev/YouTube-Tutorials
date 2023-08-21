<template>
  <div class="layout login-registration">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
    </div>
    <main>
      <div class="container mt-4">
        <div class="btn-group">
          <Nuxt-link
            to="/profile"
            class="btn btn btn-outline-primary"
            active-class=""
            exact-active-class="active"
            >Данные профиля</Nuxt-link
          >
          <Nuxt-link
            to="/profile/companies"
            class="btn btn btn-outline-primary"
            active-class=""
            exact-active-class="active"
            >Мои комании</Nuxt-link
          >
          <Nuxt-link
            to="/profile/companies/add-company"
            class="btn btn btn-outline-primary"
            active-class=""
            exact-active-class="active"
            >Добавить Компанию</Nuxt-link
          >
        </div>
      </div>
      <div class="my-3">
        <Nuxt />
      </div>
    </main>
    <ChunksFooter />
    <ModalsApplication />
  </div>
</template>

<script>
export default {
  middleware: "cities",
  async fetch() {
    if (this.$store.getters["cities/cities"].length === 0) {
      await this.$store.dispatch("cities/fetch")
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
    };
  },
}
</script>

<style>
</style>
