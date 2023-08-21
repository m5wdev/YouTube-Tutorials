<template>
  <div class="layout brands">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
    </div>
    <main>
        <Nuxt/>
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
      await this.$store.dispatch("cities/fetch");
    }
  },

  head() {
    return {
      meta: [
        {
          hid: "og:site_name",
          property: "og:site_name",
          content: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_r}`,
        },
      ],
      link: [
        { rel: "canonical", href: `http://localhost:3000/${this.$route.path}` },
      ],
    };
  },
  data() {
    return {
      arrEN: [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
      ],
    };
  },
};
</script>

<style>
.box-one-brand{
  border-radius: 3px;
  box-shadow: 5px 5px 10px 0 rgba(0,0,0,.1);
}

.header-brand {
  margin-top: 0 !important;
}
</style>
