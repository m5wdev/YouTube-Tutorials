<template>
  <div class="container login-page-content">
    <div v-if="snackbar" class="alert alert-secondary" role="alert">
      {{ text }}
    </div>
    <div class="row justify-content-center">
      <!-- <h3 v-if="telinp">dd{{telinp}}</h3> -->
      <div class="card-login col-12 col-lg-5 col-md-8">
        <h2>Вход в систему</h2>
        <div class="mt-4 row justify-content-center">
          <div class="col-12">
            <div id="sign-in-button"></div>
            <FormsLoginEmail v-if="btn === '1'" :alertPage="alertPage" />
          </div>
        </div>
        <div style="width: 100%" class="text-right mt-8 pr-4">
          <Nuxt-Link style="text-decoration: none" to="/login/resetpassword"
            >Забыли пароль?</Nuxt-Link
          >
        </div>
        <div style="width: 100%" class="text-right mt-2 pr-4">
          <Nuxt-Link style="text-decoration: none" to="/registration"
            >Регистрация</Nuxt-Link
          >
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  head: {
    title: "Авторизация",
  },
  async asyncData({ route, $axios, store }) {
    return "";
  },
  computed: {},
  data() {
    return {
      mask: "",
      textbody: "Введите данные своего аккаунта и надежный пароль для его защиты",
      texttitle: "Введите данные профиля",
      confirm: false,
      codetext: "код отправлен",
      valid: true,
      tel2: null,
      btn: "1",
      valid2: true,
      valid3: true,
      valid4: true,
      step: 1,
      location: null,
      step1: true,
      step2: false,
      loading: false,
      step3: false,
      step4: false,
      phone: null,
      arrstep: [],
      code_phone: "",
      password: "",
      valid: true,
      timer: null,
      show1: false,
      snackbar: false,
      PhoneRules: [(v) => !!v || "Не может быть пустым"],
      PhoneRules2: [
        (v) => !!v || "Не может быть пустым",
        (v) =>
          this.telinp.isValidNumber() || "Номер не валидный для вашей страны",
      ],
      emailRules: [
        (v) => !!v || "E-mail обязательное поле",
        (v) => /.+@.+/.test(v) || "E-mail не валидный",
      ],
      email: "",
      text: "",
      phone_prod: "",
      color: "",
      confirmEmail: false,
      timeout: 3000,
      telinp: null,
      codeEmail: "",
      code: null,
      codeEmailApi: null,
      succes: false,
      err: false,
    }
  },
  watch: {},
  methods: {
    alertPage() {
      this.color = "red"
      this.text = "Неверный логин или пароль"
      this.snackbar = true

      setTimeout(() => {
        console.log("false")
        this.snackbar = false
      }, 2000)

      this.loading = false
    },
  },
}
</script>

<style>
.activebtn {
  background-color: #f5f5f5;
  color: #1e2329;
  border-radius: 2px;
  font-size: 16px;
  font-weight: bold;
}
.theme--dark.v-btn.v-btn--disabled {
  color: #ccc !important;
}
.loading-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  text-align: center;
  padding-top: 200px;
  font-size: 30px;
  font-family: sans-serif;
  z-index: 1;
}
.card-login {
  min-height: 30vh;
}
body main>.my-3 {
    margin-top: 0 !important;
}
.login-page-content{
  margin-top: 60px;
}
.login-page-content .card-login{
  background: #fff;
  padding: 30px 20px;
  border-radius: 8px;
  box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 10%);
}
@media (max-width: 768px) {
  .login-page-content{
    margin-top: 0px;
  }
  .login-page-content .card-login{
    border-radius: 0px;
  }
}
@media (max-width: 600px) {
  .card-login {
    min-height: 70vh;
  }
}
</style>
