<script setup>
import { RouterView } from 'vue-router'

import MainNav from '@/components/MainNav.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
    <MainNav />

    <header class="py-3">
    </header>

    <RouterView />

    <Footer />
</template>


<style scoped>
</style>
