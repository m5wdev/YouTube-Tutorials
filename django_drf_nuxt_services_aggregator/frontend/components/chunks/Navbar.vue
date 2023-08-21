<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-color fixed-top">
    <div class="container-fluid">
      <div @click="OnPage('/')">
        <Nuxt-link class="navbar-brand" to="/">
          <img
            src="~assets/images/logo.png"
            alt="Сервисные центры России"
            width="255"
            height="84"
            data-not-lazy
          />
        </Nuxt-link>
      </div>
      <button
        class="navbar-toggler collapsed"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ getActiveCity.cityName }}
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li v-for="city in cities" :key="city.id">
                <a class="dropdown-item" :href="formatUrl(city)">
                  <strong v-if="city.city_top">{{ city.name }}</strong>
                  <span v-else>{{ city.name }}</span>
                </a>
              </li>
            </ul>
          </li>
          <li class="nav-item" @click="OnPage('/companies')">
            <Nuxt-link
              class="nav-link"
              active-class="active"
              exact-active-class=""
              :to="{ name: 'companies' }"
              >Компании</Nuxt-link
            >
          </li>
          <li class="nav-item" @click="OnPage('/brands')">
            <Nuxt-link
              class="nav-link"
              active-class="active"
              exact-active-class=""
              to="#"
              >Бренды</Nuxt-link
            >
          </li>
          <li class="nav-item" @click="OnPage('/categories')">
            <Nuxt-link
              class="nav-link"
              active-class="active"
              exact-active-class=""
              to="/categories"
              >Категории</Nuxt-link
            >
          </li>
        </ul>
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item make-order">
            <button
              type="button"
              class="btn btn-success order-button"
              data-bs-toggle="modal"
              data-bs-target="#applicationModal"
            >
              <span class="order-icon"></span
              ><span class="order-text">Заявка на ремонт</span>
            </button>
          </li>
          <li
            class="nav-item"
            v-if="$store.state.auth.user"
            @click="OnPage('/profile')"
          >
            <Nuxt-link class="nav-link" active-class="active" to="/profile"
              >Профиль</Nuxt-link
            >
          </li>
          <li v-else class="nav-item" @click="OnPage('/login')">
            <Nuxt-link class="nav-link" active-class="active" to="/login"
              >Вход</Nuxt-link
            >
          </li>
          <li class="nav-item" v-if="$store.state.auth.user">
            <span
              style="cursor: pointer"
              @click="Exit"
              class="nav-link"
              active-class="active"
              >Выйти</span
            >
          </li>
          <li v-else class="nav-item" @click="OnPage('/registration')">
            <Nuxt-link class="nav-link" active-class="active" to="/registration"
              >Регистрация</Nuxt-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      user: this.$store.state.auth.user,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.onScroll);
    let toogler = document.querySelector('.navbar-toggler')
    console.log('toogler',toogler);
    toogler.classList.add('collapsed')
  },
  computed: {
    cities() {
      return this.$store.getters["cities/cities"];
    },
    getActiveCity() {
      const activeCity = this.$store.getters["cities/activeCity"];
      if (activeCity) {
        return { cityName: activeCity.name };
      } else {
        return "Город";
      }
    },
  },
  methods: {
    OnPage(url) {
      this.$router.push(url);
      let element = document.getElementsByClassName("navbar-toggler")[0];
      if (element.getAttribute("aria-expanded") == "true") {
        element.click();
      }
    },
    OnClose() {
      console.log(44);
    },
    onScroll() {
      if (window.top.scrollY > 20) {
        document.querySelector(".navbar").classList.add("nav-scroll");
      }
      if (window.top.scrollY < 20) {
        document.querySelector(".navbar").classList.remove("nav-scroll");
      }
    },
    async Exit() {
      await this.$auth.logout();
    },
    formatUrl(city) {
      const host = process.env.FRONTURL || "localhost:3000";
      // const host = "servis-centers.ru:8000";
      // const host = "localhost:3000";
      return `http://${city.subdomain.name}.${host}`;
    },
  },
};
</script>


<style lang="scss">
.dropdown-menu.show {
  display: grid;

  @media (max-width: 534.99px) {
    grid-template-columns: repeat(2, 1fr);
    height: 70vh;
    overflow: auto;
  }
  @media (min-width: 535px) and (max-width: 991.98px) {
    grid-template-columns: repeat(3, 1fr);
  }
  // @media (max-width: 991.98px) {
  //   grid-template-columns: repeat(3, 1fr);
  // }
  @media (min-width: 992px) {
    grid-template-columns: repeat(4, 1fr);
  }
}

.text-logo {
  color: white;
}

.link {
  color: white;
}

.nav-scroll {
  background: linear-gradient(
    45deg,
    rgb(28 50 108),
    rgb(83, 111, 183),
    hsl(209deg, 79%, 51%)
  ) !important;
  border-bottom: 3px solid #fff;
  box-shadow: 0 0 15px 0 rgb(0 0 0 / 30%);
  border-top: 3px solid #d6e5ff;
}
@media all and(max-width: 1024px) {
  .navbar-dark .navbar-toggler {
    border: none;
    box-shadow: none;
    border-radius: none;
  }
  .navbar.navbar-expand-lg .navbar-toggler.collapsed .navbar-toggler-icon {
    background-image: none !important;
    display: block;
    width: 18px;
    height: 2px;
    background: #fff;
    position: relative;
  }
  .navbar.navbar-expand-lg
    .navbar-toggler.collapsed
    .navbar-toggler-icon:before {
    content: "";
    width: 18px;
    height: 2px;
    background: #fff;
    position: absolute;
    top: -5px;
    left: 0;
    transform: initial;
  }
  .navbar.navbar-expand-lg
    .navbar-toggler.collapsed
    .navbar-toggler-icon:after {
    content: "";
    width: 18px;
    height: 2px;
    background: #fff;
    position: absolute;
    bottom: -5px;
    left: 0;
    transform: initial;
  }
  .navbar.navbar-expand-lg .navbar-toggler-icon {
    background-image: none !important;
    display: block;
    width: 18px;
    height: 2px;
    background: transparent;
    position: relative;
  }
  .navbar.navbar-expand-lg .navbar-toggler .navbar-toggler-icon:before {
    content: "";
    transform: rotate(45deg);
    background: #fff;
    top: 0px;
    left: 0;
    width: 18px;
    height: 2px;
    background: #fff;
    position: absolute;
  }
  .navbar.navbar-expand-lg .navbar-toggler .navbar-toggler-icon:after {
    content: "";
    transform: rotate(-45deg);
    background: #fff;
    bottom: 0px;
    left: 0;
    width: 18px;
    height: 2px;
    background: #fff;
    position: absolute;
  }
  .fixed-top {
    background: #4463cb !important;
    border-top: 15px solid #d6e5ff;
    transition: all 0.2s ease-in-out;
    box-shadow: 0px 0px 10px 0 rgb(0 0 0 / 20%);
    border-bottom: 3px solid #fff;
  }
}
</style>
