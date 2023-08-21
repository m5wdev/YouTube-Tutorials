<template>
  <div>
    <Breadcrumbs
      :paths="[{ to: '/companies', name: 'Компании' }, ]"
      :current_page="company.name"
    />

    <div class="container">
      <div class="col-lg-12 col-sm-12 company-top-line">
        <div class="company-top-line_left">
          <div class="company-title">
            <h1 class="mb-0">{{ title }}</h1>
          </div>
        </div>

        <template v-if="company.logo">
          <div class="company-top-line_right company-review-link" v-if="company.logo.indexOf('.') > -1">
            <div class="company-logo">
              <img :src="company.logo" :alt="company.name" />
            </div>
          </div>
        </template>
      </div>
    </div>

    <div class="container mt-4 company-content">
      <div class="row">
        <div class="col-12 col-lg-8 col-xl-9">
          <!-- Карта -->
          <section id="section-title" class="card-company">
            <div class="overflow-hidden">
              <FormsYandexCard
                :firstPoint="firstPoint"
                :zoom="zoom"
                :company="company"
                :points="company.points"
              />
            </div>
          </section>

          <section id="section-about" class="card-company">
            <div class="mb-4">
              <h4>О сервисе</h4>
            </div>
            <!-- доп услуги -->
            <template
              v-if="
                company.courier_departure ||
                company.master_departure ||
                company.free_diagnostics ||
                company.quick_repair ||
                company.pay_after_repair ||
                company.own_warehouse ||
                company.free_parking ||
                company.fix_price ||
                company.cash_pay ||
                company.card_pay
              "
            >
              <div class="row row-cols-3 row-cols-lg-5 g-3 dop-services">
                <div
                  v-if="company.courier_departure"
                  class="courier_departure service-card col company-option"
                >
                  <div>Выезд курьера</div>
                </div>

                <div
                  v-if="company.master_departure"
                  class="master_departure service-card col company-option"
                >
                  <div>Выезд мастера</div>
                </div>

                <div
                  v-if="company.free_diagnostics"
                  class="free_diagnostics service-card col company-option"
                >
                  <div>Бесплатная диагностика</div>
                </div>

                <div
                  v-if="company.quick_repair"
                  class="quick_repair service-card col company-option"
                >
                  <div>Срочный ремонт</div>
                </div>
                <div
                  v-if="company.pay_after_repair"
                  class="pay_after_repair service-card col company-option"
                >
                  <div>Ремонт без предоплаты</div>
                </div>
                <div
                  v-if="company.own_warehouse"
                  class="own_warehouse service-card col company-option"
                >
                  <div>Собственный склад запчастей</div>
                </div>
                <div
                  v-if="company.free_parking"
                  class="free_parking service-card col company-option"
                >
                  <div>Бесплатная парковка</div>
                </div>
                <div
                  v-if="company.fix_price"
                  class="fix_price service-card col company-option"
                >
                  <div>Фиксированная стоимость ремонта</div>
                </div>
                <div
                  v-if="company.cash_pay"
                  class="cash_pay service-card col company-option"
                >
                  <div>Оплата наличными</div>
                </div>
                <div
                  v-if="company.card_pay"
                  class="card_pay service-card col company-option"
                >
                  <div>Оплата картой</div>
                </div>
              </div>
            </template>

            <!-- описание компании -->
            <template v-if="company.body">
              <hr />
              <div v-html="company.body" class="company-description"></div>
            </template>

            <!-- галерея -->
            <template v-if="company.images">
              <hr />
              <div id="images-gallery" class="row row-cols-3 row-cols-lg-4 g-3">
                <div
                  class="col gallery-img"
                  v-for="(gorsel, gorselIndex) in company.images"
                  :key="gorselIndex"
                  @click="index = gorselIndex"
                >
                  <img :src="gorsel.image" :alt="company.name" />
                </div>
                <TestGallery
                  :images="company.images"
                  :index="index"
                  :disable-scroll="false"
                  @close="index = null"
                />
              </div>
            </template>
          </section>

          <template v-if="categoriesServices.length > 0">
            <!-- услуги и цены -->
            <section id="servicec-categories" class="card-company">
              <div class="mb-4">
                <h4>Услуги и цены</h4>
              </div>
              <div
                v-for="category in categoriesServices"
                :key="category.id"
                class="my-4"
              >
                <div class="service-block">
                  <div class="h5">{{ category.name }}</div>
                  <table class="table table-striped table-hover">
                    <thead>
                      <tr>
                        <th scope="col">Услуга</th>
                        <th scope="col">Цена (руб)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="service in category.service" :key="service.id">
                        <td>{{ service.name }}</td>
                        <td style="width: 25%">
                          <template v-if="service.price">
                            от {{ service.price }}
                          </template>
                          <template v-if="service.price_max">
                            до {{ service.price_max }}
                          </template>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          </template>

          <!-- виды техники -->
          <section id="tech-types" class="card-company">
            <div class="mb-4">
              <h4>Виды техники</h4>
            </div>
            <div class="row row-cols-3 row-cols-lg-4 g-3">
              <div
                v-for="category in company.subcategories"
                :key="category.id"
                class="col tech-item"
              >
                <div class="p-3 border bg-light">
                  {{ category }}
                </div>
              </div>
            </div>
          </section>

          <!-- бренды -->
          <section id="section-brands" class="card-company">
            <div class="mb-4">
              <h4>Бренды</h4>
            </div>
            <div class="row row-cols-3 row-cols-lg-6 g-2">
              <div v-for="brand in company.brands" :key="brand.id" class="col brand-item">
                <Nuxt-Link :to="`/brands/${brand.slug}`">{{
                  brand.name
                }}</Nuxt-Link>
              </div>
            </div>
          </section>

          <!-- виджет отзывов яндекс карт -->
          <section id="section-list-comments" class="card-company" v-if="company.ya_id">
            <div class="row">
              <div class="col-12">
                <div style="width: 100%; height: 800px; overflow: hidden; position: relative; text-align: center;">
                  <iframe style="width: 760px; max-width: 100%; height: 100%; border: 0px solid #e6e6e6; border-radius: 8px; box-sizing: border-box;"
                    :src="`https://yandex.ru/maps-reviews-widget/${company.ya_id}?comments`"
                  ></iframe
                  ><a
                    :href="`https://yandex.ru/maps/org/${company.ya_id}/`"
                    target="_blank"
                    style="box-sizing: border-box; text-decoration: none; color: #b3b3b3; font-size: 10px; font-family: YS Text, sans-serif; padding: 0 20px; position: absolute; bottom: 8px; width: 100%; text-align: center; left: 0; overflow: hidden; text-overflow: ellipsis; display: block; max-height: 14px; white-space: nowrap; padding: 0 16px; box-sizing: border-box; "
                    >{{ company.name }}</a
                  >
                </div>
              </div>
            </div>
          </section>

          <template v-if="company.often_repair.length > 0">
            <!-- бренды часто ремонтируемые -->
            <section
              id="section-recently-fixed"
              class="popular often-repair card-company"
            >
              <div class="mb-4">
                <h4>Часто ремонтируемые</h4>
              </div>
              <div class="d-flex flex-wrap">
                <div
                  class="fix-item"
                  v-for="item in company.often_repair"
                  :key="item.id"
                >
                  <button
                    @click="OnPageCatBrand(item)"
                    type="button"
                    class="btn btn-sm btn-outline-secondary"
                  >
                    {{ item.name }}
                    <span v-if="item.brands_name">{{
                      item.brands_name[0]
                    }}</span>
                  </button>
                </div>
              </div>
            </section>
          </template>

          <div class="alert alert-warning" role="alert">
            <div class="text-center">
              Вы владелец этой компании? Зарегистрируйтесь и Вы сможете изменять
              информацию о компании, отвечать на отзывы и вопросы
            </div>
            <div class="mt-3 text-center">
              <Nuxt-Link class="btn btn-primary" to="/registration">
                Регистрация владельца
              </Nuxt-Link>
            </div>
          </div>
        </div>

        <aside class="col-12 col-lg-4 col-xl-3">
          <div id="contacts-card" class="card-company">
            <div class="d-grid gap-3">
              <!-- телефон компании components/company/HiddenPhone.vue -->
              <template v-if="company.phone">
                <span class="phone-button">
                  <CompanyHiddenPhone :phone="company.phone" />
                </span>
              </template>

              <button
                type="button"
                class="btn btn-success company-order-button"
                data-bs-toggle="modal"
                data-bs-target="#companyApplicationModal"
              >
                Оставить заявку
              </button>

              <a
                href="#section-list-comments"
                class="btn btn-primary link-to-reviews"
                >Отзывы и оценки</a
              >
            </div>

            <hr />

            <div v-if="company.email" class="left-col-email">
              <div>Email компании</div>
              <!-- email  components/company/HiddenEmail.vue-->
              <CompanyHiddenEmail :email="company.email" />
              <hr />
            </div>

            <!-- {{ company.points }} -->
            <template
              v-if="
                company.points.length > 0 &&
                'metro' in company.points[0] &&
                company.points[0].metro.length > 0
              "
            >
              <!-- список метро (мастерских) -->
              <div class="list-metro mb-3" v-if="'metro' in company.points[0]">
                <div class="h5 mb-3">Ближайшее метро</div>
                  <div v-if="company.points.length > 0" class="points-metro">
                    <template v-for="point in company.points">
                      <template
                        v-if="
                          point.city === $store.getters['cities/activeCity'].name
                        "
                      >
                        <div
                          v-for="metro in point.metro"
                          :key="metro.id"
                          class="mb-1 metro-container"
                        >
                          <!--  отдельно класс метро связан с именем метро его линии -->
                          <div
                            :class="'line-' + metro.metro_line"
                            class="metro-name btn btn-outline-secondary"
                          >
                            {{ metro.name }}
                          </div>
                        </div>
                      </template>
                    </template>
                  </div>
                <hr />
              </div>
            </template>

            <!-- адреса мастерских -->

            <template v-if="company.points.length">
              <div class="h5 mb-3">Адреса мастерских</div>
              <div v-for="point in company.points" :key="point.id" class="mb-3">
                <template

                >
                  <div class="small">
                    <address v-if="point.address" class="mb-1">
                      {{ point.city }}, {{ point.address }}
                    </address>
                    <!-- телефон компании -->
                    <div v-if="point.phone" class="mb-1">
                      <a :href="`tel:${point.phone}`">{{ point.phone }}</a>
                    </div>
                    <div v-if="point.work_time" class="mb-1 fst-italic">
                      {{ point.work_time }}
                    </div>
                  </div>

                  <div class="d-grid gap-2 button-position">
                    <button
                      @click="AddPointCart(point)"
                      class="btn see-yandex-card-btn btn-sm btn-outline-success"
                    >
                      Показать на карте
                    </button>
                  </div>
                </template>
              </div>
            </template>

            <div class="d-grid gap-3 mt-4">
              <!-- <button class="btn btn-outline-danger" type="button">
                Пожаловаться
              </button> -->
              <button
                type="button"
                class="btn btn-outline-danger"
                data-bs-toggle="modal"
                data-bs-target="#companyAbuseModal"
              >
                Пожаловаться
              </button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // layout: "company",

  beforeMount() {
    try {
      this.firstPoint = [
        this.company.points[0].latitude,
        this.company.points[0].longitude,
      ];
    } catch (error) {
      this.firstPoint = ["55.7558", "37.6173"];
    }
  },

  async asyncData({ route, $axios, store }) {
          let  subdomain
      try {
          subdomain = store.getters["cities/activeCity"].subdomain.name
      } catch (error) {
          subdomain =  'moscow'
      }

    const company = await $axios.get(
      `/api/v1/companies/company/${route.params.slug}/?subdomain=${subdomain}`
    );
    store.commit("company/SetCurrentCompany", company.data.company);

    const categoriesServices = await $axios.get(
      `/api/v1/services/company/${route.params.slug}/`
    );

    return {
      title: `${company.data.company.name} – сервисный центр в ${store.getters["cities/activeCity"].declension_p}`,
      company: company.data.company,
      // popular: company.data.popular,
      categoriesServices: categoriesServices.data,
    }
  },

  mounted() {
    // Schema.org
    const script_schema_org = document.createElement("script")
    script_schema_org.type = "application/id+json"

    const company_logo      = this.company.logo ? `"logo": "${this.company.logo}",` : ''
    const company_body      = this.company.body ? `"description": "${this.company.body}",` : ''
    const company_email     = this.company.email ? `"email": "${this.company.email}",` : ''
    const company_telephone = this.company.phone ? `"telephone": "${this.company.phone}",` : ''

    script_schema_org.innerHTML = `
      {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "${this.title}",
        "address": "${this.company.points[0].address_with_city}",
        ${company_logo}
        ${company_body}
        ${company_email}
        ${company_telephone}
      }
    `
    document.head.appendChild(script_schema_org)
    // END Schema.org
  },

  head() {
    return {
      title: this.title,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: `Адрес, телефон, часы работы сервис-центра ${this.company.name} ⭐ в ${this.$store.getters["cities/activeCity"].declension_p}. Отзывы о работе сервисного центра ${this.company.name}`,
        },
        {
          hid: 'og:title',
          name: 'og:title',
          content: `${this.company.name} – сервисный центр в ${this.$store.getters["cities/activeCity"].declension_p}, контакты, цены, отзывы`,
        },
        {
          hid: 'og:description',
          name: 'og:description',
          content: `Адрес, телефон, часы работы сервис-центра ${this.company.name} ⭐ в ${this.$store.getters["cities/activeCity"].declension_p}. Отзывы о работе сервисного центра ${this.company.name}`,
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
      firstPoint: [],
      zoom: 10,
      index: null,
    }
  },

  methods: {
    async AddPointCart(point) {
                    setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 50);
      this.firstPoint = [point.latitude, point.longitude];
      this.zoom = 15;

    },
    OnPageCatBrand(item) {
        let brand = null
        let category = item.slug
        if (item.slug.split('-').length > 1){
            brand = item.slug.split('-')[0]
            category = item.slug.split('-')[1]
        }
        if(item.slug.split('-').length > 2){
            category = item.slug.split('-')[1]+'-'+item.slug.split('-')[2]
        }
        if(item.slug.split('-').length === 2){
            category = item.slug.split('-')[1]
        }
        console.log(brand,category);
      if (brand) {
        this.$router.push(`/${category}/${brand}`);
        console.log(brand);
      } else {
        this.$router.push(`/${category}`);
      }
    },
  },
}
</script>

