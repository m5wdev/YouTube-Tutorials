<template>
  <div
    class="form-item-add"
  >
    <div
      class="d-flex flex-wrap justify-content-between align-items-center"
    >
      <h3>№{{ index + 1 }}</h3>
      <div v-if="index > 0" class="btn btn-warning mt-3" @click="removeI()">Удалить</div>
    </div>

    <div class="form-check mb-3">
      <input
        v-model="point.active"
        class="form-check-input"
        type="checkbox"
        id="item_active"
      />
      <label class="form-check-label" for="item_active">Активная </label>
    </div>
    <div class="mb-3">
      <label for="item_name" class="form-label">Название мастерской</label>
      <input
        required
        :class="{
          'text-danger': !point.name && Validate,
        }"
        v-model="point.name"
        type="text"
        class="form-control"
        id="item_name"
        placeholder=""
      />
      <span style="color: red" v-if="!point.name && Validate"
        >обязательное поле</span
      >
    </div>
    <div class="mb-3">
      <label for="item_phone" class="form-label">Телефон</label>
      <input
      v-mask="'+7 (###) ###-##-##'"
        required
        :class="{
          'text-danger': !point.phone && Validate,
        }"
        v-model="point.phone"
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
        :class="{
          'text-danger': !point.office && Validate,
        }"
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
        :class="{
          'text-danger': !point.address && Validate,
        }"
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

      <FormsSearchCity
        :point="point"
        :valid="valid"
        :AddCityPoint="AddCityPoint"
      />
      <span style="color: red" v-if="!point.city && Validate"
        >обязательное поле</span
      >
    </div>
    <div v-if="point.city_id" class="mb-3">
      <label for="item_address_with_city" class="form-label"
        >Станция метро</label
      >
      <FormsSearchMetro :point="point" :valid="valid" :AddMetro="AddMetro" />
      <span style="color: red" v-if="!point.city && Validate"
        >обязательное поле</span
      >
    </div>
    <div class="mb-3">
      <label for="item_work_time" class="form-label">Время работы</label>
      <textarea
        required
        :class="{
          'text-danger': !point.work_time && Validate,
        }"
        v-model="point.work_time"
        class="form-control"
        id="item_work_time"
        rows="3"
      ></textarea>
      <span style="color: red" v-if="!point.work_time && Validate"
        >обязательное поле</span
      >
    </div>
  </div>
</template>


<script>
export default {
  props: ["item", "removeItem", "pointsList", "index", "valid"],
  mounted() {
    this.point = this.item
  },
  watch: {
    "point.city"(val) {
      if (val) {
        this.GetCityMetroBool(val)
      }
    },
  },
  data() {
    return {
      point: {},
      city_metro: false,
    }
  },
  computed: {
    Validate() {
      if (!this.valid) {
        return true
      } else {
        return false
      }
    },
  },
  methods: {
    async GetCityMetroBool(name) {
      await this.$axios
        .get(`/api/v1/cities/metro/${name}/`)
        .then((resp) => {
          if (resp.data.metro) {
            this.city_metro = true
          } else {
            this.city_metro = false
          }
        })
        .catch(error => {
          console.error(error)
        })
    },
    AddCityPoint(city) {
      this.point.city_id = city
    },
    AddMetro(metro) {
      this.point.metro_id = metro
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
        this.removeItem(this.item)
      }
    },
  },
};
</script>


<style lang="scss" scoped>
.form-item-add {
  background: white;
  padding: 1em;
  border-radius: 12px;
  margin-top: 3em;
}

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
