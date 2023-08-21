<template>
  <div class="layout brands">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
    </div>

    <div class="my-3">
      <div class="container">
        <div class="row">
          <div
            class="
              col-12
              header-brand
              d-flex
              flex-column
              justify-content-center
              align-items-center
            "
          >
            <h1 style="color: #fff; font-weight: 600; font-size: 1.8rem">
              Все сервисные центры в городе {{ this.$store.getters["cities/activeCity"].name }} по брендам
            </h1>

            <div class="d-flex flex-row mt-5">
              <div class="" v-for="letter of arrEN" :key="letter.id">
                <nuxt-link
                  :class="{ activeletter: letter === $route.params.letter }"
                  class="letter"
                  :to="`/brands/letter/${letter}`"
                  >{{ letter }}</nuxt-link
                >
              </div>
              <div>
                <nuxt-link
                  :class="{ activeletter: 'a-ya' === $route.params.letter }"
                  class="letter"
                  :to="`/brands/letter/a-ya`"
                  >А-Я</nuxt-link
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <Nuxt />
    </div>

    <ChunksFooter />
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
.header-brand {
  min-height: 30vh;
  background: grey;
  margin-top: 3em;
  border-radius: 12px;
}
.letter {
  margin: 0 5px;
  padding-bottom: 2px;
  border-bottom: 1px solid #fff;
  color: #fff;
  font-weight: 700;
  cursor: default;
  white-space: nowrap;
  text-decoration: none;
  cursor: pointer;
}
.activeletter {
  color: #c2d1ff;
  border: none;
}
</style>