<style lang="scss" scoped>
// .Серпуховско-Тимирязевская {
//   color: green;
// }
#section-recently-fixed {
  .fix-item {
    margin: 0 10px 15px;
  }
}

#contacts-card {
  @media (min-width: 992px) {
    top: 120px;
  }
}

.card-company {
  background: white;
  padding: 1em;
  border-radius: 7px;

  &:not(:last-child) {
    margin-bottom: 30px;
  }
}

.service-card {
  text-align: center;

  img {
    width: 100%;
    height: auto;
    margin-bottom: 15px;
  }

  .h5 {
    margin-bottom: 0;
  }
}

#images-gallery {
  .gallery-img {
    overflow: hidden;

    * {
      transition: all ease-in-out .3s;
    }

    &:hover {
      cursor: pointer;

      img {
        opacity: .7;
      }
    }

    img {
      width: 100%;
      height: 100%;
    }
  }
}

#tech-types .tech-item {
  font-size: 1rem;
  line-height: 1.2;
  margin-top: 10px;
}
.company-top-line {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.company-top-line_left {
  width: 90%;
}
.company-top-line_right {
  width: 10%;
}
#contacts-card {
  box-shadow: 5px 5px 20px 0 rgb(0 0 0 / 30%);
  display: block;
  border-radius: 10px !important;
  padding: 1em;
  background: #fff !important;
  color: #333;
  text-shadow: none;
}
#section-about, #tech-types, #section-brands, #section-recently-fixed{
  border-radius: 10px !important;
  box-shadow: 5px 5px 20px 0 rgb(0 0 0 / 30%);
  display: block;
  background: rgba(255, 255, 255, 1) !important;
  color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.125);
}
#section-about h4, #tech-types h4, #section-brands h4, #section-recently-fixed h4{
  color: #323232;
  text-decoration: none;
  text-shadow: none;
}
.metro-container{
  padding: 0;
  margin-bottom: 10px !important;
  margin-right: 10px !important;
  transform: skewX(-10deg);
  border-radius: 2px;
}
.points-metro{
  display: flex;
  flex-wrap: wrap;
}
.btn.metro-name{
  padding: 0;
  border: none;
  background: transparent !important;
  color: #333;
  transform: skewX(10deg);
  display: flex;
  align-items: center;
  cursor: initial;
}
.btn.metro-name:before{
  content: "";
  display: block;
  margin-right: 7px;
  width: 8px;
  height: 8px;
  border-radius: 6px;
  background: #000;
}
.tech-item{
  width: initial !important;
}
.tech-item > .bg-light{
  width: 100%;
  height: 100%;
  color: #1e1e1e;
  border: 1px solid #d7d7d7 !important;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 7px 10px !important;
  background: #ffffff !important;
}
.brand-item > a{
  width: 100%;
  height: 100%;
  color: #fff;
  border: none !important;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 7px 10px !important;
  background: #2181dd !important;
  text-decoration: none;
  transition: all .2s ease-in-out;
}
.brand-item > a:hover, .brand-item > a:active{
  background: #405895 !important;
}
#images-gallery{
  padding: 0;
  border-radius: 5px;
  margin: 0 0px;
}
.service-card > div{
  white-space: nowrap;
}
.company-option{
  width: auto;
  max-width: initial;
  padding-right: 35px;
}
.dop-services{
  margin-left: 0;
}
.fix-item{
  margin-top: 10px !important;
  margin-bottom: 0 !important;
  margin-left: 0 !important;
}
.fix-item .btn{
  width: 100%;
  height: 100%;
  color: #fff;
  border: none !important;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 7px 10px !important;
  background: #2181dd !important;
  text-decoration: none;
}
.fix-item .btn:hover, .fix-item .btn:active{
  background: #405895 !important;
}
.card-company{
  background: white;
  padding: 1em;
  border-radius: 10px;
  box-shadow: 5px 5px 20px 0 rgb(0 0 0 / 30%);
}
.phone-button{
  display: block;
}
.phone-button .btn, .btn.link-to-reviews{
  width: 100%;
  background: #2181dd;
  border: none;
  border-radius: 5px;
}
.phone-button .btn:hover, .phone-button .btn:active, .btn.link-to-reviews:hover, .btn.link-to-reviews:active{
  background: #405895;
}
.company-order-button{
  border-radius: 50px;
  background: transparent;
  color: #333;
  border: 2px solid #333;
  box-shadow: 1px 1px 3px 0 rgb(0 0 0 / 20%);
  font-weight: 500;
}
.company-order-button:hover {
  border-radius: 50px;
  background: #3bb1ff;
  color: #fff;
  border: 2px solid #3bb1ff;
  box-shadow: 3px 3px 5px 0 rgb(0 0 0 / 20%);
  font-weight: 500;
}
.see-yandex-card-btn{
  width: fit-content;
  height: 100%;
  color: #333;
  border: none !important;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  padding: 7px 10px !important;
  background: #f1f1f1 !important;
  text-decoration: none;
  box-shadow: 1px 1px 3px 0 rgb(0 0 0 / 20%);
  text-align: left !important;
}
.see-yandex-card-btn:hover, .see-yandex-card-btn:active{
  box-shadow: 3px 3px 5px 0 rgb(0 0 0 / 20%);
  background: #ddf1ff !important;
}
.see-yandex-card-btn:before {
  content: "";
  width: 20px;
  height: 20px;
  background-image: url('/images/map-marker.svg');
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
  display: inline-block;
  margin-bottom: 0px;
  margin-right: 4px;
}
.button-position{
  justify-content: flex-start;
  padding-top: 6px;
}
.company-description{
  color: #333;
}
#images-gallery .gallery-img{
  padding-left: 0;
}
@media all and(max-width: 767px){
  .company-content > .row{
    flex-direction: column-reverse;
  }
  .company-content aside{
    margin-bottom: 30px;
  }
  .company-top-line_right{
    width: 40%;
    margin-top: 12px;
    margin-left: 20px;
  }
  .company-title h1{
    font-size: 20px;
  }
  .card-company .company-option {
    color: #fff;
    padding: 5px 10px;
    margin-top: 15px;
    background: #c7c7c7;
    margin-right: 15px;
    border-radius: 5px;
    transform: skewX(-10deg);
    text-shadow: none;
    color: #222;
    box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 10%), -5px -5px 10px 0 rgb(255 255 255);
    font-size: 16px;
    padding-right: 34px;
  }
  hr{
    background: #777;
  }
}

</style>
