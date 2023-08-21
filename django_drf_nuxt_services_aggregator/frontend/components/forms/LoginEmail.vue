<template>
  <!-- form email -->

  <form v-on:submit.prevent="onloginform">
    <div style="padding-top: 1em">
      <div class="col-12 mt-3">
        <label for="">Email</label>
        <input
          type="email"
          v-model="email"
          class="form-control"
          id="validationDefault01"
          placeholder="Email"
          required
        />
      </div>

      <div class="col-12 mt-3">
        <label for="">Пароль </label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="validationDefault02"
          placeholder="Пароль"
          required
        />
      </div>
      <div style="text-align: right" class="text-right col-12 mt-4">
        <button style="" class="btn btn-primary" type="submit">Вход</button>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  async asyncData({ route, redirect, $axios, store }) {
    if (store.getters.getUserInfo) {
    }
    return "";
  },
  props: ["alertPage"],
  data() {
    return {
      email: "",
      password: "",
      valid: true,
      show1: false,
      emailRules: [
        (v) =>
          !v ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          "Невалидный E-mail  ",
      ],
    };
  },
  methods: {
    onloginform() {

      this.login();

    },
    async login() {
      this.loading = true;
      try {
        let data = {
          email: this.email,
          password: this.password,
        };
        let response = await this.$auth.loginWith("local", {
          data: data,
        });
        this.$router.push("/profile");
      } catch (err) {
        this.alertPage();
      }
    },
  },
};
</script>
