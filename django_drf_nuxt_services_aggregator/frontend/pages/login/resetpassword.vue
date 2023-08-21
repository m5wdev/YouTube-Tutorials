<template>
  <div class="container registration-page-content">
    <div class="row justify-content-center">
      <div v-if="loading" class="loading-page"></div>

      <div v-if="snackbar" class="alert alert-secondary" role="alert">
        {{ text }}
      </div>
      <div class="col-12 col-lg-6 col-md-6">
        <div class="col-12 col-lg-6 col-md-6" id="sign-in-button"></div>
        <div>
          <div class="col-12 col-lg-6 col-md-6 m-0-auto">
            <div id="sign-in-button"></div>
            <h1>{{ texttitle }}</h1>
            <p style="color: #474d57">{{ textbody }} .</p>
            <!-- form email -->

            <!-- if email type -->
            <form v-if="step == 0" v-on:submit.prevent="EmailPasswordData">
              <div style="padding-top: 1em">
                <div cols="12">
                  <p style="color: #474d57">Укажите ваш Email.</p>
                </div>
                <div cols="12">
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
                <div style="text-align: right" class="text-right col-12 mt-4">
                  <button style="" class="btn btn-primary" type="submit">
                    Далее
                  </button>
                </div>
              </div>
            </form>
            <!-- if phone type -->

            <!-- form confirm email -->

            <form v-on:submit.prevent="EmailVerify" v-if="step == 2">
              <div cols="12" lg="8">
                <label for="">Введите код</label>

                <input
                  type="number"
                  v-model="codeEmail"
                  class="form-control"
                  id="validationDefault04"
                  placeholder="Проверочный код"
                  required
                />
                <span v-if="timer > 0" style="font-size: 0.7em; color: #474d57"
                  >Запросить новый код можно через {{ timer }} сек.</span
                >
              </div>
              <div class="" cols="12" lg="4">
                <div style="" class="text-right col-12 col-lg-4">
                  <button
                    @click="OnCodeEmail"
                    :disabled="timer > 0"
                    style=""
                    class="btn btn-primary"
                    type="submit"
                  >
                    <span v-if="timer > 0">код отправлен</span>
                    <span v-else>получить код</span>
                  </button>
                </div>

                <div style="text-align: right" class="text-right col-12 mt-4">
                  <button style="" class="btn btn-primary" type="submit">
                    Далее
                  </button>
                </div>
              </div>
            </form>
            <!-- password -->
            <form v-on:submit.prevent="editpassword" v-if="step == 3">
              <div style="padding-top: 1em">
                <div cols="12">
                  <p style="color: #474d57">
                    Придумайте новый надежный пароль.
                  </p>
                </div>

                <div cols="12">
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
                  <button style="" class="btn btn-primary" type="submit">
                    Вход
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// import intlTelInput from 'intl-tel-input';
export default {
  auth: "guest",
  head: {
    title: "Востановление пароля",
  },
  async asyncData({ route, $axios, store }) {
    return "";
  },
  data() {
    return {
      mask: "",
      textbody: "Ввод Email",
      texttitle: "Введите Email профиля для востановления",
      confirm: false,
      codetext: "код отправлен",
      valid: true,
      valid2: true,
      contry: { id: "1", contry: "Кыргызстан" },
      valid3: true,
      valid4: true,
      step: 0,
      location: null,
      step0: true,
      step1: false,
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
      value: true,
      rules: {
        required: (value) => !!value || "Required.",
        password: (value) => {
          const pattern =
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/;
          return (
            pattern.test(value) ||
            "Мин. 8 символов, включая хотя бы одну заглавную букву, цифру и специальный символ."
          );
        },
      },
      email: "",
      text: "",
      btn: "1",
      phone_prod: "",
      color: "",
      typeLogin: "0",
      confirmEmail: false,
      timeout: 3000,
      telinp: null,
      codeEmail: "",
      code: null,
      codeEmailApi: null,
      succes: false,
      err: false,
    };
  },
  computed: {},
  methods: {
    async AddType() {
      if (this.btn === "1") {
      } else {
        setTimeout(() => {
          const phoneInputField = document.querySelector("#phone");
          this.telinp = window.intlTelInput(phoneInputField, {
            initialCountry: this.location || "us",
            formatOnDisplay: true,
            preferenceCountries: ["kg", "kz", "uz", "ru"],
            separateDialCode: true,
            utilsScript:
              "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.16/js/utils.js",
          });
          this.PhoneRules = this.PhoneRules2;
        }, 150);
      }
      this.textbody =
        "Введите данные своего аккаунта и надежный пароль для его защиты";
      this.texttitle = "Введите данные профиля";
      this.step1 = true;
      this.step = 1;
    },
    editpassword() {
      let url = `/api/v1/users/reset-password/?typelogin=${this.btn}`;
      let data = {
        email: this.email,
        phone: this.phone_prod,
        password: this.password,
      };
      this.$axios
        .$post(url, data)
        .then((resp) => {
          this.color = "green";
          this.text = resp.message;
          this.snackbar = true;
          setTimeout(() => {
            this.$router.push("/login");
          }, 3000);
        })
        .catch((error) => {
          this.color = "red";
          try {
            this.text = error.response.data.message;
          } catch (error) {
            this.text = "ошибка сервера";
          }
          this.snackbar = true;
        });
    },
    SendEmail() {
      let url = `/api/v1/users/send-code/?email=${this.email}&status=2`;
      this.$axios
        .$get(url, {})
        .then((resp) => {
          this.textbody = `Пожалуйста, введите 6-значный код подтверждения, который был отправлен на ${this.email}. Код действителен в течение 3 минут`;
          this.texttitle = "Верификация по эл. почте";
          this.color = "green";
          this.text = "На вашу почту отправлен код подтверждения!";
          this.snackbar = true;
          this.step = 2;
          this.step2 = true;
          this.codeEmailApi = resp.token_email;
          this.TimerCodeEmail();
        })
        .catch((error) => {
          this.color = "red";
          try {
            this.text = error.response.data.message;
          } catch (error) {
            this.text = "ошибка сервера";
          }
          this.snackbar = true;
        });
    },
    EmailPasswordData() {
      this.SendEmail();
    },
    TimerCodeEmail() {
      this.timer = 60;
      if (this.timer > 1) {
        let nIntervId = setInterval(() => {
          this.timer -= 1;
          if (this.timer === 0) {
            clearInterval(nIntervId);
            nIntervId = null;
          }
        }, 1000);
      }
    },
    OnCodeEmail() {
      this.SendEmail();
    },
    async OnCodePhone() {
      await this.SendPhone();
    },
    async EmailVerify() {
      if (this.codeEmail === this.codeEmailApi) {
        this.textbody = `Придумайте надежный пароль`;
        this.texttitle = "Введите пароль";
        this.color = "green";
        this.text = "Email верефицирован успешно";
        this.snackbar = true;
        this.step = 3;
        this.timer = 0;
        this.step3 = true;
      } else {
        this.color = "red";
        this.text = "Неверный код";
        this.snackbar = true;
      }
    },
    ConfirmCodeEmail() {
      if (this.codeEmail === this.codeEmailApi) {
        this.text = "Email  подтвержден";
        this.succes = true;
        setTimeout(() => {
          this.succes = false;
        }, 3000);
      } else {
        this.text = "Неверный код";
        this.err = true;
        setTimeout(() => {
          this.err = false;
        }, 3000);
      }
    },
    codeSigninEmail() {},
    async createUser() {
      try {
        await this.$fire.auth.createUserWithEmailAndPassword(
          "glebhleb89@icloud.com",
          "test123"
        );
      } catch (e) {
        console.log(e);
      }
    },
    async SendPhone() {
      this.loading = true;
      let self = this;
      let appVerifier = window.recaptchaVerifier;
      if (!self.phone_prod) {
        let phone = this.telinp.getNumber();
        console.log(self.phone_prod, this.telinp);
        self.phone_prod = phone;
      }
      console.log(2, self.phone_prod, this.telinp);
      await this.$fire.auth
        .signInWithPhoneNumber(`${self.phone_prod}`, appVerifier)
        .then((confirmationResult) => {
          window.confirmationResult = confirmationResult;
          self.telinp.destroy();
          self.loading = false;
          self.textbody = `Пожалуйста, введите 6-значный код подтверждения, отправленный на +${this.phone}. Код действителен в течение 3 минут`;
          self.texttitle = "Подтверждение с помощью телефона";
          self.codetext = "код отправлен";
          self.color = "green";
          self.text = "На ваш телефон отправлен код подтверждения!";
          self.snackbar = true;
          self.TimerCodeEmail();
          self.step = 2;
          self.step2 = true;
        })
        .catch((error) => {
          let message;
          try {
            if (
              error.message ===
              "Firebase: Exceeded quota. (auth/quota-exceeded)."
            ) {
              message = "Превышен лимит запросов кода! Попробуйте через 1 час!";
            } else {
              message = "Неверный номер!";
            }
          } catch (error) {
            message = "Неверный номер!";
          }
          this.loading = false;
          this.color = "red";
          this.text = message;
          this.snackbar = true;
        });
    },
    async PhoneAdd() {
      if (this.$refs.phone.validate()) {
        await this.SendPhone();
      }
    },
    async PhonelVerify() {
      if (this.$refs.confirmphone.validate()) {
        this.loading = true;
        var self = this;
        confirmationResult
          .confirm(self.code_phone)
          .then((result) => {
            this.textbody = `Придумайте надежный пароль`;
            this.texttitle = "Введите пароль";
            this.color = "green";
            this.text = "Номер телефона верефицирован успешно";
            this.snackbar = true;
            this.step = 3;
            this.timer = 0;
            this.step3 = true;
            this.loading = false;
          })
          .catch((error) => {
            this.loading = false;
            self.color = "red";
            self.text = "Неверный код потдверждения!";
            self.snackbar = true;
          });
      }
    },
  },
};
</script>

<style scoped>
.vl {
  border-left: 3px solid rgb(239 241 245);
  height: 30px;
  margin-left: 1em;
}
.activestep {
  border-left: 3px solid #3b76ea;
}
.activebtn {
  background-color: #f5f5f5;
  color: #1e2329;
  border-radius: 2px;
  font-size: 16px;
  font-weight: bold;
}
.mdi-account::before {
  content: "\F0004";
  color: white;
}
.btn-conf {
  margin-top: 1.6em;
}
@media (max-width: 1250px) {
  .btn-conf2 {
    position: absolute;
    top: -3em;
  }
}
@media (max-width: 600px) {
  .text-btn {
    font-size: 0.5em;
  }
  .btn-conf2 {
    /* position: absolute;
    top: -1em; */
  }
}
.o2t-element1 {
  opacity: 0;
  visibility: hidden;
  transition: 0.55s opacity, 0.55s visibility;
}
.o2t-element-email {
  opacity: 0;
  visibility: hidden;
  transition: 0.55s opacity, 0.55s visibility;
}
.o2t-element {
  opacity: 1;
  visibility: visible;
}
.box-step {
  justify-content: center;
  display: flex;
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
.m-0-auto{
  margin: 0 auto;
}
</style>
