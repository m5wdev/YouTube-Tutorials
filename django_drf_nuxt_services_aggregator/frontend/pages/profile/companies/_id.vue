<template>
  <div class="container">
    <div class="row mb-4">
      <h1>Редактировать компанию</h1>
    </div>

    <div class="row">
      <div class="col-12 text-center">
        <!-- Button trigger modal -->
        <button
          type="button"
          class="btn btn-outline-danger"
          data-bs-toggle="modal"
          data-bs-target="#exampleModal"
        >
          УДАЛИТЬ КОМПАНИЮ
        </button>

        <!-- Modal -->
        <div
          class="modal fade"
          id="exampleModal"
          tabindex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">
                  Удаление компании
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                Все данные компании,а также все связанные мастерские будут
                удалены
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Отмена
                </button>
                <button @click="OnDelete" data-bs-dismiss="modal" type="button" class="btn btn-primary">
                  Подтвердить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-7 mt-4">
        <form v-on:submit.prevent="UpdateCompany">
          <div id="form-company-add">
            <!-- <div class="h3 mb-4">Добавить компанию</div> -->
            <div class="row">
              <div class="col-12 col-lg-6 col-md-6">
                <div class="h5">Добавить логотип</div>
              </div>
              <div class="col-12 col-lg-6 col-md-6">
                <ImageLogoCompany
                  :autoProcessQueue="true"
                  :urlpath="`/api/v1/companies/add-logo/${$route.params.id}/`"
                  :logo_company="company.logo"
                  :AddLogo="AddLogo"
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
                class="form-control"
                id="company_body"
                rows="3"
                v-model="company.body"
              ></textarea>
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
            </div>
            <div class="mb-3">
              <label for="company_url" class="form-label">Сайт</label>
              <input
                required
                type="url"
                class="form-control"
                id="company_url"
                placeholder="company.ru"
                v-model="company.url"
              />
            </div>
            <div class="mb-3">
              <label for="company_phone" class="form-label">Телефон</label>
              <input
                required
                type="text"
                class="form-control"
                id="company_phone"
                v-mask="'+7 (###) ###-##-##'"
                v-model="company.phone"
              />
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
              </div>
              <div class="col">
                <label for="company_max_price" class="form-label"
                  >Максимальная цена</label
                >
                <input
                  required
                  min="1"
                  type="number"
                  class="form-control"
                  id="company_max_price"
                  placeholder="00000"
                  v-model="company.max_price"
                />
              </div>
            </div>

            <div class="row g-3 mb-3">
              <div class="col">
                <label for="company_number_of_employees" class="form-label"
                  >Количество работников</label
                >
                <input
                  required
                  min="0"
                  type="number"
                  class="form-control"
                  id="company_number_of_employees"
                  placeholder="15"
                  v-model="company.number_of_employees"
                />
              </div>
              <div class="col">
                <label for="company_year_of_foundation" class="form-label"
                  >Год основания</label
                >
                <input
                  required
                  type="number"
                  min="0"
                  class="form-control"
                  id="company_year_of_foundation"
                  placeholder="2008"
                  v-model="company.year_of_foundation"
                />
              </div>
            </div>
            <div class="mt-5" style="">
              <h5>Выбрать бренды</h5>

              <div v-for="(item, index) in company.brands" :key="index">
                <FormsEditSearchDataCompany
                  UrlPath="/api/v1/brands/search/?search="
                  :index="index"
                  :ListData="company.brands"
                  placeholder="Поиск Бренда"
                  :item="item"
                  :RemoveItemData="removeItemBrand"
                  :valid="valid"
                />
              </div>
              <div class="col-12 mt-4" style="text-align: start">
                <div
                  @click="
                    company.brands.push({
                      id: (countbrand_id += 1),
                      name: '',
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

              <div v-for="(item, index) in company.subcategories" :key="index">
                <FormsEditSearchDataCompany
                  UrlPath="/api/v1/categories/search/?search="
                  :index="index"
                  :ListData="company.subcategories"
                  :item="item"
                  placeholder="Поиск категории"
                  :RemoveItemData="removeItemCategory"
                  :valid="valid"
                />
              </div>
              <div class="col-12 mt-4" style="text-align: start">
                <div
                  @click="
                    company.subcategories.push({
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

            <ImageEditManyImageCompany
              :AddImages="AddImages"
              :images="company.images"
            />

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
              v-for="(item, index) in company.points"
              :key="item.id"
              class="col-12 mt-2"
            >
              <FormsEditPoint
                :index="index"
                :pointsList="company.points"
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
  async asyncData({ $axios, req, store, route }) {
    const resp_data = await $axios.get(
      `/api/v1/companies/profile/${route.params.id}/`
    );
    return {
      company: resp_data.data,
      urlRemovePhoto: `/api/companies/delete-logo/${resp_data.data.id}/`,
      urlAddPhoto: `/api/companies/add-logo/${resp_data.data.id}/`,
    };
  },
  async mounted() {
    if (this.company.points.length == 0) {
      ("add point");
      this.AddPoint();
    }
    // setTimeout(() => {
    //   if (this.company.points.length) {
    //     this.pointsList = this.company.points;
    //   }
    // }, 30);
    // setTimeout(() => {
    //        if (this.company.brands.length) {
    //   this.ListInputBrands = this.company.brands;
    // }
    // }, 10);
    // setTimeout(() => {
    //   if (this.company.subcategories.length) {
    //     this.ListInputCategory = this.company.subcategories;
    //   }
    // }, 10);
  },

  data() {
    return {
      photo_label: null,

      paramname: "logo",
      Submit: false,
      autoProcessQueue: true,
      formcompany: false,
      countbrand_id: 1,
      valid: true,
      removePoint: [],
      count_id: 1,
      pointsList: [
        {
          id: new Date().getTime(),
        },
      ],
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
    };
  },
  methods: {
    AddLogo(photo) {
      this.logo_company = photo;
    },
    OnDelete(){
        let url = `/api/v1/companies/delete/${this.$route.params.id}/`
        this.$axios.delete(url,{})
        .then((resp)=>{
            this.$router.push('/profile/companies')
        })

    },
    AddImages(images_company) {
      console.log("many images");
      this.images_company = images_company;
    },
    async UpdateCompany() {
      const url = `/api/v1/companies/update/${this.$route.params.id}/`;
      delete this.company["logo"];
      let company = this.company;
      let company_points = this.company.points;
      company["brands_list_id"] = this.company.brands;
      company["categories_list_id"] = company.subcategories;
      this.formcompany = true;
      await this.$axios
        .$put(url, company, {})
        .then((resp) => {
          console.log(resp);
          console.log(resp.id);
          setTimeout(() => {
            this.Submit = true;
          }, 150);

          for (let item of company_points) {
            if (String(item.id).substr(0, 2) != "id") {
              item.city_id = item.city;
              item.company_id = resp.id;
              item.metro_id = item.metro;
              item.author = this.$store.state.auth.user.id;
              console.log(item.id);
              this.UpdatePoint(item);
            } else {
              item.city_id = item.city;
              item.metro_id = item.metro;
              item.author = this.$store.state.auth.user.id;
              this.SavePoint(item, resp.id);
            }
          }

          this.$router.push("/profile/companies");
          setTimeout(() => {
            window.scrollTo({
              top: 0,
              behavior: "smooth",
            });
          }, 50);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    async UpdatePoint(point) {
      if (typeof point.metro_id === "number") {
      } else {
        point.metro_id = 0;
      }
      const url = `/api/v1/points/update/${point.id}/`;
      await this.$axios
        .$put(url, point, {})
        .then((resp) => {
          console.log("update point", resp);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    async SavePoint(point, company_id) {
      console.log("create");
      const url = "/api/v1/points/create/";
      point.company_id = company_id;
      console.log(point);
      await this.$axios
        .$post(url, point, {})
        .then((resp) => {
          console.log(resp);
          //   this.$router.push("/profile/companies");
        })
        .catch((error) => {
          console.error(error);
        });
    },

    AddPoint() {
      this.count_id += 1;
      this.company.points.push({ id: "id" + new Date().getTime() });
    },
    OnDataPoint(data) {
      this.$store.commit("points/SetPoints", data);
    },

    removeItem(item) {
      for (var i = 0; i < this.company.points.length; i++) {
        if (this.company.points[i].id === item.id) {
          this.company.points.splice(i, 1);
        }
        if (this.company.points.length == 0) {
          this.AddPoint();
        }
      }
    },
    removeItemCategory(item) {
      for (var i = 0; i < this.company.subcategories.length; i++) {
        if (this.company.subcategories[i].id === item.id) {
          this.company.subcategories.splice(i, 1);
        }
      }
    },
    removeItemBrand(item) {
      for (var i = 0; i < this.company.brands.length; i++) {
        if (this.company.brands[i].id === item.id) {
          this.company.brands.splice(i, 1);
        }
      }
    },
  },
};
</script>
