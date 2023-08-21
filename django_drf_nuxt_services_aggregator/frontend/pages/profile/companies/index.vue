<template>
    <div class="container">
        <div class="row mb-4">
            <h1>Мои компании</h1>
        </div>

        <template v-if="companies">
            <CompanyCardCompany v-for="company in companies" :key="company.id" :company="company" />
        </template>
    </div>
</template>

<script>
export default {
    async asyncData({ $axios, req, store, route }) {
        const resp_data = await $axios.get(`/api/v1/companies/user-companies/`)
        return {
            companies: resp_data.data,
        }
    },
    middleware: "auth",
    layout: "profile",
}
</script>
