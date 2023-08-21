<template>
  <div
    class="card mb-5"

    :class="{
       promo: company.is_promo && company.promo,
       'promo-item-1': company.is_promo && company.promo == 1,
       'promo-item-2': company.is_promo && company.promo == 2,
       'promo-item-3': company.is_promo && company.promo == 3,
       'promo-item-4': company.is_promo && company.promo == 4,
       'promo-item-5': company.is_promo && company.promo == 5,
       'promo-item-6': company.is_promo && company.promo == 6,
       'promo-item-7': company.is_promo && company.promo == 7,
       'promo-item-8': company.is_promo && company.promo == 8,
       'promo-item-9': company.is_promo && company.promo == 9,
       'promo-item-10': company.is_promo && company.promo == 10

    }"
  >
    <div class="card-body">
      <div class="card-header-new">
        <h3 class="comany-name card-title mb-3">
          <Nuxt-link
            v-if="$route.path.includes('profile')"
            :to="'/profile/companies/' + company.id"
          >
            {{ company.name }}
          </Nuxt-link>
          <Nuxt-link v-else :to="'/companies/' + company.slug">
            {{ company.name }}
          </Nuxt-link>
        </h3>
        <template v-if="company.logo">
          <div class="company-logo" v-if="IsLogoPresent(company)">
            <img :src="company.logo" :alt="company.name" />
          </div>
        </template>
      </div>
      <!-- телефон email компании -->
      <!-- путь к компонентам components/comapny/HiddenPhone и  components/comapny/HiddenEmail-->
      <div class="body-company card-text">
        <template v-if="company.phone">
          <CompanyHiddenPhone :phone="company.phone" />
        </template>
        <template v-if="company.email">
          <CompanyHiddenEmail :email="company.email" />
        </template>
      </div>
      <div class="card-text mt-3">
        <!-- Доп услуги(выезд куръера бесплатная парковка и т д) -->
        <div class="dop-services d-grid gap-2 d-sm-block">
          <div
            v-if="company.courier_departure"
            class="courier_departure company-option"
          >
            <span>Выезд курьера</span>
          </div>
          <div
            v-if="company.master_departure"
            class="master_departure company-option"
          >
            <span>Выезд мастера</span>
          </div>
          <div
            v-if="company.free_diagnostics"
            class="free_diagnostics company-option"
          >
            <span>Бесплатная диагностика</span>
          </div>
          <div v-if="company.quick_repair" class="quick_repair company-option">
            <span>Срочный ремонт</span>
          </div>
          <div
            v-if="company.pay_after_repair"
            class="pay_after_repair company-option"
          >
            <span>Ремонт без предоплаты</span>
          </div>
          <div
            v-if="company.own_warehouse"
            class="own_warehouse company-option"
          >
            <span>Собственный склад запчастей</span>
          </div>
          <div v-if="company.free_parking" class="free_parking company-option">
            <span>Бесплатная парковка</span>
          </div>
          <div v-if="company.fix_price" class="fix_price company-option">
            <span>Фиксированная стоимость</span>
          </div>
          <div v-if="company.cash_pay" class="cash_pay company-option">
            <span>Оплата наличными</span>
          </div>
          <div v-if="company.card_pay" class="card_pay company-option">
            <span>Оплата картой</span>
          </div>
          <div v-if="company.free_parking" class="free_parking company-option">
            <span>Бесплатная парковка</span>
          </div>
        </div>

        <!-- галерея -->
        <div v-if="company.images">
          <hr />
          <div id="images-gallery" class="row row-cols-3 row-cols-lg-6 g-3">
            <div
              class="gallery-img"
              v-for="(gorsel, gorselIndex) in company.images"
              :key="gorselIndex"
              @click="index = gorselIndex"
            >
              <img
                width="100"
                height="50"
                :src="gorsel.image"
                :alt="company.name"
              />

              <!-- <img :src="gorsel.image_thumbnail" :alt="company.name"> -->
            </div>
            <TestGallery
              :images="company.images"
              :index="index"
              :disable-scroll="false"
              @close="index = null"
            />
          </div>
        </div>
      </div>
      <!-- адреса мастерских -->
      <template v-if="company.points && company.points.length > 0">
        <div class="address-points py-3 mt-2">
          <div class="card-addresses">
            <template v-if="company.points.length > 0 && !showAddresses">
              <div>
                <span
                  @click="AddFirstPointMaps(company.points[0],company.name)"
                  v-if="company.points[0].address"
                >
                  <span class="map-tooltip">
                    <i>На карте</i>
                  </span>
                  {{ company.points[0].city }}, {{ company.points[0].address }}
                </span>
                <span v-if="company.points[0].work_time">{{
                  company.points[0].work_time
                }}</span>
              </div>
            </template>

            <template v-if="company.points.length > 1 && showAddresses">
              <div v-for="point in company.points" :key="point.id">
                <span @click="AddFirstPointMaps(point,company.name)" v-if="point.address">
                  <span class="map-tooltip">
                    <i>На карте</i>
                  </span>
                  {{ point.city }}, {{ point.address }}
                </span>
                <span v-if="point.work_time">{{ point.work_time }}</span>
              </div>
            </template>
          </div>

          <div
            v-if="company.points.length > 1"
            @click="showAddresses = !showAddresses"
            class="btn mb-2 btn-outline-primary show-more-addresses"
          >
            <template v-if="!showAddresses"> Показать все адреса </template>
            <template v-else> Скрыть все адреса </template>
          </div>
        </div>
      </template>

      <div class="text-end">
        <Nuxt-link
          v-if="$route.path.includes('profile')"
          :to="'/profile/companies/' + company.id"
        >
          <span class="btn mt-4 btn-success more-button">Подробнее...</span>
        </Nuxt-link>
        <Nuxt-link v-else :to="'/companies/' + company.slug">
          <span class="btn btn-success more-button">Подробнее...</span>
        </Nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["company"],


  data() {
    return {
      showAddresses: false,
      index: null,
    };
  },
  methods: {
    AddFirstPointMaps(point,company) {
        console.log(company);
      this.$store.commit("pointyandex/SetfirstPoint", [
        point.latitude,
        point.longitude,
      ]);
      this.$store.commit("pointyandex/SetPoint", [point]);
      this.$store.commit("pointyandex/SetCompany", company);
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 350);
    },
    IsLogoPresent(company) {
      if (company.logo.indexOf(".") > -1) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style lang="scss">
.card-addresses {
  max-height: 400px;
  overflow-y: auto;
}

.gallery-img {
  cursor: pointer;
  height: 70px;
  overflow: hidden;

  img {
    width: 100%;
    height: auto;
    min-height: 70px;
  }
}
@media all and(max-width: 767px) {
.company-option{
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
}
</style>
