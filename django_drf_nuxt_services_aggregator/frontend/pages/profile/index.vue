<template>
  <div class="user-profile">
    <div class="container">
      <Toast text="Данные профиля изменены" title="Изменение профиля" />

      <div class="row mb-4">
        <h1>Профиль пользователя</h1>
      </div>

      <div class="row mt-5">
        <div class="col-12 col-lg-6 col-md-6 mb-4">
          <h6>Фото профиля</h6>
          <ImageLogoImage
            :photo_label="user.avatar"
            :urlRemovePhoto="urlRemovePhoto"
            :urlAddPhoto="urlAddPhoto"
            :paramname="paramname"
            :Submit="Submit"
            :autoProcessQueue="autoProcessQueue"
          />
        </div>
        <div class="col-12"></div>
        <div
          class="col-12 col-lg-6 col-md-6 mt-4"
          style="
            background: white;
            border-radius: 9px;
            padding-bottom: 2em;
            padding-top: 2em;
          "
        >
          <div class="row" style="padding: 0.7em;">
            <div class="col-6">Ваш Email</div>
            <div class="col-6">{{ user.email }}</div>

            <div class="col-6">Ваше Имя</div>
            <div class="col-6">
              <span v-if="user.username">{{ username }}</span>
              <span v-else>Не предоставлено</span>
            </div>

            <div class="col-6">Ваша Фамилия</div>
            <div class="col-6">
              <span v-if="user.first_name">{{ first_name }}</span>
              <span v-else>Не предоставлено</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="container"
      style="
        background: white;
        border-radius: 9px;
        margin-top: 4em;
        padding-bottom: 2em;
        padding-top: 2em;
      "
    >
      <h4>Изменить данные</h4>
      <form v-on:submit.prevent="onSendDataUser">
        <!-- <div class="col-12 mt-3">
          <label for="">Загрузить аватар</label>
          <input
            class="form-control"
            @change="AddAvatar"
            required
            type="file"
            id="formFile"
          />
        </div> -->
        <div class="col-12 mt-3">
          <label for="">Имя пользователя</label>
          <input
            class="form-control"
            v-model="username"
            id="validationDefault01"
            placeholder="Введите имя"
            required
          />
        </div>
        <div class="col-12 mt-3">
          <label for="">Фамилия пользователя</label>
          <input
            v-model="first_name"
            class="form-control"
            id="validationDefault01"
            placeholder="Введите фамилию"
            required
          />
        </div>
        <div style="text-align: right" class="text-right col-12 mt-4">
          <button style="" class="btn btn-primary" type="submit">
            Сохранить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  middleware: "auth",
  layout: "profile",

  async asyncData({ $axios, req, store, route }) {
    return {
      user: store.state.auth.user,
      urlAddPhoto: `api/v1/users/add-avatar/${store.state.auth.user.id}/`,
      urlRemovePhoto: `api/v1/users/delete-avatar/${store.state.auth.user.id}/`,
    };
  },

  data() {
    return {
      user: null,
      title: `Профиль пользователя`,
      pushalert: false,
      Submit: false,
      autoProcessQueue: true,
      paramname: "avatar",
      first_name: "",
      username: "",
      avatar: null,
    };
  },
  head() {
    return {
      title: `Профиль пользователя`,
    };
  },
  mounted() {
    this.user = this.$store.state.auth.user;
    this.first_name = this.user.first_name;
    this.username = this.user.username;
  },

  methods: {
    AddAvatar(e) {
      console.log(e);
    },
    onSendDataUser() {
      let data = {
        password: "",
        username: this.username,
        first_name: this.first_name,
      };

      this.$axios
        .$put(`api/v1/users/${this.user.id}/`, data, {})
        .then((resp) => {
          console.log(resp);
          this.$auth.setUser(resp);
          this.pushalert = true;
        })
        .catch(function (error) {});
    },
  },
};
</script>

<style>
</style>
