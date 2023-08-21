<template>
  <div class="container">
    <div class="row" style="padding:.7em">
      <div class="col-12 list-brand d-flex justify-content-center flex-wrap">
        <div v-for="brand of brands" :key="brand.id" style="padding:1em">
          <nuxt-link class="link-brand" :to="`/brands/${brand.slug}`">{{
            brand.name
          }}</nuxt-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
//   layout: "brandsletters",
  async asyncData({ route, $axios, store }) {
    const letter = route.params.letter;
    const subdomain = store.getters["cities/activeCity"].subdomain.name;
    const brands = await $axios.get(`/api/v1/brands/letter/${letter}/?subdomain=${subdomain}`);
    return { letter: letter, brands: brands.data };
  },
};
</script>


<style lang="scss" scoped>
.list-brand {
  background: #ffff;
  margin-top: 3em;
  border-radius: 12px;
}
.link-brand {
  color: #363636;
  text-decoration: none;
  font-weight: 400;
  font-size: 14px;
}
</style>
