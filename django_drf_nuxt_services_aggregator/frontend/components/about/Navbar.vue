<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand class="navbar-brand" @click="OnPage('/')">
        <img
          class="mt-3"
          width="23px"
          height="auto"
          src="images/sc-logo.png"
          alt=""/>
        <span class="text-logo ml-3">Сервисные центры России</span>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown text="Города" right>
            <b-dropdown-item
              @click="OnPageDom('http://' + city.subdomain.name + process.env.FRONTURL || 'localhost:3000')"
              v-for="city in cities"
              :key="city.id">
              <a :href="'http://' + city.sub + process.env.FRONTURL || 'localhost:3000'">{{ city.name }}</a>
            </b-dropdown-item>
            </b-nav-item-dropdown>

          <b-nav-item @click="OnPage('/company')">Компании

          </b-nav-item>
          <b-nav-item @click="OnPage('/brands')">Бренды</b-nav-item>
          <b-nav-item @click="OnPage('/categories')">Категории</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <Nuxt-link class="link" to="/login">Вход</Nuxt-link>
          <Nuxt-link class="link ml-3" to="/registration">Регистрация</Nuxt-link>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  data() {
    return {}
  },
  computed: {
    cities() {
      return this.$store.getters["cities/cities"]
    },
  },
  methods: {
    OnPage(url) {
      this.$router.push(url)
    },
    OnPageDom(url) {
      window.location.href = url + this.$route.path
    },
  },
}
</script>


<style lang="scss" scoped>
.navbar-brand {
  cursor: pointer;
  display: flex;
  color: white;
  text-transform: uppercase;
  align-items: center;
  background-color: #02789b;
  /* background-image: url("/images/tmp_logo_bg_2.jpeg"); */
  background-repeat: no-repeat;
  background-size: cover;
  border-color: #11bcef;
  transform: skewX(-10deg);
  border-bottom: 2px solid #000;
  border-top: 4px solid rgba(255, 255, 255, 0.5);
  border-right: 2px solid #000;
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  padding: 0.255rem 1rem 0.255rem 1rem;
  margin-left: 5px;
  /* margin-top: -17px; */
  border-radius: 5px;
  background-blend-mode: darken;
  background-position: center;
}
.text-logo {
  color: white;
}
.link {
  color: white;
}
</style>
