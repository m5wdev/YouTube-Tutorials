<template>
  <div class="layout brands">
    <div class="my-3">
      <div class="container" v-if="RoUtePath">
        <div class="row" style="padding: 0.7em">
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
            <h1 class="main-title">
              Все сервисные центры в городе
              {{ this.$store.getters["cities/activeCity"].name }} по брендам
            </h1>

            <div class="d-flex flex-row flex-wrap mt-5">
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
      <nuxt-child></nuxt-child>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    RoUtePath() {
      if (!this.$route.params.slug) {
        return true;
      } else {
        return false;
      }
    },
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
  background: #18265fc7;
  margin-top: 0;
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
@media (max-width: 1024px) {
  .main-title {
    color: #fff;
    font-weight: 600;
    font-size: 1.3rem;
  }
  .header-brand {
    margin-top: 0;
  }
  .list-brand {
    margin-top: 0 !important;
  }
}
/* @media (max-width: 767px) {
  .brands > .my-3 > .container + container > .row > .col-12 {
    width: 50%;
  }
  .brands > .my-3 > .container + container > .row > .col-12 a img {
    width: auto;
    max-width: 100%;
  }
} */
</style>
