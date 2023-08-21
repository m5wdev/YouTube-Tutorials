<template>
    <button v-if="phone" type="button" class="btn btn-primary">
        <span
            v-if="phoneHide"
            @click="phoneHide = 0"
            :href="OnPhone(phone)"
            >{{ phone.substring(0, phone.length - 3) }}..**</span>
        <a
            v-if="!phoneHide"
            :href="OnPhone(phone)"
            >{{ phone }}</a>
    </button>
</template>

<script>
export default {
    props: ["phone"],
    data() {
        return {
            phoneHide: true,
        }
    },
    methods: {
        OnPhone(company_phone) {
            return `tel:${company_phone}`;
        },
    },
}
</script>

<style>
.card-text .btn > span, .card-text .btn > a{
    color: #fff;
    text-decoration: none;
    display: inline-block;
    transform: skewX(10deg);
}
</style>
