<template>
  <div>
    <!-- <div v-if="loader" class="loader-page">
      <div
        style="position: absolute; left: 50%; top: 50%"
        :size="50"
        color="rgb(59, 118, 234)"
        indeterminate
        class="spinner-border text-primary"
        role="status"
      >
        <span class="visually-hidden"></span>
      </div>
    </div> -->

    <!-- <FormsSearchCompany /> -->

    <!-- <div class="container">
      <h2>Бренд: {{ brand_name.name }}</h2>
    </div> -->

    <PagesCompanies
      :companies="resp_data"
      :name_slug="`Сервисные центры ${brand_name.name} в ${$store.getters['cities/activeCity'].declension_p}`"
      :list_companies="resp_data.results.companies"
      :OnFilters="OnFilters"
      :RemoveFilter="RemoveFilter"
      :list_categories="list_categories"
      :brand="brand_name"
    />

    <div class="container d-flex justify-content-center my-4">
      <pagination :options="options" v-model="page_Pagination" :records="resp_data.count" />
    </div>
  </div>
</template>

<script>
import Paginate from  '@/components/Paginate.vue'
export default {
//   layout: "brands",

  async asyncData({ $axios, req, store, route }) {
     let subdomain;
    try {
      subdomain = store.getters["cities/activeCity"].subdomain.name;
    } catch (error) {
      subdomain = "moscow";
    }

    let page = route.query.page || 1;
    let params;
    if (Object.keys(route.query).length > 1) {
      // console.log("params")
      params =
        `page=${page}&brands=${route.params.slug}&` +
        `subdomain=${subdomain}&` +
        `free_diagnostics=${route.query.free_diagnostics || ""}&` +
        `quick_repair=${route.query.quick_repair || ""}&` +
        `pay_after_repair=${route.query.pay_after_repair || ""}&` +
        `own_warehouse=${route.query.own_warehouse || ""}&` +
        `free_parking=${route.query.free_parking || ""}&` +
        `fix_price=${route.query.fix_prices || ""}&` +
        `cash_pay=${route.query.cash_pay || ""}` +
        `&card_pay=${route.query.card_pay || ""}`;
    } else {
      params = `page=${page}&subdomain=${subdomain}&brands=${route.params.slug}`;
    }
    const resp_data = await $axios.get(`/api/v1/companies/?${params}`);
    let list_categories = [];
    for (let company of resp_data.data.results.companies) {
      for (let category of company.subcategories) {
        if (!category.important) {
          list_categories.push(category);
        }
      }
    }

    const brand_name = await $axios.get(`/api/v1/brands/${route.params.slug}/`);
    return {
      resp_data: resp_data.data,
      brand_name: brand_name.data,
      subdomain: subdomain,
      list_categories: list_categories,
    };
  },

  head() {
    return {
      // title: `Сервисные центры по ремонту техники бренда ${this.brand_name.name} в городе ${this.$store.getters["cities/activeCity"].declension_p}`,
      // Сервисные центры Asus в CПб – адреса, цены | Ремонт Asus
      title: `Сервисные центры ${this.brand_name.name} в ${this.$store.getters["cities/activeCity"].declension_p} – адреса, цены | Ремонт ${this.brand_name.name}`,
      meta: [
        {
          hid: 'description',
          property: "description",
          content: `${this.resp_data.count} сервисный центр ${this.brand_name.name} в ${this.$store.getters["cities/activeCity"].declension_p}: удобный поиск, просмотр на карте, рейтинг, адреса, телефоны, время работы, цены и отзывы`
        },

        {
          hid: 'og:title',
          property: "og:title",
          content: `Сервисные центры ${this.brand_name.name} в ${this.$store.getters["cities/activeCity"].declension_p} – адреса, цены | Ремонт ${this.brand_name.name}`
        },
        {
          hid: 'og:description',
          property: "og:description",
          content: `${this.resp_data.count} сервисный центр ${this.brand_name.name} в ${this.$store.getters["cities/activeCity"].declension_p}: удобный поиск, просмотр на карте, рейтинг, адреса, телефоны, время работы, цены и отзывы`
        },
        // TODO: og:url
        // {
        //   hid: `og:url`,
        //   name: "og:url",
        //   content: `https://sankt-peterburg.servis-centers.ru`,
        // },
      ],
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
            options: {
        chunk: 10,
        template: Paginate
      },
    };
  },
  watch: {
    search(newValue, oldValue) {
      console.log(newValue);
    },
    page_Pagination(val) {
      this.pageData();
    },
  },
    mounted() {
    let width = window.innerWidth;
    if (width < 960) {
        console.log(555);
      this.options.chunk = 5

    }
  },
  computed: {
    rows() {
      return Math.ceil(this.resp_data.count / 5);
    },
    list_companies() {
      if (!this.filter && !this.search) {
        this.companies = this.resp_data.results.companies;
      }
      return this.companies;
    },
    category_page() {
      return this.$store.getters["url_page/value_url"];
    },
    category_page_url() {
      return this.$store.getters["url_page/group_name_url"];
    },
  },
  methods: {
    importantFilters() {
      let list_categories = [];
      for (let company of this.resp_data.results.companies) {
        for (let category of company.subcategories) {
          if (!category.important) {
            list_categories.push(category);
          }
        }
      }
      this.list_categories = list_categories;
    },
    async pageData() {
      let url;
      if (Object.keys(this.$route.query).length > 1) {
        url = `api/companies/?page=${this.page_Pagination}&${this.filter_params}`;
        this.$router.push(
          `/brands/${this.$route.params.slug}/` +
            `?page=${this.page_Pagination}` +
            `&${this.filter_params}`
        );
      } else {
        url = `api/v1/companies/?page=${this.page_Pagination}&subdomain=${this.subdomain}&brands=${this.$route.params.slug}`;
        this.$router.push(
          `/brands/${this.$route.params.slug}/` +
            `?page=${this.page_Pagination}`
        );
      }
      this.loader = true;
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 250);

      await this.$axios
        .$get(url, {})
        .then((resp) => {
          this.resp_data = resp;

          setTimeout(() => {
            this.importantFilters();
          }, 50);
          setTimeout(() => {
            this.loader = false;
          }, 50);
        })
        .catch((error) => {
          this.loader = false;
          // console.error(error)
        });
    },
    async RemoveFilter() {
      let url = `api/v1/companies/?page=${this.page_Pagination}&subdomain=${this.subdomain}&brands=${this.$route.params.slug}`;
      this.loader = true;
      this.filter = false;
      this.filter_params = "";
      this.page_Pagination = 1;
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 250);
      await this.$axios
        .$get(url, {})
        .then((resp) => {
          this.resp_data = resp;

          this.$router.push(`/brands/${this.$route.params.slug}`);
          setTimeout(() => {
            this.importantFilters();
          }, 50);
          setTimeout(() => {
            this.loader = false;
          }, 50);
        })
        .catch((error) => {
          this.loader = false;
          // console.error(error)
        });
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
      this.filter = true;
      if (cash_pay == false) {
        cash_pay = "";
      }
      if (courier_departure == false) {
        courier_departure = "";
      }
      if (master_departure == false) {
        master_departure = "";
      }
      if (card_pay == false) {
        card_pay = "";
      }
      if (free_diagnostics == false) {
        free_diagnostics = "";
      }
      if (quick_repair == false) {
        quick_repair = "";
      }
      if (pay_after_repair == false) {
        pay_after_repair = "";
      }
      if (own_warehouse == false) {
        own_warehouse = "";
      }
      if (free_parking == false) {
        free_parking = "";
      }
      if (fix_price == false) {
        fix_price = "";
      }
      this.loader = true;
      this.page_Pagination = 1;
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 250);
      await this.$axios
        .$get(
          "api/v1/companies/?" +
            `page=1&brands=${this.$route.params.slug}&` +
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
            console.log(resp.results.companies[0]);
            this.resp_data = resp;
          }, 50);

          let filter_params =
            `&brands=${this.$route.params.slug}` +
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
            `master_departure=${master_departure}`;
          this.filter_params = filter_params;
          this.$router.push(
            `/brands/${this.$route.params.slug}/` +
              `?page=${this.page_Pagination}` +
              filter_params
          );
          setTimeout(() => {
            this.importantFilters();
          }, 50);
          setTimeout(() => {
            this.loader = false;
          }, 50);
        })
        .catch((error) => {
          // console.log(error)
          this.loader = false;
        });
    },
  },
};
</script>

<style>
.loader-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  padding-top: 200px;
  font-size: 30px;
  font-family: sans-serif;
  z-index: 1;
}
</style>
