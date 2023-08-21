<template>
  <div id="search">
    <div>
      <div class="container">
        <div class="row">
          <div class="col-12" style="position: relative">
            <form
              class="d-flex"
              style="width: 100%"
              @submit.prevent="onSearchForm"
            >
              <div style="width: 100%">
                <autocomplete
                  :autoSelect="true"
                  @submit="OnSubmit"
                  :search="search"
                  :debounce-time="500"
                  v-on="{ submit: handleSubmit(index) }"
                  :get-result-value="getResultValue"
                  placeholder="поиск мастерских"
                  class="autocomplete"
                >
                  <template #result="{ result, props }">
                    <li v-bind="props">
                      <div class="wiki-title" style="cursor: pointer">
                        {{ result.titleResult }}
                      </div>
                      <div class="wiki-snippet" v-html="result.snippet" />
                    </li>
                  </template>
                </autocomplete>
              </div>

              <button
                class="btn btn-outline-secondary btn-lg"
                type="submit"
                id="button-search"
                active-class=""
              >
                <span>Найти</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      searchdata: [],
      searchmodel: "",
      searchQuery: "",
      inputval: "",
    };
  },
  methods: {
    onSearchForm() {
      console.log("submit");
      if (this.searchmodel.pathRedirect) {
        try {
          this.$router.push(this.searchmodel.pathRedirect);
        } catch (error) {
          console.log("not path");
        }
      } else {
        console.log("no", this.inputval);
        this.$axios
          .get(
            `/api/v1/companies/search-slug/?search=${this.inputval}` +
              `&city=${this.$store.getters["cities/activeCity"].name}`
          )
          .then((resp) => {
            if (resp.data.length > 0) {
              this.$router.push(resp.data[0].slug);
            }
          });
      }
    },
    handleSubmit(index) {
      return (result) => {
        this.searchmodel = result;
      };
    },
    OnSubmit(result) {
      try {
        this.searchmodel.pathRedirect;
        this.$router.push(this.searchmodel.pathRedirect);
        return "";
      } catch (error) {
        console.log("not path");
      }
    },
    getResultValue(result) {
      return result.titleResult;
    },
    async search(input) {
      if (!input) return [];
      this.searchQuery = input;
      let datainput = input;
      if (
        input === "рем" ||
        input === "ремо" ||
        input === "ремон" ||
        input === "ремонт"
      ) {
        datainput = "ремонт ";
      }
      this.inputval = datainput;
      let results = [];
      await this.$axios
        .get(
          `/api/v1/companies/search/?search=${datainput}` +
            `&city=${this.$store.getters["cities/activeCity"].name}`
        )
        .then((resp) => {
          for (let i of resp.data) {
            console.log();
            let splitquery = this.searchQuery.split(" ");

            // если присутствует слово ремонт
            if (
              (splitquery.length > 1 && splitquery.includes("ремонт")) ||
              splitquery.includes("Ремонт")
            ) {
              console.log("fffffff");
              if (
                i.categories &&
                i.categories[0] &&
                !results.filter(
                  (el) =>
                    el.titleResult ===
                    `ремонт ${i.categories[0].declension_one_p}`
                ).length > 0
              ) {
                results.push({
                  titleResult: `ремонт ${i.categories[0].declension_one_p}`,
                  pathRedirect: `/${i.categories[0].slug}`,
                });
              }
            }

            // поиск по категории
            else {
              if (
                i.categories &&
                i.categories[0] &&
                !results.filter(
                  (el) =>
                    el.titleResult ===
                    `ремонт ${i.categories[0].declension_one_p}`
                ).length > 0
              ) {
                results.push({
                  titleResult: `ремонт ${i.categories[0].declension_one_p}`,
                  pathRedirect: `/${i.categories[0].slug}`,
                });
              }
            }
          }
          this.searchdata = results;
        })
        .catch((error) => {
          //   console.error(error);
        });
      this.searchdata = results;
      this.searchmodel = {};

      return results;
    },
  },
};
</script>

<style>
#button-search{
    padding: 7px 12px 6px;
    border: none;
    background: #ffffff;
    font-size: 18px;
    margin-left: -14px;
    z-index: 3;
    transform: skewX(-10deg);
    color: #2e2e2e;
    border-radius: 0px 5px 5px 0;
}
#button-search span{
    font-weight: 500;
    display: block;
    transform: skewX(10deg);
}
.autocomplete-input{
  border: 1px solid #dfdfdf;
  background-color: #dfdfdf;
}
.autocomplete-input:focus, .autocomplete-input[aria-expanded=true]{
  background: #dfdfdf;
  background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjNjY2IiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PGNpcmNsZSBjeD0iMTEiIGN5PSIxMSIgcj0iOCIvPjxwYXRoIGQ9Ik0yMSAyMWwtNC00Ii8+PC9zdmc+);
  background-repeat: no-repeat;
  background-position: 12px;
}
</style>