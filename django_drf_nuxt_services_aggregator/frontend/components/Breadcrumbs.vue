<template>
    <!--
    <Breadcrumbs
        :paths="[{ to: '/test', name: 'test' }, { to: '/test2', name: 'test2' },]"
        :current_page="category_name.name"
    />
    -->
    <nav id="breadcrumbs" aria-label="breadcrumb">
        <div class="container">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <Nuxt-link class="" active-class="" exact-active-class="" :to="{ name: 'index' }">Главная</Nuxt-link>
                </li>
                <li v-for="(path, index) in paths" :key="index"
                    class="breadcrumb-item">
                    <Nuxt-link class="" active-class="" exact-active-class="" :to="path.to">{{ path.name }}</Nuxt-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">{{ current_page }}</li>
            </ol>
        </div>
    </nav>
</template>

<script>
export default {
    props: {
        paths: {
            type: Array,
            required: false
        },
        current_page: {
            type: String,
            required: true
        }
    }
}
</script>

<style lang="scss">
#breadcrumbs{
    margin-top: 30px;
}
</style>
