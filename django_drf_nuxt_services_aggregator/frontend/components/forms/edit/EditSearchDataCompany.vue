<template>
  <div class="form-brand">
    № {{ index + 1 }}
    <div class="row">
      <div class="col-12 col-lg-9 col-md-9">
        <div
          id="search"
          v-click-outside="closeSearchResults"
          @click="displaySearchResults"
        >
          <input
            required
            :class="{
              'text-danger': Validate,
            }"
            class="form-control form-control-lg"
            type="search"
            :placeholder="placeholder"
            v-model="search_query"
          />
          <span style="color: red" v-if="Validate">обязательное поле</span>
          <template v-if="search_results.length > 1">
            <div class="search-results" v-if="showSearchResults">
              <div
                @click="OnAddData(item)"
                class="search-item"
                v-for="item in search_results"
                :key="item.id"
              >
                <div class="search-item__name">
                  {{ item.name }}
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
      <div class="col-12 col-lg-3 col-md-3 text-end">
        <div class="btn btn-warning mt-1" @click="removeI()">Удалить</div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ["index","placeholder", "UrlPath", "ListData", "item", "RemoveItemData", "valid"],

  mounted() {
    this.model = this.item;
    setTimeout(() => {
      this.search_query = this.item.name;
    }, 50);
  },
  computed: {
    Validate() {
      if (!this.valid && !this.model.brand) {
        return true;
      } else {
        return false;
      }
    },
    SearchResult() {
      return this.showSearchResults;
    },
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
        this.searchAutocomplete();
      } else {
        this.search_results = [];
      }
    },
  },
  methods: {
    OnAddData(item) {
      this.model.name = item.name;
      this.model.id = item.id;
      this.search_query = item.name;
      this.showSearchResults = false;
    },
    async searchAutocomplete() {
      let url = String(this.UrlPath) + this.search_query;
      await this.$axios.$get(url).then((resp) => {
        this.search_results = resp;
        this.showSearchResults = true;
      });
    },
    closeSearchResults() {
      this.showSearchResults = false;
    },
    displaySearchResults() {
      this.showSearchResults = true;
    },
    removeI() {
      if (this.ListData.length === 1) {
        this.search_query = "";
        this.search_results = [];
        this.model = { id: 1, brand: "" };
        this.showSearchResults = false;
      } else {
        this.RemoveItemData(this.item);
      }
    },
  },
};
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
          font-size: 0.9rem;
        }
      }
    }
  }
}
</style>
