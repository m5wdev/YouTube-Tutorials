<template>
  <div class="companies-content">
    <div class="container">
      <h1>{{ title }}</h1>
      <!-- заголовок страницы -->
      <div class="my-4 title-list-companies">
        <span class="sub-text">
          Найдено {{ companies.count }} сервисных центра по ремонту
          <span v-if="category">{{ category.declension_one_p }}</span>
          <span v-if="brand">бренда {{ brand.name }}</span> в
          {{ $store.getters["cities/activeCity"].declension_p }}
        </span>
      </div>
      <!-- список категорий и подкатегорий -->
      <div class="box-categories d-flex flex-wrap" v-if="list_categories">
        <div
          v-for="subcategory in list_categories.slice(0, 20)"
          :key="subcategory.id"
          @click="OnCategorySlug(subcategory)"
          class="category btn btn-outline-secondary m-1"
        >
          <span>{{ subcategory }}</span>
        </div>
      </div>
    </div>

    <div class="container mt-3">
      <div class="row">

        <div class="yandex-car col-12 mb-4" v-if="markerPoint.length >0">
          <CardsYandex :company="markerCompany" :point="markerPoint[0]" />
        </div>
        <!-- Список компани1 (карточки) путь /components/company/CardCompany.vue -->
        <div class="list-company col-12 col-lg-8 col-xl-9 order-2 order-lg-1">
          <CompanyCardCompany
            v-for="company in list_companies"
            :key="company.id"
            :company="company"
          />
          <!-- карта -->
        </div>

        <!-- Фильтры -->
        <aside
          class="
            filters
            col-12 col-lg-4 col-xl-3
            order-1 order-lg-2
            mb-5 mb-lg-0
          "
        >
          <div class="card-filter d-lg-block d-md-block d-none">
            <div class="h4">Фильтры</div>
            <hr />
            <div class="filter-group">
              <div class="fw-bold">Оплата</div>
              <div class="form-check ml-2">
                <input
                  id="cash_pay"
                  class="form-check-input"
                  type="checkbox"
                  v-model="cash_pay"
                />
                <label class="form-check-label" for="cash_pay">
                  Наличными
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="card_pay"
                  class="form-check-input"
                  type="checkbox"
                  v-model="card_pay"
                />
                <label class="form-check-label" for="card_pay"> Картой </label>
              </div>
            </div>

            <hr />

            <div class="filter-group">
              <div class="fw-bold">Другие услуги</div>
              <div class="form-check mb-2">
                <input
                  id="free_parking"
                  class="form-check-input"
                  type="checkbox"
                  v-model="free_parking"
                />
                <label class="form-check-label" for="free_parking">
                  Бесплатная парковка
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="own_warehouse"
                  class="form-check-input"
                  type="checkbox"
                  v-model="own_warehouse"
                />
                <label class="form-check-label" for="own_warehouse">
                  Собственный склад запчастей
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="pay_after_repair"
                  class="form-check-input"
                  type="checkbox"
                  v-model="pay_after_repair"
                />
                <label class="form-check-label" for="pay_after_repair">
                  Ремонт без предоплаты
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="quick_repair"
                  class="form-check-input"
                  type="checkbox"
                  v-model="quick_repair"
                />
                <label class="form-check-label" for="quick_repair">
                  Срочный ремонт
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="free_diagnostics"
                  class="form-check-input"
                  type="checkbox"
                  v-model="free_diagnostics"
                />
                <label class="form-check-label" for="free_diagnostics">
                  Бесплатная диагностика
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="master_departure"
                  class="form-check-input"
                  type="checkbox"
                  v-model="master_departure"
                />
                <label class="form-check-label" for="master_departure">
                  Выезд мастера
                </label>
              </div>
              <div class="form-check mb-2">
                <input
                  id="courier_departure"
                  class="form-check-input"
                  type="checkbox"
                  v-model="courier_departure"
                />
                <label class="form-check-label" for="courier_departure">
                  Выезд курьера
                </label>
              </div>

              <hr />

              <div class="d-grid gap-3">
                <button
                  @click="FilterCompanies"
                  type="button"
                  class="btn btn-primary"
                >
                  Применить
                </button>

                <button
                  @click="FilterDont"
                  type="button"
                  class="btn btn-outline-secondary"
                >
                  Сбросить
                </button>
              </div>
            </div>
          </div>
          <div class="card-filter d-block d-lg-none d-md-none">
            <div class="accordion accordion-flush" id="accordionFlushExample">
              <div class="accordion-item">
                <h2 class="accordion-header" id="flush-headingOne">
                  <button
                    class="accordion-button collapsed"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#flush-collapseOne"
                    aria-expanded="false"
                    aria-controls="flush-collapseOne"
                  >
                    Фильтры
                  </button>
                </h2>
                <div
                  id="flush-collapseOne"
                  class="accordion-collapse collapse"
                  aria-labelledby="flush-headingOne"
                  data-bs-parent="#accordionFlushExample"
                >
                  <div class="accordion-body">
                    <hr />
                    <div class="filter-group ">
                      <div class="fw-bold">Оплата</div>
                      <div class="form-check ml-2">
                        <input
                          id="cash_pay"
                          class="form-check-input"
                          type="checkbox"
                          v-model="cash_pay"
                        />
                        <label class="form-check-label" for="cash_pay">
                          Наличными
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="card_pay"
                          class="form-check-input"
                          type="checkbox"
                          v-model="card_pay"
                        />
                        <label class="form-check-label" for="card_pay">
                          Картой
                        </label>
                      </div>
                    </div>

                    <hr />

                    <div class="filter-group">
                      <div class="fw-bold">Другие услуги</div>
                      <div class="form-check mb-2">
                        <input
                          id="free_parking"
                          class="form-check-input"
                          type="checkbox"
                          v-model="free_parking"
                        />
                        <label class="form-check-label" for="free_parking">
                          Бесплатная парковка
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="own_warehouse"
                          class="form-check-input"
                          type="checkbox"
                          v-model="own_warehouse"
                        />
                        <label class="form-check-label" for="own_warehouse">
                          Собственный склад запчастей
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="pay_after_repair"
                          class="form-check-input"
                          type="checkbox"
                          v-model="pay_after_repair"
                        />
                        <label class="form-check-label" for="pay_after_repair">
                          Ремонт без предоплаты
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="quick_repair"
                          class="form-check-input"
                          type="checkbox"
                          v-model="quick_repair"
                        />
                        <label class="form-check-label" for="quick_repair">
                          Срочный ремонт
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="free_diagnostics"
                          class="form-check-input"
                          type="checkbox"
                          v-model="free_diagnostics"
                        />
                        <label class="form-check-label" for="free_diagnostics">
                          Бесплатная диагностика
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="master_departure"
                          class="form-check-input"
                          type="checkbox"
                          v-model="master_departure"
                        />
                        <label class="form-check-label" for="master_departure">
                          Выезд мастера
                        </label>
                      </div>
                      <div class="form-check mb-2">
                        <input
                          id="courier_departure"
                          class="form-check-input"
                          type="checkbox"
                          v-model="courier_departure"
                        />
                        <label class="form-check-label" for="courier_departure">
                          Выезд курьера
                        </label>
                      </div>

                      <hr />

                      <div class="d-grid gap-3">
                        <button
                          @click="FilterCompanies"
                          type="button"
                          class="btn btn-primary"
                        >
                          Применить
                        </button>

                        <button
                          @click="FilterDont"
                          type="button"
                          class="btn btn-outline-secondary"
                        >
                          Сбросить
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    "companies",
    "name_slug",
    "categoriesImportant",
    "list_companies",
    "OnFilters",
    "RemoveFilter",
    "list_categories",
    "brand",
    "category",
  ],
  computed: {
    markerPoint() {
      return this.$store.getters["pointyandex/Point"];
    },
        markerCompany() {
            console.log(this.$store.getters["pointyandex/companyName"]);
      return this.$store.getters["pointyandex/companyName"];
    },
  },
  mounted() {
    this.$store.commit("pointyandex/SetPoint", []);
    this.free_diagnostics = this.$route.query.free_diagnostics || false;
    this.quick_repair = this.$route.query.quick_repair || false;
    this.pay_after_repair = this.$route.query.pay_after_repair || false;
    this.own_warehouse = this.$route.query.own_warehouse || false;
    this.free_parking = this.$route.query.free_parking || false;
    this.fix_price = this.$route.query.fix_prices || false;
    this.cash_pay = this.$route.query.cash_pay || false;
    this.card_pay = this.$route.query.card_pay || false;

    this.is_promo = this.$route.query.is_promo || false;
    this.promo = this.$route.query.promo || null;
  },

  data() {
    return {
      // title: `Сервисные центры по ремонту бытовой техники ${this.name_slug ? this.name_slug + " " : ""}в ${this.$store.getters["cities/activeCity"].declension_p}`,
      // Ремонт стиральных машин Bosch в Санкт-Петербурге
      // title: `Ремонт ${this.name_slug ? this.name_slug + " " : ""}в ${this.$store.getters["cities/activeCity"].declension_p}`,
      title: this.name_slug,
      category_name: "",
      companies_list: [],
      courier_departure: false,
      master_departure: false,
      free_diagnostics: false,
      quick_repair: false,
      pay_after_repair: false,
      own_warehouse: false,
      free_parking: false,
      fix_price: false,
      cash_pay: false,
      card_pay: false,
      owner_register: false,
    };
  },

  methods: {
    async OnCategorySlug(name) {
      let url = `api/v1/categories/slug/${name}/`;

      await this.$axios
        .$get(url, {})
        .then((resp) => {
          this.$router.push(`/${resp.slug}`);
        })
        .catch((error) => {
          // console.error(error)
        });
    },
    FilterCompanies() {
      {
        this.OnFilters(
          this.free_diagnostics,
          this.quick_repair,
          this.pay_after_repair,
          this.own_warehouse,
          this.free_parking,
          this.fix_price,
          this.cash_pay,
          this.card_pay,
          this.courier_departure,
          this.master_departure,
          this.is_promo,
          this.promo
        );
      }
    },
    FilterDont() {
      this.free_diagnostics = false;
      this.quick_repair = false;
      this.pay_after_repair = false;
      this.own_warehouse = false;
      this.free_parking = false;
      this.fix_price = false;
      this.cash_pay = false;
      this.card_pay = false;
      this.courier_departure = false;
      this.master_departure = false;
      this.is_promo = false;
      this.promo = "";
      this.RemoveFilter();
    },
  },
};
</script>

