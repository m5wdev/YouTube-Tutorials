<template>
    <span :class="classes">
        <a class="dashed-link"
            v-if="emailHide"
            @click.prevent="emailHide = false"
            href="#">
            <span class="email-text-container">
                {{ email.substring(0, email.length - 5) }}..**
            </span>
        </a>
        <a class="dashed-link"
            v-if="!emailHide"
            :href="`mailto:${email}`">
            <span class="email-text-container">
                {{ email }}
            </span>
        </a>
    </span>
</template>

<script>
export default {
    props: ["email", "classes"],
    data() {
        return {
            emailHide: true,
        }
    },
}
</script>

<style>

</style>
