<template>
  <div class="container registration-page-content">
    <div class="row justify-content-center">
      <div v-if="loading" class="loading-page"></div>

      <div v-if="snackbar" class="alert alert-secondary" role="alert">
        {{ text }}
      </div>
      <div class="col-12 col-lg-5 col-md-8 registration-card">
        <div>
          <div class="col-12 col-lg-12 col-md-12">
            <div id="sign-in-button"></div>
            <h1>{{ texttitle }}</h1>
            <p style="color: #474d57">{{ textbody }} .</p>
            <!-- form email -->
            <form v-if="step == 1" v-on:submit.prevent="EmailPasswordData">
              <div class="row mt-3">
                <div class="col-12">
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
                  <button style="" class="btn btn-primary" type="submit">
                    Далее
                  </button>
                </div>
              </div>
            </form>

            <!-- form confirm email -->

            <form v-on:submit.prevent="EmailVerify" v-if="step == 2">
              <div style="padding-top: 1em">
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
                  <span
                    v-if="timer > 0"
                    style="font-size: 0.7em; color: #474d57"
                    >Запросить новый код можно через {{ timer }} сек.</span
                  >
                </div>
                <div class="" cols="12" lg="4">
                  <v-btn
                    @click="OnCodeEmail"
                    :disabled="timer > 0"
                    dark
                    outlined
                    class="text-capitalize rounded-lg mt-6"
                    color="#3B76EA"
                    ><span v-if="timer > 0">код отправлен</span>
                    <span v-else>получить код</span>
                  </v-btn>
                </div>
                <div style="text-align: right" class="text-right col-12 mt-4">
                  <button style="" class="btn btn-primary" type="submit">
                    Регистрация
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
export default {
  auth: "guest",
  head: {
    title: "Регистрация",
  },
  async asyncData({ route, $axios, store }) {
    return "";
  },
  data() {
    return {
      mask: "",
      textbody:
        "Введите данные своего аккаунта и надежный пароль для его защиты",
      texttitle: "Введите данные профиля",
      confirm: false,
      codetext: "код отправлен",
      valid: true,
      valid2: true,
      contry: { id: "1", contry: "Кыргызстан" },
      valid3: true,
      valid4: true,
      valid5: true,
      step: 1,
      location: null,
      step1: true,
      step2: false,
      step5: false,
      loading: false,
      step3: false,
      step4: false,
      phone: null,
      arrstep: [],
      code_phone: "",
      password: "",
      last_name: "",
      first_name: "",
      valid: true,
      timer: null,
      show1: false,
      snackbar: false,
      value: true,
      PhoneRules: [(v) => !!v || "Не может быть пустым"],
      PhoneRules2: [
        (v) => !!v || "Не может быть пустым",
        // (v) =>
        //   this.telinp.isValidNumber() || "Номер не валидный для вашей страны",
      ],
      emailRules: [
        (v) => !!v || "E-mail обязательное поле",
        (v) => /.+@.+/.test(v) || "E-mail не валидный",
      ],
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
    };
  },
  computed: {
    CodeContry() {
      if (this.telinp) {
        let loc = this.telinp.getSelectedCountryData().iso2;
        for (let i in this.maskData) {
          if (i.toLowerCase() === loc) {
            this.mask = this.maskData[i];
            this.phone = "";
          }
        }
      }
    },
  },
  methods: {
    SendEmail() {
      let url = `api/v1/users/send-code/?email=${this.email}&status=1`;
      this.$axios
        .$get(url, {})
        .then((resp) => {
          this.textbody = `Пожалуйста, введите 6-значный код подтверждения, который был отправлен на ${this.email}. Код действителен в течение 3 минут`;
          this.texttitle = "Верификация по эл. почте";
          this.color = "green";
          this.text = "На вашу почту отправлен код подтверждения!";
          this.snackbar = true;
          this.TimerCodeEmail();
          this.codetext = "код отправлен";
          this.step = 2;
          this.step2 = true;
          this.codeEmailApi = resp.token_email;
          setTimeout(() => {
            this.snackbar = false;
          }, 2000);
        })
        .catch((error) => {
          this.color = "red";
          setTimeout(() => {
            this.snackbar = false;
          }, 2000);
          try {
            console.log(error);
            this.text = error.response.data.message;
            setTimeout(() => {
              this.snackbar = false;
            }, 2000);
          } catch (error) {
            this.text = "ошибка сервера";
          }
          this.snackbar = true;
          setTimeout(() => {
            this.snackbar = false;
          }, 2000);
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
        this.color = "green";
        this.text = "";
        this.snackbar = true;
        this.Registration();
      } else {
        this.color = "red";
        this.text = "неверный код";
        this.snackbar = true;
        setTimeout(() => {
          this.snackbar = false;
        }, 2000);
      }
    },
    async Registration() {
      let data = {
        password: this.password,
        email: this.email,
      };
      let url = "/api/v1/users/create/";
      await this.$axios
        .$post(url, data)
        .then((resp) => {
          this.loading = false;
          this.color = "green";
          this.text = "Успешная регистрация!";
          this.snackbar = true;
          this.$router.push("/login");
        })
        .catch((error) => {
          this.loading = false;
          this.text = "Пользователь с таким  email телеграмм уже существует";
          this.color = "red";
          this.snackbar = true;
          setTimeout(() => {
            this.snackbar = false;
          }, 2000);
        });
    },
    EmailSign() {
      if (this.$refs.email.validate()) {
        this.confirmEmail = true;
        this.color = "green";
        this.text = "На вашу почту отправлен код подтверждения!";
        this.snackbar = true;
        setTimeout(() => {
          document
            .querySelector(".o2t-element-email")
            .classList.add("o2t-element");
        }, 100);
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
    async phoneSign() {
      if (this.$refs.phone.validate()) {
        this.confirm = true;
        this.color = "green";
        this.text = "Смс с кодом отправлено на ваш номер телефона!";
        this.snackbar = true;
        setTimeout(() => {
          document.querySelector(".o2t-element1").classList.add("o2t-element");
        }, 100);
      }
    },
    codeSignin() {
      var self = this;
    },
  },
};
</script>
<style>
.vl {
  border-left: 3px solid rgb(239 241 245);
  height: 30px;
  margin-left: 1em;
}
.activestep {
  border-left: 3px solid #3b76ea;
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
.theme--light.v-input input,
.theme--light.v-input textarea {
  color: rgba(0, 0, 0, 0.87);
  padding-left: 0px;
}
body main>.my-3 {
    margin-top: 0 !important;
}
.registration-page-content{
  margin-top: 60px;
}
.registration-page-content .registration-card{
  background: #fff;
  padding: 30px 20px;
  border-radius: 8px;
  box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 10%);
}
.registration-page-content h1{
  color: #333;
  text-shadow: none;
}
@media (max-width: 768px) {
  .registration-page-content{
    margin-top: 0px;
  }
  .registration-page-content .registration-card{
    border-radius: 0px;
  }
}
</style>
