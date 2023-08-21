<template>
  <div
    id="search"
    class="my-4"
    v-click-outside="closeSearchResults"
    @click="displaySearchResults"
  >
    <div class="container">
      <div class="input-group">
        <input
          v-model="search_query"
          type="search"
          class="form-control form-control-lg"
          placeholder="Поиск..."
          aria-describedby="button-search">
        <!-- <button class="btn btn-outline-secondary" type="button" id="button-search">Найти</button> -->
        <Nuxt-link class="btn btn-outline-secondary btn-lg" type="button" id="button-search" active-class="" to="/companies">Найти</Nuxt-link>
      </div>
      <!-- <input
        class="form-control form-control-lg"
        type="search"
        placeholder="Поиск..."
        v-model="search_query"
      /> -->
      <div
        id="search-results"
        v-if="search_results.length > 0 && showSearchResults"
      >
        <div
          @click="onPage(`/companies/${item.slug}`)"
          class="search-item mb-3"
          v-for="item in search_results"
          :key="item.id"
        >
          <!-- {{ item }} -->
          <div class="search-item__name">
            {{ item.name }}
          </div>
          <div class="search-item-brands">
            <strong>Бренды: </strong>
            <span
              class="search-item__brand"
              v-for="(brand, index) in item.brands"
              :key="index"
            >
              {{ brand }}<span v-if="index < item.brands.length - 1">, </span>
            </span>
          </div>
        </div>
        <div class="mt-3 text-center">
          <Nuxt-link class="btn btn-success" active-class="" to="/companies">Все результаты</Nuxt-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search_query: "",
      search_results: [],
      results_qty: 5,
      showSearchResults: false,
      brandsRes: [],
    };
  },
  watch: {
    search_query(val) {
      if (val) {
        this.searchAutocomplete()
      } else {
        this.search_results = []
      }
    },
  },
  methods: {
    onPage(url) {
      this.search_query = ""
      this.search_results = []
      this.$router.push(url)
    },
    async searchAutocomplete() {
      // console.log('searchAutocomplete')
      await this.$axios
        .$get(`/api/v1/companies/search/?search=${this.search_query}` +
            `&city=${this.$store.getters["cities/activeCity"].name}` +
            `&qty=${String(this.results_qty)}`
        )
        .then((res) => (this.search_results = res))
      this.showSearchResults = true
      this.search_results.forEach((el) => {
        let brandsNames = []
        el.brands.forEach(item => {
          brandsNames.push(item.name)
        })

        // find matched brands
        let matchingStrings = []
        brandsNames.forEach(list => {
          if (
            list
              .toLocaleLowerCase()
              .search(this.search_query.toLocaleLowerCase()) > -1
          ) {
            matchingStrings.push(list)
          }
        })
        brandsNames = brandsNames.filter(val => !matchingStrings.includes(val)) // remove brand duplicates
        brandsNames = [...matchingStrings, ...brandsNames]
        if (brandsNames.length > 20) {
          brandsNames.splice(20)
          brandsNames.push("...")
        }
        // end find matched brands

        // push to brand
        el.brands = []
        el.brands.push(...brandsNames)
      })
    },
    closeSearchResults() {
      this.showSearchResults = false
    },
    displaySearchResults() {
      this.showSearchResults = true
    },
  },
}
</script>

<style lang="scss" scoped>
#search {
  position: relative;

  #search-results {
    background-color: white;
    box-shadow: 3px 4px 5px #bebebe;
    padding: 15px;
    margin-right: 15px;
    z-index: 10;
    position: absolute;
    left: 15px;

    .search-item {
      cursor: pointer;
      transition: all ease-in-out 0.3s;
      &:focus,
      &:hover {
        color: orangered;
      }
      &__name {
        font-size: 1.1rem;
        font-weight: 600;
      }
      .search-item-brands {
        line-height: 1.1;
        .search-item__brand {
          font-size: 0.9rem;
        }
      }
    }
  }
}
</style>
