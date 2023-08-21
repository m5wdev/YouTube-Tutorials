<template>
    <button :class="btn_class">{{ btn_text }}</button>
</template>

<script>
export default {
    props: {
        btn_class: String,
        btn_text: String,
    },
}
</script>

<style>

</style>
