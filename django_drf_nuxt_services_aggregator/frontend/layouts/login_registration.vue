<template>
  <div class="layout login-registration">
    <div>
      <div id="bg"></div>
      <ChunksHeader />
    </div>
    <main>
      <div class="my-3">
        <Nuxt />
      </div>
    </main>
    <ChunksFooter />
    <ModalsApplication />
  </div>
</template>

<script>
export default {
  middleware: "cities",
  async fetch() {
    if (this.$store.getters["cities/cities"].length === 0) {
      await this.$store.dispatch("cities/fetch");
    }
  },
  head() {
    return {
      meta: [
        {
          hid: 'og:site_name',
          property: "og:site_name",
          content: `Servis-Centers.ru – реестр сервисных центров ${this.$store.getters["cities/activeCity"].declension_p}`,
        },
      ],
    };
  },
};
</script>

<style>
  .login-registration .btn-group{
    background: #fff;
    border-radius: 6px;
    margin-bottom: 20px;
    box-shadow: 5px 5px 10px 0 rgb(0 0 0 / 20%);
  }
  .login-registration .btn-group .btn.btn-outline-primary.active, .login-registration .btn-group .btn:hover{
    color: #fff;
    background-color: #4463cb;
    border-color: transparent;
  }
  .login-registration .btn-group .btn-outline-primary {
    color: #222;
    border-color: transparent;
  }
  .login-registration .btn-group .btn:hover, .login-registration .btn-group .btn:focus{
    box-shadow: none;
  }
  .login-registration .mt-4.more-button{
    margin-top: 0 !important;
  }
  .login-registration h6, .login-registration .h5{
    color: #fff;
    font-size: 1.5rem;
  }
  .login-registration label{
    color: #fff;
  }
</style>
