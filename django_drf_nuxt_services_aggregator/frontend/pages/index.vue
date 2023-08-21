<template>
  <div class="container">
    <section id="statistic-city" class="mb-4">
      <h3>
        Статистика по городу {{ $store.getters["cities/activeCity"].name }}
      </h3>
      <div class="row row-cols-1 row-cols-md-3 row-cols-lg-3 g-3">
        <!--<div v-for="i in 3" :key="i.id">
          <div class="box-statistic d-flex flex-column">
            <span class="text-statistic">{{ companies_count }}</span>
            <span class="text-statistic">сервисов</span>
          </div>
        </div>-->
        <div>
          <div class="box-statistic d-flex flex-column">
            <span class="text-statistic">{{ count.category_count }}</span>
            <span class="text-statistic">категорий</span>
          </div>
        </div>
        <div>
          <div class="box-statistic d-flex flex-column">
            <span class="text-statistic">{{ count.company_count }}</span>
            <span class="text-statistic">сервисных центров</span>
          </div>
        </div>
        <div>
          <div class="box-statistic d-flex flex-column">
            <span class="text-statistic">{{ count.point_count }}</span>
            <span class="text-statistic">мастерских</span>
          </div>
        </div>
      </div>
    </section>

    <section id="statistic-city" class="mb-4">
      <h3>Сервисные центры по видам техники</h3>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
        <CardsService
          v-for="category in categories.slice(0, 9)"
          :key="category.id"
          :category="category"
        />
      </div>
      <div class="all-services">
        <Nuxt-link to="/categories">Смотреть все виды техники</Nuxt-link>
      </div>
    </section>

    <section id="manufacturerss">
      <h3>Производители</h3>
      <div class="row">
        <div
          v-for="brand in brands.slice(0, 30)"
          :key="brand.id"
          class="col-lg-2 col-12"
        >
          <div class="box-manufacturerss">
            <Nuxt-link :to="`/brands/${brand.slug}`"
              ><img width="36" height="36" :src="brand.logo" alt=""
            /></Nuxt-link>
          </div>
          <p class="text-center mt-4">
            <Nuxt-link
              style="text-decoration: none; color: white"
              :to="`/brands/${brand.slug}`"
            >
              {{ brand.name }}
            </Nuxt-link>
          </p>
        </div>
      </div>
      <div class="all-services">
        <Nuxt-link to="/brands">Все Бренды</Nuxt-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_r}`,
      meta: [
        {
          hid: `description`,
          name: "description",
          content: `Услуги сервисных центров ${this.$store.getters["cities/activeCity"].declension_r}`,
        },
        {
          hid: `og:title`,
          name: "og:title",
          content: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_r}`,
        },
        {
          hid: `og:description`,
          name: "og:description",
          content: `Услуги сервисных центров ${this.$store.getters["cities/activeCity"].declension_r}`,
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
  async asyncData({ $axios, req, store, route }) {
      let  subdomain
      try {
          subdomain = store.getters["cities/activeCity"].subdomain.name
      } catch (error) {
          subdomain =  'moscow'
      }

    // const subdomain = store.getters["cities/activeCity"].subdomain;
    const services = await $axios.get(
      `/api/v1/services/all-services-city?slug_city=${subdomain}`
    );
    let params = `subdomain=${subdomain}`;
    const resp_data = await $axios.get(`/api/v1/companies/?${params}`);
    return {
      services: services.data,
      companies_count: resp_data.data.count,
    };
  },
  async fetch({ store }) {
    if (store.getters["brands/brands"].length === 0) {
      await store.dispatch("brands/fetch");
    }
    if (store.getters["categories/categories"].length === 0) {
      await store.dispatch("categories/fetch");
    }
  },
  mounted() {
    let cities = [];
    this.cities = cities;
    this.OnCount();
  },
  data() {
    return {
      cities: [],
      count: {
        category_count: 0,
        point_count: 0,
        company_count: 0,
      },
      brands: this.$store.getters["brands/brands"],
      categories: this.$store.getters["categories/categories"],
    };
  },
  methods: {
    OnPage(url) {
      this.$router.push(url);
    },
    async OnCount() {
      let slug;
      try {
        slug = this.$store.getters["cities/activeCity"].subdomain.name;
      } catch (error) {
        console.log("err", this.$store.getters["cities/activeCity"]);
        slug = "moscow";
      }

      await this.$axios
        .get(`api/v1/companies/count/?subdomain=${slug}`)
        .then((resp) => {
          this.count = resp.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    onPAgeSlug(data_category, slug) {
      this.$store.commit("url_page/SetGroup_name_url", data_category);
      this.$store.commit("url_page/Setvalue_url", slug);
      this.$cookies.set("value_url", slug, {
        path: `/`,
        maxAge: 60 * 60 * 24 * 7,
      });
      this.$cookies.set("group_name_url", data_category, {
        path: `/`,
        maxAge: 60 * 60 * 24 * 7,
      });
      this.$router.push(`/${slug}`);
    },
  },
};
</script>

<style lang="scss">
section {
  h3 {
    margin-bottom: 1.2rem;
  }
}

.header_page {
  margin-right: auto;
  margin-left: auto;
  background-image: linear-gradient(rgba(0, 0, 0, 0.29), rgba(0, 0, 0, 0.66)),
    url("https://servicerating.ru/main-d.jpg");
  background-size: cover;
  box-shadow: 0 1px 5px hsl(0deg 0% 86% / 50%);
  box-sizing: border-box;
  padding: 100px 25px;
  color: white;
}
#header_page {
  background-position: 50% 0;
  background-repeat: no-repeat;
  background-attachment: initial;
  box-shadow: 0 1px 5px hsla(0,0%,85.9%,.5);
  color: #fff;
  width: 100%;
  height: 100%;
  background-size: cover !important;
}

.box-statistic {
  min-height: 10vh;
  background: #1a2861;
  padding: 1em;
  display: flex;
  align-items: center;
  justify-content: center;
  /* transform: skewX(-10deg); */
  border-radius: 5px;
  box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 10%);
}

.text-statistic {
  color: white;
  font-size: 1.5em;
}

.box-popular-services {
  cursor: pointer;
  background: #fff;
  align-items: center;
  margin-top: 1em;
  padding: 1em;
  min-height: 3vh;
  box-shadow: 0 1px 5px hsl(0deg 0% 86% / 50%);
}

.all-services {
  margin-top: 3em;
  width: 100%;
  background: transparent;
  box-shadow: none;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 5vh;
}
main > .my-3 {
  margin-top: 0px !important;
}
.box-services__subcategories .item-category {
  display: block;
  float: left;
  background: #4089f8;
  color: #fff;
  padding: 4px 8px 5px;
  margin: 0 5px 5px 0;
  border-radius: 3px;
}
.box-services__inner {
  border-radius: 5px;
  box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 10%);
}
.all-services a {
  background: linear-gradient(340deg, #b7dcfb, #ffffff);
  border-radius: 56px;
  box-shadow: 1px 1px 3px 0 rgb(0 0 0 / 20%);
  padding: 7px 23px;
  color: #333;
  text-decoration: none;
}
.box-manufacturerss > a > img {
  width: auto;
  max-width: 100%;
}
#manufacturerss{
  margin-top: 50px;
}
@media all and(max-width: 767px) {
  #manufacturerss > .row > .col-12 {
    width: 50%;
  }
  #manufacturerss > .row > .col-12 a img {
    width: auto;
    max-width: 100%;
  }
}
</style>
