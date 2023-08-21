<template>
  <div class="col box-services">
    <div class="box-services__inner">
      <div class="box-services__img">
        <!-- <img
          v-if="category.logo"
          width="64"
          height="64"
          :scr="category.logo"
          alt=""
        /> -->
        <img height="64" width="64" :src="'https://servis-centers.ru'+category.logo" :alt="category.logo">
      </div>
      <div class="box-services__name h5">{{ category.name }}</div>
      <div class="box-services__subcategories">
        <span
          v-for="(subcategory, index) in category.children_category"
          :key="subcategory.id"
        >
          <Nuxt-link :to="`/${subcategory.slug}`" class="item-category">{{
            subcategory.name
          }}</Nuxt-link>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    category: Object,
  },
};
</script>

<style lang="scss" scoped>
.box-services {
  &__inner {
    background-color: white;
    padding: 15px;
    height: 100%;
    box-shadow: 0 1px 5px hsl(0deg 0% 86% / 50%);

    display: grid;
    grid-template-rows: auto auto 1fr;
    row-gap: 15px;
  }

  &__img,
  &__name {
    text-align: center;
  }

  &__subcategories {
    line-height: 1.2;
    word-wrap: anywhere;

    a {
      // font-size: .9rem;
      text-decoration: none;
    }
  }
}
</style>
