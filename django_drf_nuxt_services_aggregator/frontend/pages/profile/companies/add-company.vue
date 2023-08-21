<template>
  <div class="container">
    <div class="row mb-4">
      <h1>Добавить компанию</h1>
    </div>

    <div class="row">
      <div class="col-12 col-lg-7">
        <form v-on:submit.prevent="SaveCompany">
          <div id="form-company-add">
            <div class="row">
              <div class="col-12 col-lg-6 col-md-6">
                <div class="h5">Добавить логотип</div>
              </div>
              <div class="col-12 col-lg-6 col-md-6">
                <ImageLogoCompany
                  :logo_company="logo_company"
                  :AddLogo="AddLogo"
                  :autoProcessQueue="false"
                  :urlpath="`/api/v1/companies/add-logo/`"
                />
              </div>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="company_active"
                v-model="company.active"
              />
              <label class="form-check-label" for="company_active">
                Активная
              </label>
            </div>
            <div class="mb-3">
              <label for="company_name" class="form-label"
                >Название компании</label
              >
              <input
                required
                :class="{
                  textdanger: !company.name && !valid,
                }"
                type="text"
                class="form-control"
                id="company_name"
                placeholder="Сервисный Центр"
                v-model="company.name"
              />
              <span style="color: red" v-if="!valid && !this.company.name"
                >обязательное поле</span
              >
            </div>

            <div class="mb-3">
              <label for="company_body" class="form-label">Описание</label>
              <textarea
                :class="{
                  textdanger: !company.body && !valid,
                }"
                class="form-control"
                id="company_body"
                rows="3"
                v-model="company.body"
              ></textarea>
              <span style="color: red" v-if="!valid && !this.company.body"
                >обязательное поле</span
              >
            </div>
            <div class="mb-3">
              <label for="company_email" class="form-label">Email</label>
              <input
                required
                type="email"
                class="form-control"
                id="company_email"
                placeholder="company@example.com"
                v-model="company.email"
              />
              <span style="color: red" v-if="!valid && !this.company.email"
                >обязательное поле</span
              >
            </div>
            <div class="mb-3">
              <label for="company_url" class="form-label">Сайт</label>
              <input
                required

                class="form-control"
                id="company_url"
                type="url"
                placeholder="https://example.com"
                v-model="company.url"
              />
              <span style="color: red" v-if="!valid && !this.company.url"
                >обязательное поле</span
              >
            </div>
            <div class="mb-3">
              <label for="company_phone" class="form-label">Телефон</label>
              <input
                required
                v-mask="'+7 (###) ###-##-##'"
                :class="{
                  textdanger: !company.phone && !valid,
                }"
                type="text"
                class="form-control"
                id="company_phone"
                placeholder="+7 000 000-00-00"
                v-model="company.phone"
              />
              <span style="color: red" v-if="!valid && !this.company.phone"
                >обязательное поле</span
              >
            </div>

            <div class="row g-3 mb-3">
              <div class="col">
                <label for="company_min_price" class="form-label"
                  >Минимальная цена</label
                >
                <input
                  required
                    min="1"
                  type="number"
                  class="form-control"
                  id="company_min_price"
                  placeholder="000"
                  v-model="company.min_price"
                />
                <span
                  style="color: red"
                  v-if="!valid && !this.company.min_price"
                  >обязательное поле</span
                >
              </div>
              <div class="col">
                <label for="company_max_price" class="form-label"
                  >Максимальная цена</label
                >
                <input
                  required
                  :class="{
                    textdanger: !company.max_price && !valid,
                  }"
                  type="number"
                  class="form-control"
                  id="company_max_price"
                  placeholder="00000"
                  v-model="company.max_price"
                />
                <span
                  style="color: red"
                  v-if="!valid && !this.company.max_price"
                  >обязательное поле</span
                >
              </div>
            </div>

            <div class="row g-3 mb-3">
              <div class="col">
                <label for="company_number_of_employees" class="form-label"
                  >Количество работников</label
                >
                <input
                  required
                  :class="{
                    textdanger: !company.number_of_employees && !valid,
                  }"
                  type="number"
                  class="form-control"
                  id="company_number_of_employees"
                  placeholder="15"
                  v-model="company.number_of_employees"
                />
                <span
                  style="color: red"
                  v-if="!valid && !this.company.number_of_employees"
                  >обязательное поле</span
                >
              </div>
              <div class="col">
                <label for="company_year_of_foundation" class="form-label"
                  >Год основания</label
                >
                <input
                  required
                  :class="{
                    textdanger: !company.year_of_foundation && !valid,
                  }"
                  type="number"
                  class="form-control"
                  id="company_year_of_foundation"
                  placeholder="2008"
                  v-model="company.year_of_foundation"
                />
                <span
                  style="color: red"
                  v-if="!valid && !this.company.year_of_foundation"
                  >обязательное поле</span
                >
              </div>
            </div>
            <div class="mt-5" style="">
              <h5>Выбрать бренды</h5>
              <div v-for="(item, index) in ListInputBrands" :key="index">
                <FormsSearchData
                  :index="index"
                  :ListInputData="ListInputBrands"
                  :item="item"
                  :removeItemData="removeItemBrand"
                  UrlPath="/api/v1/brands/search/?search="
                  placeholder="Поиск Бренда"
                  :valid="valid"
                />
              </div>
              <div class="col-12 mt-4" style="text-align: start">
                <div
                  @click="
                    ListInputBrands.push({
                      id: (countbrand_id += 1),
                      name: '',
                      search_query: '',
                    })
                  "
                  class="btn btn-info"
                >
                  + Добавить бренд
                </div>
              </div>
            </div>

            <div class="mt-5" style="">
              <h5>Выбрать Категории</h5>

              <div v-for="(item, index) in ListInputCategory" :key="index">
                <FormsSearchData
                  :index="index"
                  :ListInputData="ListInputCategory"
                  :item="item"
                  placeholder="Поиск категории"
                  :removeItemData="removeItemCategory"
                  UrlPath="/api/v1/categories/search/?search="
                  :valid="valid"
                />
              </div>
              <div class="col-12 mt-4" style="text-align: start">
                <div
                  @click="
                    ListInputCategory.push({
                      id: (countcategory_id += 1),
                      category: '',
                    })
                  "
                  class="btn btn-info"
                >
                  + Добавить категорию
                </div>
              </div>
            </div>

            <div class="form-check mb-3" style="margin-top: 3em">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_courier_departure"
                v-model="company.courier_departure"
              />
              <label class="form-check-label" for="company_courier_departure">
                Выезд курьера
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_master_departure"
                v-model="company.master_departure"
              />
              <label class="form-check-label" for="company_master_departure">
                Выезд мастера
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_free_diagnostics"
                v-model="company.free_diagnostics"
              />
              <label class="form-check-label" for="company_free_diagnostics">
                Бесплатная диагностика
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_quick_repair"
                v-model="company.quick_repair"
              />
              <label class="form-check-label" for="company_quick_repair">
                Срочный ремонт
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_pay_after_repair"
                v-model="company.pay_after_repair"
              />
              <label class="form-check-label" for="company_pay_after_repair">
                Ремонт без предоплаты
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_own_warehouse"
                v-model="company.own_warehouse"
              />
              <label class="form-check-label" for="company_own_warehouse">
                Собственный склад запчастей
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_free_parking"
                v-model="company.free_parking"
              />
              <label class="form-check-label" for="company_free_parking">
                Бесплатная парковка
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_fix_price"
                v-model="company.fix_price"
              />
              <label class="form-check-label" for="company_fix_price">
                Фиксированная стоимость ремонта
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_cash_pay"
                v-model="company.cash_pay"
              />
              <label class="form-check-label" for="company_cash_pay">
                Оплата наличными
              </label>
            </div>
            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_card_pay"
                v-model="company.card_pay"
              />
              <label class="form-check-label" for="company_card_pay">
                Оплата картой
              </label>
            </div>

            <ImageManyImageCompany :AddImages="AddImages" />

            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="company_owner_register"
                v-model="company.owner_register"
              />
              <label class="form-check-label" for="company_owner_register">
                Владелец зарегистрирован
              </label>
            </div>

            <div class="h3 mt-4">Добавление Мастерской</div>
            <div
              v-for="(item, index) in pointsList"
              :key="item.id"
              class="col-12 mt-2"
            >
              <FormsCreatePoint
                :index="index"
                :pointsList="pointsList"
                :item="item"
                :removeItem="removeItem"
                :valid="valid"
              />
            </div>
            <div class="col-12 mt-4" style="text-align: end">
              <div @click="AddPoint" class="btn btn-info">+ Добавить еще</div>
            </div>
            <div class="mt-4 text-end">
              <button style="width: 100%" class="btn btn-success" type="submit">
                Сохранить
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  middleware: "auth",
  layout: "profile",
  data() {
    return {
      logo_company: null,
      urlRemovePhoto: "api/v1/delete-logo/",
      urlAddPhoto: "api/v1/add-logo/",
      paramname: "logo",
      countcategory_id: 1,
      images_company: [],
      Submit: false,
      autoProcessQueue: false,
      valid: true,
      formcompany: false,
      Submit: false,
      count_id: 1,
      countbrand_id: 1,
      ListInputCategory: [
        {
          id: 1,
          name: "",
        },
      ],
      ListInputBrands: [
        {
          id: 1,
          name: "",
        },
      ],
      pointsList: [
        {
          id: 1,
          company_id: null,
          active: true,
          name: "",
          phone: "+7",
          metro_id: 0,
          office: "",
          address: "",
          city_id: null,
          work_time: "",
          author: this.$store.state.auth.user.id,
        },
      ],
      company: {
        active: true,
        name: "",

        body: "dfdf",
        email: "tt@mail.ru",
        url: "https://ru.stackoverflow.com/qu",
        phone: "+7",
        logo: null,
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
        min_price: 5,
        author_id: this.$store.state.auth.user.id,
        max_price: 5,
        number_of_employees: 5,
        year_of_foundation: "5",
        is_promo: true,
      },
    };
  },
  methods: {
    AddLogo(photo) {
      this.logo_company = photo;
    },
    AddImages(images_company) {
      console.log("many images");
      this.images_company = images_company;
    },
    async SaveCompany() {
      const url = "/api/v1/companies/create/";
      this.company.brands_list_id = this.ListInputBrands;
      this.company.categories_list_id = this.ListInputCategory;
      let logo_company = this.logo_company;
      let images_company = this.images_company;

      await this.$axios
        .$post(url, this.company, {})
        .then((resp) => {
          if (logo_company) {
            setTimeout(() => {
              this.AddLogoCompany(resp.id, logo_company);
            }, 10);
          }
          setTimeout(() => {
            for (let image of images_company) {
              this.AddPhotoCompany(resp.id, image);
            }
          }, 15);

          for (let item of this.pointsList) {
            setTimeout(() => {
              this.SavePoint(item, resp.id);
            }, 20);
            this.$router.push("/profile/companies");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    async SavePoint(point, company_id) {
      const url = "/api/v1/points/create/";
      point.company_id = Number(company_id);

      await this.$axios
        .$post(url, point, {})
        .then((resp) => {})
        .catch((error) => {
          console.error(error);
        });
    },
    async AddLogoCompany(pk, logo_company) {
      let url = `/api/v1/companies/partial/${pk}/`;
      let bodyFormData = new FormData();
      bodyFormData.append("logo", logo_company);

      await this.$axios
        .$patch(url, bodyFormData, {})
        .then((resp) => {
          console.log("addlogo");
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    async AddPhotoCompany(pk, image) {
      let url = `/api/v1/companies/images/create/`;
      let bodyFormData = new FormData();

      bodyFormData.append("image", image);
      bodyFormData.append("company", pk);

      await this.$axios
        .$post(url, bodyFormData, {})
        .then((resp) => {
          console.log("addmany");
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    AddPoint() {
      this.count_id += 1;
      this.pointsList.push({
        id: this.count_id,
        metro_add: [5],
        company_id: null,
        active: true,
        name: "",
        phone: "+7",
        office: "",
        address: "",
        city_id: "",
        work_time: "",
        author: this.$store.state.auth.user.id,
      });
    },
    OnDataPoint(data) {
      this.$store.commit("points/SetPoints", data);
    },
    OnPkCategory() {
      this.ListInputCategory = [
        {
          id: 1,
        },
      ];
    },
    removeItem(item) {
      for (let i = 0; i < this.pointsList.length; i++) {
        if (this.pointsList[i].id === item.id) {
          this.pointsList.splice(i, 1);
        }
      }
    },
    removeItemCategory(item) {
      for (let i = 0; i < this.ListInputCategory.length; i++) {
        if (this.ListInputCategory[i].id === item.id) {
          this.ListInputCategory.splice(i, 1);
        }
      }
    },
    removeItemBrand(item) {
      for (let i = 0; i < this.ListInputBrands.length; i++) {
        if (this.ListInputBrands[i].id === item.id) {
          this.ListInputBrands.splice(i, 1);
        }
      }
    },
  },
};
</script>

<style scoped>
.textdanger {
  border: 1px solid red;
}
</style>
