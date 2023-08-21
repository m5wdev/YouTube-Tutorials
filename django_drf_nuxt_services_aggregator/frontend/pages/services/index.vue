<template>
  <div class="container">
    <div v-if="loader" class="loader-page">
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
    </div>
    <div class="row">
      <div
        v-for="service in services"
        :key="service.id"
        class="col-lg-4 col-12"
      >
        <div
          @click="$router.push(`/services/${service.slug}`)"
          class="box-popular-services d-flex flex-column"
        >
          <!-- <img
            width="36px"
            src="https://servicerating.ru/images/main/uslugi/ustanovka-i-nastroyka-windows.png"
            alt=""
          /> -->
          <span>{{ service.name }}</span>
        </div>
      </div>
    </div>
    <div class="container d-flex justify-content-center my-4">
      <Pagination v-model="page_Pagination" :records="services.count" />
    </div>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: `Популярные Услуги сервисных центров в городе ${this.$store.getters["cities/activeCity"]}`,
      meta: [
        {
          hid: `description`,
          name: "description",
          content: `Популярные Услуги сервисных центров в городе ${this.$store.getters["cities/activeCity"]}`,
        },
        {
          hid: `keywords`,
          name: "keywords",
          content: ``,
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
  async asyncData({ $axios, store, req, route }) {
    let subdomain = store.getters["cities/activeCity"].subdomain.name;
    let page = route.query.page || 1;
    const services = await $axios.get(
    //   `/api/v1/services/city/${subdomain}/?}`
    `/api/v1/services/all-services-city?slug_city=${subdomain}`
    );
    return { services: services.data, subdomain: subdomain };
  },
  mounted() {
    this.page_Pagination = this.$route.query.page || 1;
  },

  data() {
    return {
      page_Pagination: 1,
      loader: false,
    };
  },
  watch: {
    page_Pagination(val) {
      this.pageData();
    },
  },
  methods: {
    async pageData() {
      let url;

      url = `/api/v1/services/city/${this.subdomain}/?page=${this.page_Pagination}`;
      this.$router.push(`/services` + `?page=${this.page_Pagination}`);

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
          this.services = resp;

          setTimeout(() => {
            this.loader = false;
          }, 50);
        })
        .catch((error) => {
          this.loader = false;
          // console.error(error)
        });
    },
  },
};
</script>


<style >
.box-popular-services {
  cursor: pointer;
  background: #fff;
  align-items: center;
  margin-top: 1em;
  padding: 1em;
  min-height: 3vh;
  box-shadow: 0 1px 5px hsl(0deg 0% 86% / 50%);
}
</style>
