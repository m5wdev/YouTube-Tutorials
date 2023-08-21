<template>
  <div
    style="
      background: white;
      padding: 1em;
      border-radius: 12px;
      margin-top: 3em;
    "
    id="form-item-add "
  >
    <div
      class="d-flex flex-wrap"
      style="justify-content: space-between; align-items: center"
    >
      <h3>№{{ index + 1 }}</h3>
      <div class="btn btn-warning mt-3" @click="removeI()">Удалить</div>
    </div>

    <div class="form-check mb-3">
      <input
        v-model="point.active"
        class="form-check-input"
        type="checkbox"
        id="item_active"
      />
      <label class="form-check-label" for="item_active"> Активная </label>
    </div>
    <div class="mb-3">
      <label for="item_name" class="form-label">Название мастерской</label>
      <input
        required
        v-model="point.name"
        type="text"
        class="form-control"
        id="item_name"
        placeholder=""
      />
    </div>
    <div class="mb-3">
      <label for="item_phone" class="form-label">Телефон</label>
      <input
        required
        v-model="point.phone"
        v-mask="'+7 (###) ###-##-##'"
        type="text"
        class="form-control"
        id="item_phone"
        placeholder="+7 000 000-00-00"
      />
      <span style="color: red" v-if="!point.phone && Validate"
        >обязательное поле</span
      >
    </div>
    <div class="mb-3">
      <label for="item_office" class="form-label">Офис</label>
      <input
        required
        v-model="point.office"
        type="text"
        class="form-control"
        id="item_office"
        placeholder=""
      />
      <span style="color: red" v-if="!point.office && Validate"
        >обязательное поле</span
      >
    </div>
    <div class="mb-3">
      <label for="item_address" class="form-label">Адрес</label>
      <input
        required
        v-model="point.address"
        type="text"
        class="form-control"
        id="item_address"
        placeholder=""
      />
      <span style="color: red" v-if="!point.address && Validate"
        >обязательное поле</span
      >
    </div>
    <div class="mb-3">
      <label for="item_address_with_city" class="form-label">Город</label>

      <FormsEditSearchDataCity
        UrlPath="/api/v1/cities/search/?search="
        :item="point.city"
        :city_id="city_id"
        :Addcityid="Addcityid"
      />
    </div>

    <div v-if="city_metro" class="mb-3">
      <label for="item_address_with_city" class="form-label"
        >Станция метро</label
      >

      <FormsEditSearchCityMetro
        :UrlPath="`/api/v1/metro-station/search/?city=${this.city_id}&search=`"
        :item="point"
        :valid="valid"
        :AddMetroId="AddMetroId"
      />
    </div>
    <div class="mb-3">
      <label for="item_work_time" class="form-label">Время работы</label>
      <textarea
        required
        v-model="point.work_time"
        class="form-control"
        id="item_work_time"
        rows="3"
      ></textarea>
    </div>
  </div>
</template>


<script>
export default {
  props: ["item", "removeItem", "pointsList", "index", "valid"],
  mounted() {
    this.point = this.item;
    this.point.metro_id = this.point.metro || 0
  },
  watch: {
    "point.city"(val) {
      if (val) {
        this.GetCityMetroBool(val);
      }
    },
  },
  data() {
    return {
      point: {},
      city_metro: false,
      city_id: null,
      metro_id: null,
    };
  },
  computed: {
    Validate() {
      if (!this.valid) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    Addcityid(pk) {
      this.city_id = pk;
      this.point.city = pk;
      this.GetCityMetroBool(pk);
    },
    AddMetroId(pk) {
      console.log(pk);
      this.metro_id = pk;
      this.point.metro = pk;
      this.point.metro_id = pk
    },
    async GetCityMetroBool(pk) {
      await this.$axios
        .get(`/api/v1/cities/metro/${pk}/`)
        .then((resp) => {
          if (resp.data.metro) {
            this.city_metro = true;
          } else {
            this.city_metro = false;
          }
        })
        .catch((error) => {
          console.log("error");
        });
    },
    AddCityPoint(city) {
      this.point.city_id = city;
    },
    AddMetro(metro) {
      this.point.metro_id = metro;
    },
    async DeletePoint() {
      const url = `/api/v1/points/delete/${this.item.id}/`;
      await this.$axios
        .$delete(url, {})
        .then((resp) => {

        })
        .catch((error) => {
          console.error(error);
        });
    },
    removeI() {
      if (this.pointsList.length === 1) {
        this.point = {
          id: 1,
          metro_add: [5],
          company_id: null,
          active: false,
          name: "",
          phone: "",
          office: "",
          address: "",
          city: "",
          work_time: "",
          author: this.$store.state.auth.user.id,
        };
      } else {
        this.removeItem(this.item);
      }

      if (String(this.item.id).substr(0, 2) != "id") {
        this.DeletePoint();
      }
    },
  },
};
</script>


<style scoped>
.form-point {
  background: white;
  padding: 1em;
  border-radius: 12px;
  margin-top: 3em;
}

.text-danger {
  border: 1px solid red;
}
</style>