<style lang="scss">
.form-check {
  &:hover {
    .form-check-input,
    .form-check-label {
      cursor: pointer;
    }
  }
}

.box-card {
  min-height: 20vh;
  background-position: 50%;
  height: 120px;
  background-size: cover;
  box-sizing: border-box;
  background-blend-mode: multiply;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-image: url("https://media.wired.com/photos/59269cd37034dc5f91bec0f1/master/pass/GoogleMapTA.jpg");
}
.card-filter {
  min-height: 30vh;
  background: white;
  border-radius: 12px;
  padding: 1;
  padding: 1em;
  background: #fff !important;
  color: #333;
  text-shadow: none;
}
@media (max-width: 960px) {
    .card-filter {
        min-height: 3vh;
    }
}
.companies-content {
  margin-top: 30px;
}
@media all and(max-width: 1024px) {
  .text-end {
    float: none;
    position: relative;
    margin-top: 15px;
    margin-left: 10px;
  }
}
@media all and(max-width: 767px) {
  .box-categories {
    flex-wrap: nowrap !important;
    width: 88vw;
    overflow-x: auto;
    margin: 0 auto 0 0;
  }
  .my-4.title-list-companies {
    color: #fff;
    display: inline-block;
    padding: 7px 10px;
    background: #192660;
    border: none;
    border-radius: 5px;
    transform: initial;
    margin-top: 6px !important;
  }
  .category.btn {
    font-size: 14px;
    margin-bottom: 15px !important;
    white-space: nowrap;
  }
  .companies-content > .container.mt-5 {
    margin-top: 1rem !important;
  }
  .companies-page-content .company-option, .list-company .company-option{
    margin-right: 0px;
    text-shadow: none;
    font-size: 0;
    background: transparent;
    box-shadow: none;
    padding: 0 0 0 10px;
  }
  .card-addresses > div > span + span {
    margin-top: 5px;
    margin-left: 0px;
  }
  .card-text > .btn + span {
    display: none;
  }
  .companies-list-content > .row {
    flex-direction: column-reverse;
  }
  .filters {
    order: -1;
    margin-bottom: 50px;
  }
  .company-option{
    position: relative;
  }
  .company-option:hover{
    z-index: 100;
  }
  .company-option:hover span{
    font-size: 14px;
    display: block;
    position: absolute;
    background: #fff;
    transform: skewX(10deg);
    padding: 5px 10px;
    border-radius: 3px;
    box-shadow: 3px 3px 5px 0 rgb(0 0 0 / 20%);
    left: -3px;
    top: 29px;
  }
}
</style>
