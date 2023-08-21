<template>
  <div>
    <div v-if="loader" class="loader-page">
      <div
        style="position: absolute left: 50% top: 50%"
        :size="50"
        color="rgb(59, 118, 234)"
        indeterminate
        class="spinner-border text-primary"
        role="status"
      >
        <span class="visually-hidden"></span>
      </div>
    </div>

    <!-- <FormsSearchCompany /> -->

    <div class="container">
      <h1>Услуга: {{ service_name.name }}</h1>
    </div>

    <PagesCompanies
      :companies="resp_data"
      :name_slug="'поуслуге ' + service_name.name"
      :list_companies="resp_data.results.companies"
      :OnFilters="OnFilters"
      :RemoveFilter="RemoveFilter"
      :list_categories="list_categories"
    />

    <div class="container d-flex justify-content-center my-4">
      <Pagination v-model="page_Pagination" :records="resp_data.count" />
    </div>
  </div>
</template>


<script>
export default {
  async asyncData({ $axios, store, req, route }) {
    let subdomain = store.getters["cities/activeCity"].subdomain.name
    let page = route.query.page || 1
    let params
    if (Object.keys(route.query).length > 1) {
      // console.log("params")
      params =
        `page=${page}&servicesslug=${route.params.slug}&` +
        `subdomain=${subdomain}&` +
        `free_diagnostics=${route.query.free_diagnostics || ""}&` +
        `quick_repair=${route.query.quick_repair || ""}&` +
        `pay_after_repair=${route.query.pay_after_repair || ""}&` +
        `own_warehouse=${route.query.own_warehouse || ""}&` +
        `free_parking=${route.query.free_parking || ""}&` +
        `fix_price=${route.query.fix_prices || ""}&` +
        `cash_pay=${route.query.cash_pay || ""}` +
        `&card_pay=${route.query.card_pay || ""}`
    } else {
      params = `page=${page}&subdomain=${subdomain}&servicesslug=${route.params.slug}`
    }
    const resp_data = await $axios.get(`/api/v1/companies/?${params}`)

    let list_categories = []
    for (let company of resp_data.data.results.companies) {
      for (let category of company.subcategories) {
        if (!category.important) {
          list_categories.push(category)
        }
      }
    }
    const service_name = await $axios.get(
      `api/v1/services/${route.params.slug}/`
    );

    return {
      resp_data: resp_data.data,
      subdomain: subdomain,
      list_categories: list_categories,
      service_name: service_name.data,
    };

  },
  data() {
    return {
      companies: [],
      page_Pagination: this.$route.query.page || 1,
      filter_params: "",
      perPage: 3,
      filter: false,
      search: "",
      loader: false,
    }
  },
  mounted() {},
  watch: {
    search(newValue, oldValue) {
      console.log(newValue)
    },
    page_Pagination(val) {
      this.pageData()
    },
  },
  computed: {
    rows() {
      return Math.ceil(this.resp_data.count / 5)
    },
    list_companies() {
      if (!this.filter && !this.search) {
        this.companies = this.resp_data.results.companies
      }
      return this.companies
    },
    category_page() {
      return this.$store.getters["url_page/value_url"]
    },
    category_page_url() {
      return this.$store.getters["url_page/group_name_url"]
    },
  },
  methods: {
    importantFilters() {
      let list_categories = []
      for (let company of this.resp_data.results.companies) {
        for (let category of company.subcategories) {
          if (!category.important) {
            list_categories.push(category)
          }
        }
      }
      this.list_categories = list_categories
    },
    async pageData() {
      let url
      if (Object.keys(this.$route.query).length > 1) {
        url = `api/companies/?page=${this.page_Pagination}&${this.filter_params}`
        this.$router.push(
          `/services/${this.$route.params.slug}/` +
            `?page=${this.page_Pagination}` +
            `&${this.filter_params}`
        )
      } else {
        url = `api/v1/companies/?page=${this.page_Pagination}&subdomain=${this.subdomain}&servicesslug=${this.$route.params.slug}`
        this.$router.push(
          `/services/${this.$route.params.slug}/` +
            `?page=${this.page_Pagination}`
        )
      }
      this.loader = true
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        })
      }, 250)

      await this.$axios
        .$get(url, {})
        .then((resp) => {
          this.resp_data = resp

          setTimeout(() => {
            this.importantFilters()
          }, 50)
          setTimeout(() => {
            this.loader = false
          }, 50)
        })
        .catch((error) => {
          this.loader = false
          // console.error(error)
        })
    },
    async RemoveFilter() {
      let url = `api/v1/companies/?page=${this.page_Pagination}&subdomain=${this.subdomain}&servicesslug=${this.$route.params.slug}`
      this.loader = true
      this.filter = false
      this.filter_params = ""
      this.page_Pagination = 1
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        })
      }, 250)
      await this.$axios
        .$get(url, {})
        .then((resp) => {
          this.resp_data = resp

          this.$router.push(`/services/${this.$route.params.slug}`)
          setTimeout(() => {
            this.importantFilters()
          }, 50)
          setTimeout(() => {
            this.loader = false
          }, 50)
        })
        .catch((error) => {
          this.loader = false
          // console.error(error)
        })
    },
    async OnFilters(
      free_diagnostics,
      quick_repair,
      pay_after_repair,
      own_warehouse,
      free_parking,
      fix_price,
      cash_pay,
      card_pay,
      courier_departure,
      master_departure
    ) {
      this.filter = true
      if (cash_pay == false) {
        cash_pay = ""
      }
      if (courier_departure == false) {
        courier_departure = ""
      }
      if (master_departure == false) {
        master_departure = ""
      }
      if (card_pay == false) {
        card_pay = ""
      }
      if (free_diagnostics == false) {
        free_diagnostics = ""
      }
      if (quick_repair == false) {
        quick_repair = ""
      }
      if (pay_after_repair == false) {
        pay_after_repair = ""
      }
      if (own_warehouse == false) {
        own_warehouse = ""
      }
      if (free_parking == false) {
        free_parking = ""
      }
      if (fix_price == false) {
        fix_price = ""
      }
      this.loader = true
      this.page_Pagination = 1
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        })
      }, 250)
      await this.$axios
        .$get(
          "api/v1/companies/?" +
            `page=1&servicesslug=${this.$route.params.slug}&` +
            `subdomain=${this.subdomain}&` +
            `free_diagnostics=${free_diagnostics}&` +
            `quick_repair=${quick_repair}&` +
            `pay_after_repair=${pay_after_repair}&` +
            `own_warehouse=${own_warehouse}&` +
            `free_parking=${free_parking}&` +
            `fix_price=${fix_price}&` +
            `cash_pay=${cash_pay}&` +
            `card_pay=${card_pay}&` +
            `courier_departure=${courier_departure}&` +
            `master_departure=${master_departure}`,
          {}
        )
        .then((resp) => {
          setTimeout(() => {
            console.log(resp.results.companies[0])
            this.resp_data = resp
          }, 50)

          let filter_params =
            `&servicesslug=${this.$route.params.slug}` +
            `&subdomain=${this.subdomain}&` +
            `free_diagnostics=${free_diagnostics}&` +
            `quick_repair=${quick_repair}&` +
            `pay_after_repair=${pay_after_repair}&` +
            `own_warehouse=${own_warehouse}&` +
            `free_parking=${free_parking}&` +
            `fix_price=${fix_price}&` +
            `cash_pay=${cash_pay}&` +
            `card_pay=${card_pay}&` +
            `courier_departure=${courier_departure}&` +
            `master_departure=${master_departure}`
          this.filter_params = filter_params
          this.$router.push(
            `/services/${this.$route.params.slug}/` +
              `?page=${this.page_Pagination}` +
              filter_params
          )
          setTimeout(() => {
            this.importantFilters()
          }, 50)
          setTimeout(() => {
            this.loader = false
          }, 50)
        })
        .catch((error) => {
          // console.log(error)
          this.loader = false
        })
    },
  },
}
</script>
