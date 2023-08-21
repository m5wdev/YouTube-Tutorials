<template>
  <div class="form-city">

    <div class="row">
      <div class="col-12">
        <div
          id="search"
          v-click-outside="closeSearchResults"
          @click="displaySearchResults"
        >
          <input
            required

            class="form-control form-control-lg"
            type="search"
            placeholder="Поиск Города"
            v-model="search_query"
          />
          <template v-if="search_results.length > 1">
            <div class="search-results" v-if="showSearchResults">
              <div
                @click="AddData(res)"
                class="search-item"
                v-for="res in search_results"
                :key="res.id"
              >
                <div class="search-item__name">
                  {{ res.name }}
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ["UrlPath", "item", "Addcityid"],

  mounted() {
    this.model = this.item;
    setTimeout(() => {
      this.search_query = this.item.name;
      this.Addcityid(this.item.id);
    }, 50);
  },
  computed: {

  },

  data() {
    return {
      brand: "",
      model: {},
      search_query: "",
      showSearchResults: false,
      search_results: [],
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
    AddData(item) {
      this.search_query = item.name;
      this.Addcityid(item.id);
      this.showSearchResults = false;;
    },
  async searchAutocomplete() {
      this.showSearchResults = true;
        await this.$axios
          .$get(String(this.UrlPath) + this.search_query
          )
          .then((resp) =>{
              this.search_results = resp
              this.showSearchResults = true
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
.form-brand {
  background: white;
  padding: 1em;
  border-radius: 12px;
  margin-top: 3em;
}

.text-danger {
  border: 1px solid red;
}

#search {
  position: relative;

  .search-results {
    background-color: white;
    box-shadow: 3px 4px 5px #bebebe;
    padding: 15px;
    z-index: 10;
    position: absolute;
    left: 0;
    width: 100%;
    max-height: 400px;
    overflow: auto;

    .search-item {
      cursor: pointer;
      transition: all ease-in-out 0.3s;

      &:not(:last-child) {
        margin-bottom: 10px;
      }

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
          font-size: .9rem;
        }
      }
    }
  }
}
</style>



