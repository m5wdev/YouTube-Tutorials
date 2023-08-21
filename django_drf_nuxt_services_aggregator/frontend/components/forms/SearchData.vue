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

            class="form-control form-control-lg"
            type="search"
            :placeholder="placeholder"
            v-model="item.search_query"
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
      <div class="col-12 col-lg-3 col-md-3 text-end">
        <div class="btn btn-warning mt-1" @click="removeI()">Удалить</div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  props: ["index", "ListInputData","UrlPath", "item","placeholder", "removeItemData", "valid"],

  mounted() {
    //   this.searchData = this.item
  },
  computed: {

  },

  data() {
    return {
        searchData:{
            search_query:'',
            id:'',
            name:'',
        },

      showSearchResults: false,
      search_results: [],
    };
  },
  watch: {
    'item.search_query'(val) {
      if (val) {
        this.searchAutocomplete()
      } else {
        this.search_results = []
      }
    },
  },
  methods: {
    AddData(item) {
        this.item.search_query = item.name
        this.item.name = item.name
        this.item.id = item.id
      this.showSearchResults = false
    },
    async searchAutocomplete() {
      await this.$axios
        .$get(this.UrlPath+this.item.search_query)
        .then((resp) => {
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
    removeI() {
      if (this.ListInputData.length === 1) {
        this.searchData.search_query = ""
        this.search_results = []
        this.showSearchResults = false
      } else {
        this.removeItemData(this.item)
      }
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
